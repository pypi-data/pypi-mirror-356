import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
from scipy.optimize import curve_fit
from scipy import integrate, stats
import pickle
import csv
import re

class CAF_Analysis:
    def __init__(self, setpoint_file, pmt_folder, avg=5):
        self.setpoint_file = setpoint_file
        self.pmt_folder = pmt_folder
        self.avg = avg
        self.new_colour = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4', '#6A4C93']
        self.QLMblue = '#1982C4'
        self.decimation = 32
        self.sampling_rate = 125e6
        self.time_axis = np.array([x / (self.sampling_rate / self.decimation) * 1e3 for x in range(16384)])
        self.title = ""
        self.average_p2_diff = None
        self.avgdata = None
        self.peak2 = None
        self.peak_height = peak_height
        self.peak_distance = peak_distance
        self.peak_prominence = peak_prominence
        self.show_plot = show_plot
        self.return_peaks = return_peaks
        self.polyorder = polyorder
        self.buffer = buffer
        self.window_length = window_length

    def load_data(self):
        npy_files = [f for f in os.listdir(self.pmt_folder) if f.endswith(".npy") and "_run_PMT_" in f]
        if not npy_files:
            raise FileNotFoundError(f"No matching .npy files found in {self.pmt_folder}")
        data_path = os.path.join(self.pmt_folder, npy_files[0])
        return np.load(data_path)

    def smooth_data(self, data):
        return savgol_filter(data, window_length=self.window_length, polyorder=self.polyorder)

    def find_peaks(self, data):
        peaks, properties = find_peaks(
            data,
            height=self.peak_height,
            distance=self.peak_distance,
            prominence=self.peak_prominence
        )
        return peaks

    def plot(self, time, smoothed_data, peaks, raw_data):
        plt.figure(figsize=(12, 6))
        plt.plot(time, smoothed_data, label="Smoothed Data", color='black')
        plt.plot(time[peaks], smoothed_data[peaks], "ro", label="Peaks")
        plt.scatter(time, raw_data, marker='o', label="Raw Data", s=10, alpha=0.3)
        plt.xlabel("Time (ms)")
        plt.ylabel("Signal (a.u.)")
        plt.title("TOF Signal with Peaks")
        plt.legend()
        plt.tight_layout()
        plt.show()
    def compute_time_axis(self):
        buff_length = range(16384)
        rate = self.sampling_rate / self.decimation
        time = np.array([x / rate * 1e3 for x in buff_length])  # ms
        return time


    def averageTOF(self):
        data = self.load_data()
        time = self.compute_time_axis()
        raw_data = data[self.buffer:]
        time = time[self.buffer:]

        smoothed_data = self.smooth_data(raw_data)
        peaks = self.find_peaks(smoothed_data)
        tof_times = time[peaks]

        if self.show_plot:
            self.plot(time, smoothed_data, peaks, raw_data)

        if self.return_peaks:
            return np.round(tof_times, 3)
        else:
            print("TOF peak times (ms):", np.round(tof_times, 3))


    @staticmethod
    def line(x, m, c):
        return m * x + c

    @staticmethod
    def get_std_dev(ls):
        n = len(ls)
        mean = sum(ls) / n
        var = sum((x - mean) ** 2 for x in ls) / (n - 1)
        return var ** 0.5

    @staticmethod
    def gaussian(x, a, b, c, d):
        return a * np.exp(-(x - b) ** 2 / (2 * c ** 2)) + d



    def ExtractDataSetpoint(self,filename, FindResiduals):
        """Extracts the setpoint data from the STCL GUI and packages it into lists.
        
        Args: 
            filename (r string): filepath for the saved setpoint data.
            
        Returns:
            Setpoint data (list of arrays): List of several arrays: indices, desired 
            setpoint, peak 1 position, peak 2 position, peak 3 position."""
            
        x=[]
        
        with open(filename,'r', encoding='utf-8-sig') as csvfile:
        
            plots = csv.reader(csvfile, delimiter = ',')
            
            for each_row in plots:
                #print(each_row)
                x.append((each_row[0]))
                
        index =[]
        setpoint = []
        peak1 = []
        peak2 = []
        peak3 = []
        lockcheck = []
    
        for i in range(int(len(x)/6)):
            index.append(float(x[i*6]))
            setpoint.append(float(x[i*6 +1]))
            peak1.append(float(x[i*6 +2])/84000) # /84000 is to convert to ms from arduino units
            peak2.append(float(x[i*6 +3])/84000)
            peak3.append(float(x[i*6+4])/84000)
            lockcheck.append(float(x[i*6 + 5]))
            
        time = np.array(range(len(peak1)))*0.5 #time is given as such because we take a reading every 0.5s

        #plotting the behaviour of the three peaks, as a quick diagonostic
        fig, axs = plt.subplots(3, sharex=True)
        axs[0].set_title(filename[-22:], fontsize=18)
        axs[0].scatter(time, peak1, color=new_colour[3])
        axs[1].scatter(time, peak2,color=new_colour[1])
        axs[2].scatter(time, peak3, color=new_colour[2])
        axs[0].set_ylim(min(peak1)-0.05, max(peak1)+0.05)
        if min(peak2)-0.05 > 0:
            lowerlim = min(peak2)-0.05
        if min(peak2)-0.05 < 0:
            lowerlim = 0
        if max(peak2)+0.05 < 10:
            greaterlim = max(peak2)+0.05
        if max(peak2)+0.05 > 10:
            greaterlim = 10
        axs[1].set_ylim(lowerlim, greaterlim)
        axs[2].set_ylim(min(peak3)-0.05, max(peak3)+0.05)
        axs[2].set_xlabel('Time (s)')
        axs[0].set_ylabel('Peak 1 (ms)')
        axs[1].set_ylabel('Peak 2 (ms)')
        axs[2].set_ylabel('Peak 3 (ms)')
        
        fig = plt.figure(figsize=(7,5), dpi=400)
        ax = fig.add_subplot()
        ax.set_xlabel('Time (s)', fontsize=18)
        ax.tick_params(axis='x', labelsize=17)
        ax.tick_params(axis='y', labelsize=17)
        ax.tick_params(axis="y",direction="in")
        ax.tick_params(axis="x",direction="in")
        ax.scatter(time, np.array(peak2)-np.array(peak1))
        ax.set_ylabel('Peak2-peak1 difference (ms)', fontsize=16)
        
        if FindResiduals:
            FindLaserPositionResiduals(np.array(peak1), np.array(peak2))

            
        return [np.array(index), np.array(setpoint), np.array(peak1), np.array(peak2), np.array(peak3)]


    def ExtractDataSetpointTWOPEAK(self,filename, FindResiduals):
        """Extracts the setpoint data and packages it into lists. 
        Specifically for the two peak locking, as it only deals with peak 1 and peak 2.
        
        Args: 
            filename (r string): filepath for the saved setpoint data.
            
        Returns:
            Setpoint data (list of arrays): List of several arrays: indices, desired 
            setpoint, peak 1 position, peak 2 position."""
        x=[]
        
        with open(filename,'r', encoding='utf-8-sig') as csvfile:
        
            plots = csv.reader(csvfile, delimiter = ',')
            
            for each_row in plots:
                #print(each_row)
                x.append((each_row[0]))
                
        index =[]
        setpoint = []
        peak1 = []
        peak2 = []
        lockcheck = []
    
        
        for i in range(int(len(x)/5)):
            index.append(float(x[i*5]))
            setpoint.append(float(x[i*5 +1]))
            peak1.append(float(x[i*5 +2])/84000)
            peak2.append(float(x[i*5 +3])/84000)
            lockcheck.append(float(x[i*5 + 4]))
            
        time = np.array(range(len(peak1)))*0.5

        fig, axs = plt.subplots(2, sharex=True)
        axs[0].set_title(filename[-22:], fontsize=18)
        axs[0].scatter(time, peak1, color=new_colour[3])
        axs[1].scatter(time, peak2,color=new_colour[1])
        axs[0].set_ylim(min(peak1)-0.05, max(peak1)+0.05)
        if min(peak2)-0.05 > 0:
            lowerlim = min(peak2)-0.05
        if min(peak2)-0.05 < 0:
            lowerlim = 0
        if max(peak2)+0.05 < 10:
            greaterlim = max(peak2)+0.05
        if max(peak2)+0.05 > 10:
            greaterlim = 10
        axs[1].set_ylim(lowerlim, greaterlim)
        axs[0].set_ylabel('Peak 1 (ms)')
        axs[1].set_ylabel('Peak 2 (ms)')
        
        peak1 = np.array(peak1)
        peak2 = np.array(peak2)
        
        fig = plt.figure(figsize=(7,5), dpi=400)
        ax = fig.add_subplot()
        ax.set_xlabel('Time (s)', fontsize=18)
        ax.tick_params(axis='x', labelsize=17)
        ax.tick_params(axis='y', labelsize=17)
        ax.tick_params(axis="y",direction="in")
        ax.tick_params(axis="x",direction="in")
        ax.scatter(time, peak2-peak1)
        ax.set_ylabel('Peak2-peak1 difference (ms)')
        
        if FindResiduals:
            FindLaserPositionResiduals(np.array(peak1), np.array(peak2))


            
        return [np.array(index), np.array(setpoint), np.array(peak1), np.array(peak2)]

    def FindLaserPositionResiduals(self,p1, p2):
        """ Function you can use to evaluate how much of a straight line the peak
        positions follow. Will return the fit to the first peak position in ms because
        I don't have a conversion yet, but the second peak position should be in MHz,
        with the current conversion factor 233MHz/ms"""
        
        p1 = p1 -p1[0]
        p1 = p1*1 #eventually we need a conversion factor for this
        
        p2 = p2 -p2[0]
        p2 = p2*233
        
        time = np.array(range(len(p1)))*0.5
        
        #fitting the reference peak
        popt, pcov = curve_fit(line, time, p1, p0=[0.5, 1.5])
        
        #print(f'Gradient: {popt[0]}, Intercept:{popt[1]}')

        residuals = p1 - line(time, popt[0], popt[1])

        fig = plt.figure(figsize=(7,5), dpi=400)
        ax = fig.add_subplot()
        ax.set_xlabel('Time (s)', fontsize=18)
        ax.tick_params(axis='x', labelsize=17)
        ax.tick_params(axis='y', labelsize=17)
        ax.tick_params(axis="y",direction="in")
        ax.tick_params(axis="x",direction="in")
        result = ax.hist(residuals, bins=20, alpha=0.6, color=new_colour[4])
        meanb = np.mean(residuals)
        sd = get_std_dev(residuals)
        x1 = np.linspace(min(residuals), max(residuals), 100)
        dx1 = result[1][1] - result[1][0]
        scale1 = len(residuals)*dx1 #scaling the curves to match the histogram
        fwhmb = 2*np.sqrt(2*np.log(2))*sd
        ax.plot(x1, scipy.stats.norm.pdf(x1, meanb, sd)*scale1, label=f'FWHM: {fwhmb:.4}, \n mean: {meanb:.5}', color='k')
        ax.set_xlabel('Reference peak position \n deviation from straight line (ms)')
        ax.set_title(f'Reference laser residuals', fontsize=18)
        ax.legend(fontsize=15)
        
        
        #fitting the follower peak
        popt, pcov = curve_fit(line, time[0:-20], p2[0:-20], p0=[0.5, 1.5])
        
        #print(f'Gradient: {popt[0]}, Intercept:{popt[1]}')
        
        fig = plt.figure(figsize=(7,4), dpi=400)
        ax = fig.add_subplot()
        ax.set_ylabel('Peak position (MHz)', fontsize=18)
        ax.set_xlabel('Time (s)', fontsize=18)
        ax.tick_params(axis='x', labelsize=17)
        ax.tick_params(axis='y', labelsize=17)
        ax.tick_params(axis="y",direction="in")
        ax.tick_params(axis="x",direction="in")
        ax.plot(time, line(time, popt[0], popt[1]), color='k')
        ax.scatter(time[0:-20], p2[0:-20],color=new_colour[1])
        ax.set_title('Fitting a straight line to follower laser data', fontsize=18)


        residuals = p2 - line(time, popt[0], popt[1])
        
        residuals = residuals[0:-20]


        fig = plt.figure(figsize=(7,5), dpi=400)
        ax = fig.add_subplot()
        ax.set_xlabel('Time (s)', fontsize=18)
        ax.tick_params(axis='x', labelsize=17)
        ax.tick_params(axis='y', labelsize=17)
        ax.tick_params(axis="y",direction="in")
        ax.tick_params(axis="x",direction="in")
        result = ax.hist(residuals, bins=20, alpha=0.6, color=new_colour[1])
        meanb = np.mean(residuals)
        sd = get_std_dev(residuals)
        x1 = np.linspace(min(residuals), max(residuals), 100)
        dx1 = result[1][1] - result[1][0]
        scale1 = len(residuals)*dx1 #scaling the curves to match the histogram
        fwhmb = 2*np.sqrt(2*np.log(2))*sd
        ax.plot(x1, scipy.stats.norm.pdf(x1, meanb, sd)*scale1, label=f'FWHM: {fwhmb:.4}, \n mean: {meanb:.5}', color='k')
        ax.set_xlabel('Follower peak position \n deviation from straight line (MHz)')
        ax.set_title(f'Follower laser residuals', fontsize=18)
        ax.legend(fontsize=15)


    def PlotAverageTOF(self,PMTfilename, fitGaussian, initialguess=0):
        """Plotting a TOF profile that includes all data, averaged over all frequencies, 
        to give an idea of what the data looks like.
        
        Args:
            PMTfilename (string): folder path where all the data is saved.
            fitGaussian (bool): if True, will fit a Gaussian to the TOF profile
            initialguess (array): initial guess parameters for the TOF gaussian fit."""
        
        print('')
        print('Plotting an average TOF...')
        
        try:

            filename = os.path.join(PMTfilename, 'pickledunprocesseddata.pkl')  
            print(f'Unprocessed data found: {filename}')
            #averagep2diff, avgdata, title = UnpickleUnprocessedData(filename)
            
            with open(filename, 'rb') as file:
                newdata = pickle.load(file)
            
                averagep2diff, avgdata, title = newdata
            
            
            buff_length = range(16384)
            dec = 32
            rate = 125*10**6/dec
            time = [x / rate *10**3 for x in buff_length]
            
            fig = plt.figure(figsize=(7,5))
            ax = fig.add_subplot()
            ax.tick_params(axis='x', labelsize=16,direction="in")
            ax.tick_params(axis='y', labelsize=16,direction="in")
            ax.set_ylabel('Background free signal (arb)', fontsize=17)
            ax.set_xlabel('Time (ms)', fontsize=17)
            
            #use from 1000 on, to remove the YAG peak
            #also remove the background
            background = np.mean(np.mean(avgdata,axis=0)[1000:][0:1000])
        
            backgroundfreedata = np.mean(avgdata,axis=0)[1000:] - background
        
            ax.scatter(time[1000:], backgroundfreedata, color=new_colour[1], s=3)
            ax.set_title('Average TOF profile: ' + title, fontsize=17)
            
            if fitGaussian == True:
        
                popt, pcov = scipy.optimize.curve_fit(gaussian, time[1000:], backgroundfreedata, p0=initialguess)
                a, b, c, d = popt
                err = np.sqrt(np.diag(pcov))
                
                ax.plot(time[1000:], gaussian(time[1000:], *popt), color='k')
                
                print(f'\tCentre of peak: {b:.4} ms')
                print(f'\tAmp. above background: {a:.4}')
                print(f'\tWidth: {c:.4} ms')
                
        except:
            print(f'No unprocessed data file found in this folder! Run DealWithAllData first!!')
            

    def DealwithPMTData(self,setpointfilename, PMTfilename, FindResiduals):
        """Takes the PMT data, extracts it, and deals with matching up the indexes for the PMT and setpoint data"""
        print('Dealing with the PMT and setpoint data...')
        #extract the setpoint data
        index, setpoint, p1, p2, p3 = ExtractDataSetpoint(setpointfilename, FindResiduals)
        #following for dealing with two peak locking data
        #index, setpoint, p1, p2 = ExtractDataSetpointTWOPEAK(setpointfilename, FindResiduals)
        
        #find the minimum index on the setpoint data- we want to start looking at the PMT data from here onwards
        minindexsp = int(min(index))
        maxindexsp = int(max(index))
        #print([minindexsp, maxindexsp])
        print(f'\tMin setpoint index: {minindexsp}, max setpoint index: {maxindexsp}')
        print(f'\tNumber of setpoints saved: {len(index)}')

        #see how many PMT datasets we've got
        obj = os.scandir(PMTfilename)
        
        PMTcounter = 0
        # List all files and directories in the specified path
        print("Searching the PMT files in '% s'..." % PMTfilename)
        for entry in obj: #loop through them
            if entry.is_file() and entry.name.endswith('.npy'): #searches through the npy files
                PMTcounter += 1
        print(f'\tThe number of PMT files is {PMTcounter}')
        
        if maxindexsp < PMTcounter:
            #ie we assume we have more PMT files than SP indices, which should generally be the case
            end = maxindexsp
            size = len(range(minindexsp+1, end+2)) #the +1 here to account for index mismatching between 
            #PMT and sp data, the +2 is to account for the index mismatching, and also that range() ends 
            #one before the actual end you give
            print(f'\tThe length of the bigdata array we\'re making is {size}, BEFORE REMOVING THE FIRST ONE!' )
            bigdata = np.zeros((size,16384))
            
            for i in range(minindexsp+1, end+2): 
                name = os.path.join(PMTfilename, f'_run_PMT_{int(i)}.npy')
                data = np.load(name)
                bigdata[int(i-minindexsp-1)]=data
                
                
        if maxindexsp > PMTcounter:
            #ie we assume we have more SP indices than PMT files- shouldn't be the case
            end = PMTcounter
            size = len(range(minindexsp+1, end+1)) #the +1 here to account for index mismatching between 
            #PMT and sp data, the +1 is to account for the index mismatching
            print(f'\tThe length of the bigdata array we\'re making is {size}, BEFORE REMOVING THE FIRST ONE' )
            bigdata = np.zeros((size,16384))
            
            for i in range(minindexsp+1, end+1): 
                name = os.path.join(PMTfilename, f'_run_PMT_{int(i)}.npy')

                data = np.load(name)
                bigdata[int(i-minindexsp-1)]=data
            
        #want to remove the first instance from the setpoint and PMT data, to remove the weird one
        #that is recorded before any jumps have happened 
        bigdata = bigdata[1:]
        p2 = p2[1:]
        p1 = p1[1:]
            
        print(f'\tThe length of the peak array is {len(p2)}, and the PMT data array is {np.shape(bigdata)}')
        return bigdata, p2, index, p1

    #Setpointfilename = r'K:\Experimental\HF scan data\2024_06_21\HFscan3\_Setpoints'
    #PMTfilename = r'K:\Experimental\HF scan data\2024_06_21\HFscan3'
    #bigdata, p2, index, p1 = DealwithPMTData(Setpointfilename, PMTfilename) 


    def AverageData(self,bigdata, avg):
        """Averages the PMT data (bigdata) over the range you specify - eg every 'avg' runs get averaged together"""
        length = int(len(bigdata))
        
        temp = np.zeros((avg,16384))
        
        averaged = np.zeros((int(length/avg), 16384))
        
        counter = 0
        for i in range(length):
            temp[counter] = bigdata[i]
            
            counter += 1
            if counter == avg:
                averaged[int(i/avg)] = np.mean(temp,axis=0)
                
                counter = 0
                
        print(f'Shape of the averaged data array is {np.shape(averaged)}')
        return averaged

    # Also average the peak position?

    def AveragePeakPositionSD(self,p2, avg):
        """To give us something to plot against, also average every 'avg' peak 2 positions"""
        print('p2 len')
        print(len(p2))
        peak = p2[0:-2]
        sd = []
        if len(peak)%avg == 0:
            print(len(peak))
            avgpeak = np.average(peak.reshape(-1, avg), axis=1)
            for i in range(len(avgpeak)):
                sd.append(get_std_dev(peak.reshape(-1, avg)[i]))
                
        else:
            x = len(peak)%avg
            peak = peak[0:-x]
            avgpeak = np.average(peak.reshape(-1, avg), axis=1)
            for i in range(len(avgpeak)):
                sd.append(get_std_dev(peak.reshape(-1, avg)[i]))
        
        print(f'Shape of the averaged peak array is {np.shape(avgpeak)}')
        return avgpeak, sd

    def AveragePeakPosition(self,p2, avg):
        """To give us something to plot against, also average every 'avg' peak 2 positions"""
        print('p2 len')
        print(len(p2))
        peak = p2[0:-2]
        if len(peak)%avg == 0:
            print(len(peak))
            avgpeak = np.average(peak.reshape(-1, avg), axis=1)           
        else:
            x = len(peak)%avg
            peak = peak[0:-x]
            avgpeak = np.average(peak.reshape(-1, avg), axis=1)
        
        print(f'Shape of the averaged peak array is {np.shape(avgpeak)}')
        return avgpeak


    def AveragePeakDifference(self,p1, p2, avg):
        """This version should take calculate the spacing between the reference and follower peaks
        and then average that to generate the x axis"""
        print('Averaging the peak positions...')
        #OKAY I'M NOT SURE WHY THIS BIT IS HERE- WHY WOULD WE REMOVE THE LAST TWO DATA POINTS?
        #peak1 = p1[0:-2]
        #peak2 = p2[0:-2]
        peak1 = p1
        peak2 = p2
        difference = peak2-peak1
        sd = [] #standard deviation of the peak difference

        if len(difference)%avg == 0:
            avgpeak = np.average(difference.reshape(-1, avg), axis=1) 
            for i in range(len(avgpeak)):
                sd.append(get_std_dev(difference.reshape(-1, avg)[i]))         
        else:
            x = len(difference)%avg
            difference = difference[0:-x]
            avgpeak = np.average(difference.reshape(-1, avg), axis=1)
            for i in range(len(avgpeak)):
                sd.append(get_std_dev(difference.reshape(-1, avg)[i]))
            
        print(f'The number of avg peak positions is {len(avgpeak)}')
        
        return avgpeak, sd



    def PlotAverageDataIntegral(self,initialguess, PMTfilename, checkfitparams, plotMaximum, plotQuadintegral, plotTrapzintegral, SaveData, upperlimit):
        """Fit the averaged data to a gaussian, then extract the amplitude and centre plus 
        their errors. Find the amplitude and integrated area under the gaussian and then 
        plot that. Will look for a saved data file to plot, in the PMTfilename folder.
        Args:
            initialguess (list): the initial guess parameters for the gaussian fit. For 17cm,
                            the following seemed to work okay: [0.1, 1, 0.05, 0.005] 
                            For 40cm: [0.004, 1.9, 0.05, 0.005]. Definitely want to check the
                            fits though and make sure these parameters are appropriate!
            PMTfilename (string): the filepath for the folder where the PMT data is stored.
            checkfitparams (boolean): if True, will plot a gaussian for every 10th shot, 
                            hopefully giving a sense of how well the fit parameters are working.
            plotMaximum (boolean): if True, plot a frequency spectra in terms of the 
                            amplitudes extracted from the gaussian TOF fits.
            plotQuadIntegral (boolean): if True, plot a frequency spectra in terms of the area
                            under the TOF signal, as extracted by doing a quad integral under 
                            the fitted gaussian, between 0 and 3ms.
            plotTrapzIntegral (boolean): if True, plot a frequency spectra in terms of the area
                            under the TOF signal, as extracted by doing the trapz method of
                            integration under the actual data, not a fit.
            SaveData (boolean): if True, save the peak position data, as well as the amplitudes
                            and various integrals in a pkl file. This will save the data in 
                            the same file as the PMT data is saved.
                            
                            
        Returns:
            savename (string): the exact filepath for the saved pkl file, so you can immediately
                            output this into an unpacking function etc.
            """
            
        print('')
        print('Searching for a saved file with unprocessed data...')
        founddata = False
        #look in the filepath specified by PMT filename
        try:

            filename = os.path.join(PMTfilename, 'pickledunprocesseddata.pkl')
            print(f'Found! {filename}')
            with open(filename, 'rb') as file:
                newdata = pickle.load(file)
            
                peak2, avgdata, title = newdata
                
            founddata = True
                
        except:
            
            print('no saved file containing unprocessed data found! ')
            
        
        if founddata == True:
            print('Starting to plot the data...')
            
            buff_length = range(16384)
            dec = 32
            rate = 125*10**6/dec
            time = [x / rate *10**3 for x in buff_length]
        
            amp = []
            amperr = []
            centre = []
            centreerr = []
            integral = []
            interror = []
            integral2 = []
            
            print(f'Length of avgdata array: {np.shape(avgdata)}')
            print(f'Length of peakdifference array: {len(peak2)}')
            

            
            #loops through the data and fits each averaged TOF to a gaussian
            for i in range(len(avgdata)):
                
                #[0.01, 1, 0.1, 0.01]
                try:
                    
                    background = np.mean(avgdata[i][-2000:])
                    #print(background)
                    
                    backgroundfreedata = avgdata[i] - background
        
                    #initialguess = [max(backgroundfreedata[1000:]), time[1000 + np.argmax(backgroundfreedata[1000:])], 0.05, 0]
                    
                    popt, pcov = scipy.optimize.curve_fit(gaussian, time[1000:], backgroundfreedata[1000:], p0=initialguess)
                    a, b, c, d = popt
                    err = np.sqrt(np.diag(pcov))
                    
                    if checkfitparams == True:
                        if i%15 == 0: #only plot every 10th gaussian 
                            fig = plt.figure(figsize=(6,4), dpi=100)
                            
                            ax = fig.add_subplot()
                            ax.tick_params(axis='x', labelsize=17,direction="in")
                            ax.tick_params(axis='y', labelsize=17,direction="in")
                            ax.set_xlabel('Time (ms)', fontsize=17)
                            ax.scatter(time[1000:], backgroundfreedata[1000:], color=new_colour[1])
                            #ax.set_ylim(0,0.1)
                            ax.plot(time[1000:], gaussian(time[1000:], a,b,c,d), color='k')
                            #print(b)
                            #ax.scatter(time[-2000:], avgdata[i][-2000:])
                            #ax.axhline(np.mean(avgdata[i][-2000:]))
                            
                    if 1 > b > 2.5 or a < 0:
                        amp.append(0)
                    else:
                        amp.append(a)
                    centre.append(b)
                    amperr.append(err[0])
                    centreerr.append(err[1])
                    
                    #integrate under gaussian between 0 and 4
                    intsignal = integrate.quad(gaussian, 0.5, 3, args=(a,b,c,d))
                    integral.append(intsignal[0])
                    interror.append(intsignal[1])
                    #integrate under the actual data
                    intsignal2 = np.trapz(backgroundfreedata[1000:-5000], time[1000:-5000])
                    integral2.append(intsignal2)
                        
                except RuntimeError:
                    print(f'Gaussian fit failed: image {i}')
                    amp.append(0)
                    amperr.append(0)
                    integral.append(0)
                    interror.append(0)
                    integral2.append(0)
        
            
            print(f'Length of data to plot: {len(amp)}')
            print(f'Length of freq data: {len(peak2*233)}')
            
            if len(amp) != len(peak2*233):
                print('oh no! not the same length for some reason')
                
                if len(amp) > len(peak2*233):
                    lendiff = -len(peak2*233) + len(amp)
                    amp = amp[0:-lendiff]
                    
                if len(amp) < len(peak2*233):
                    lendiff =  len(peak2*233) - len(amp)
                    #print(lendiff)
                    #print(len(peak2)-lendiff)
                    peak2 = peak2[0:len(peak2)-lendiff]
            
            print(f'Length of data to plot: {len(amp)}')
            print(f'Length of freq data: {len(peak2*233)}')
                    
                
            if plotMaximum == True:
                fig = plt.figure(figsize=(5,4), dpi=400)
                ax = fig.add_subplot()
                ax.set_title(title, fontsize=18)
                ax.tick_params(axis='x', labelsize=17,direction="in")
                ax.tick_params(axis='y', labelsize=17,direction="in")
                ax.set_xlabel('Peak 2 - peak 1 difference (MHz)', fontsize=18)
                ax.set_ylabel('Signal amplitude', fontsize=18)
                ax.errorbar(peak2*233, amp, fmt='o', yerr=amperr, color=QLMblue, markersize=3)
                #ax.set_ylim(-0.001, 4*np.mean(amp))
                ax.set_ylim(-0.001, upperlimit)
        
            if plotQuadintegral == True:
                fig = plt.figure(figsize=(5,4), dpi=400)
                ax = fig.add_subplot()
                ax.set_title(title, fontsize=18)
                ax.tick_params(axis='x', labelsize=17,direction="in")
                ax.tick_params(axis='y', labelsize=17,direction="in")
                ax.set_xlabel('Peak 2 position (MHz)', fontsize=18)
                ax.set_ylabel('Integrated signal, QUAD', fontsize=18)
                ax.errorbar(peak2*233, integral, yerr=interror, fmt= 'o', color= '#f748a5', markersize= 3)
                # ax.set_ylim(-0.0002)
            
            if plotTrapzintegral == True:
                fig = plt.figure(figsize=(5,4), dpi=400)
                ax = fig.add_subplot()
                ax.set_title(title, fontsize=18)
                ax.tick_params(axis='x', labelsize=17,direction="in")
                ax.tick_params(axis='y', labelsize=17,direction="in")
                ax.set_xlabel('Peak 2 position (MHz)', fontsize=18)
                ax.set_ylabel('Integrated signal,TRAPZ', fontsize=18)
                ax.scatter(peak2*233, integral2, color=new_colour[1], s=5)
                #ax.set_ylim(-0.0002)
            
            #want to have option to save the analysed data as well
            #pickle it for ease of use
            if SaveData == True: 
                #current_time = datetime.datetime.now()
                #DATEMARKER = str(current_time.day) + '-' + str(current_time.month) + '-' + str(current_time.year) + '-' + str(current_time.hour) + 'h' + str(current_time.minute) 
            
                alldata = [peak2, amp, amperr, integral, interror, integral2]
                

                savename = os.path.join(PMTfilename, 'pickledprocesseddata.pkl')
            
                with open(savename, 'wb') as file:
                    pickle.dump(alldata, file)
                    
            

        


    def DealWithAllData(self,PMTfilename, avg, SaveData, FindResiduals):
        """Combining all the functions from above, excluding plotting. ie processes
        all the data, getting it ready to plot. Will only do the long process of actually
        processing the data if a saved file doesn't already exist in PMTfilename folder.'
        Args:
            PMTfilename (string): file path for the folder where the PMT and setpoint data is saved.
            avg (int): number of shots taken at each frequency, ie we average over every n 
                        shots. 
            SaveData (bool): if True, pickles and saves the data (averaged peak2-peak1 difference, 
                        averaged PMT data and title (run number)). Saved in PMTfilename folder as
                        \pickledunprocesseddata.pkl
            FindResiduals (bool): if True, will fit the laser peak positions to straight lines and spit
            out graphs showing the residuals.
            
        """
        try:

            filename = os.path.join(PMTfilename, 'pickledunprocesseddata.pkl') 
            print(f'Filename with this data already found! {filename}')
            with open(filename, 'rb') as file:
                newdata = pickle.load(file)
            
                peak2, avgdata, title = newdata
        
        except:
            print('')
            print('Processing data...')
            

            setpointfilename = os.join(setpointfilename, '_Setpoints.csv')
            bigdata, p2, index, p1 = DealwithPMTData(setpointfilename, PMTfilename, FindResiduals) 
            avgdata = AverageData(bigdata, avg)
            averagep2diff, sd = AveragePeakDifference(p1,p2,avg)
            
            pattern = (r'(\D+)(\d+)(\D+)(\D+)(\d+)')
            name = PMTfilename
            runnumber = re.search(pattern, name, re.IGNORECASE).group(5)
            title = 'Run ' + str(runnumber)
            
            
            #have the option to save the unprocessed data as well- saves to the run folder
            if SaveData == True: 
                
                alldata = [averagep2diff, avgdata, title]
                

                savename = os.join(PMTfilename, 'pickledunprocesseddata.pkl')
                
                print(f'Saving data to {savename}...')
            
                with open(savename, 'wb') as file:
                    pickle.dump(alldata, file)#
                    
                    
            return averagep2diff, avgdata, title
            
        

    ########################################################################################
    # want to make some functions that should make the fitting of lorentzians easier       #
    ########################################################################################


    def UnpickleProcessedData(self,filename):
        print(f'\nUnpacking data in {filename}...')
        
        with open(filename, 'rb') as file:
            newdata = pickle.load(file)
        
            peakdiff, amp, amperr, integral, interror, integral2 = newdata

        print('\tdata unpickled!')
        return peakdiff, amp, amperr, integral, interror, integral2


    def UnpickleUnprocessedData(self,file):
        print(f'\nUnpacking data in {file}...')
        

        filename = os.path.join(file, 'pickledunprocesseddata.pkl')
        
        with open(filename, 'rb') as file:
            newdata = pickle.load(file)
        
            averagep2diff, avgdata, title = newdata

        print('\tdata unpickled!')
        return averagep2diff, avgdata, title


    def lorentz(self,t,A,x0,w):
        L = w/2
        return A*L**2/((t-x0)**2 + L**2) 


    def fourlorentz(self,t, a, a2, a3, a4, b, b2, b3, b4, c, d):
        return lorentz(t,a,b,c) + lorentz(t, a2,b2,c) + lorentz(t, a3,b3,c) + lorentz(t, a4,b4,c) + d

    def fourlorentzHF(self,t, a, a2, a3, a4, b,c,d):
        return lorentz(t,a,b,c) + lorentz(t, a2,b+74,c) + lorentz(t, a3,b+48+74,c) + lorentz(t, a4,b+74+48+24,c) + d


    def FitDataToLorentzians(self,PMTfilename, datatype, initialguess, cutoff, forceHF, OffsettoF0, SaveFig):
        
        """ Args:
                PMTfilename (string): filename of the folder you want to plot the data of.
                datatype (string): either 'amp' or 'quad' or 'trapz', specifies which type of data 
                                you want to plot
                initialguess (list): the initial guess parameters for the fit. If not forcing the HF
                                spacing, then it'll be [a, a2, a3, a4, b, b2, b3, b4, c, d], and 
                                if you are, then it'll be of the form [a, a2, a3, a4, b,c,d]. a 
                                values are the amplitudes, b are peak centres, c is the peak width
                                and d is an overall offset.
                cutoff (float): this is the y (signal) value above which you don't want to consider 
                                points. Essentially there to help remove points from anomalous 
                                gaussian fits which could affect the lorentzian fit.
                forceHF (boolean): if True, this will fit the spectra with lorentzians fixed at 74, 48 
                                and 24 MHz spacings. If not, the spacings will be a free parameter in 
                                the fit.
                OffsettoF0 (bool): if True, will plot the lorentzians offset such that the F=0 peak is 
                                    at 0 MHz.
                SaveFig (boolean): if True, this will save the resulting figure in the folder the pkl 
                                file is in. will be saved as an svg.
                
        """
        try:
            print('')
            print('Fitting data to Lorentzians...')
            filename = os.path.join(PMTfilename, 'pickledprocesseddata.pkl')
            
            print(filename)
            
            inputpeakdiff, amp, amperr, integral, interr, integral2 = UnpickleProcessedData(filename)
            
        # with open(filename, 'rb') as file:
        #     newdata = pickle.load(file)
        #     inputpeakdiff, amp, amperr, integral, interr, integral2 = newdata


            if datatype == 'amp':
                print('Using amplitude...')
                inputdata = amp
                inputerr = amperr
                colour = QLMblue
            if datatype == 'quad':
                print('Using quad integral...')
                inputdata = integral
                inputerr = interr
                colour =  '#f748a5'
            if datatype == 'trapz':
                print('Using trapz integral...')
                inputdata = integral2
                inputerr = np.zeros(len(integral2))
                colour = new_colour[1]
        
            
            peakdiff = []
            data = []
            error = []
            
            for i in range(len(inputdata)):
                if inputdata[i] < cutoff:
                    #print(f'Removed data point {i} as it is above the cutoff')  
                    data.append(inputdata[i])
                    peakdiff.append(inputpeakdiff[i])
                    error.append(inputerr[i])
                
            
            
            data = np.array(data)
            peakdiff = np.array(peakdiff)
            error = np.array(error)
            
            
            
            offset = 0
            
            fig = plt.figure(figsize=(7,5), dpi=400)
            ax = fig.add_subplot()
            ax.tick_params(axis='x', labelsize=17,direction="in")
            ax.tick_params(axis='y', labelsize=17,direction="in")
            ax.set_xlabel('Peak 2 - peak 1 difference (MHz)', fontsize=18)
            ax.set_ylabel('Signal', fontsize=18)
            t = peakdiff*233
        # ax.set_ylim(-0.001, 0.01)
            
            #firstindexguess = t[np.argmax(data)]
            #print(firstindexguess)
            #print(t[int(len(t)/2)])
            #if firstindexguess > t[int(len(t)/2)]:
            #    firstindexguess = t[np.argmax(data)] -140
            #    print(firstindexguess)

            if forceHF == True:
                popt, pcov = scipy.optimize.curve_fit(fourlorentzHF, t, data, p0=initialguess)
                a, a2, a3, a4, b,c,d= popt
                err = np.sqrt(np.diag(pcov))
        
                print('Lorentz one:')
                print(f'a: {a:.3}, b: {b:.4}, c: {c:.3}')
                print('Lorentz two:')
                print(f'a: {a2:.3}, b: {b+74:.4}')
                print('Lorentz three:')
                print(f'a: {a3:.3}, b: {b+74+48:.4}')
                print('Lorentz four:')
                print(f'a: {a4:.3}, b: {b+74+24+48:.4}')
                print('Offset:')
                print(f'd: {d:.3}')
                
                
                
                if OffsettoF0 == True:
                    offset = b + 74
        
                ax.plot(t - offset, fourlorentzHF(t, a, a2, a3, a4, b,c,d), color='k', linestyle='--')
        
                ax.plot(t - offset, lorentz(t, a, b, c) +d, color='darkgray', linestyle='-.')
                ax.plot(t - offset, lorentz(t, a2, b+74, c) +d, color='darkgray', linestyle='-.')
                ax.plot(t - offset, lorentz(t, a3, b+74+48, c) + d, color='darkgray', linestyle='-.')
                ax.plot(t - offset, lorentz(t, a4, b+74+48+24, c) +d, color='darkgray', linestyle='-.')
                
            else:
                print('in else func')

                popt, pcov = scipy.optimize.curve_fit(fourlorentz, t, data, p0=initialguess)
                a, a2, a3, a4, b, b2, b3, b4, c, d = popt
                err = np.sqrt(np.diag(pcov))
        
                print('fit to function')
                
                print('Lorentz one:')
                print(f'a: {a:.3}, b: {b:.4}, c: {c:.3}')
                print('Lorentz two:')
                print(f'a: {a2:.3}, b: {b2:.4}')
                print('Lorentz three:')
                print(f'a: {a3:.3}, b: {b3:.4}')
                print('Lorentz four:')
                print(f'a: {a4:.3}, b: {b4:.4}')
                print('Offset:')
                print(f'd: {d:.3}')
                print('')
                print(f'Spacings: {b4-b3:.3}, {b3-b2:.3}, {b2-b:.3} MHz')
        
                if OffsettoF0 == True:
                    offset = b2
        
                ax.plot(t - offset, fourlorentz(t, a, a2, a3, a4, b, b2, b3, b4, c, d), color='k', linestyle='--')
        
                ax.plot(t - offset, lorentz(t, a, b, c) + d, color='darkgray', linestyle='-.')
                ax.plot(t - offset, lorentz(t, a2, b2, c) +d, color='darkgray', linestyle='-.')
                ax.plot(t - offset, lorentz(t, a3, b3, c) +d , color='darkgray', linestyle='-.')
                ax.plot(t - offset, lorentz(t, a4, b4, c) +d, color='darkgray', linestyle='-.')
        
            ax.errorbar(t - offset, data, yerr =error, fmt='o', markersize=3, color=colour)
        
            #ax.set_ylim(-0.001, 0.01)
            pattern = (r'(\D+)(\d+)(\D+)(\D+)(\d+)')
            runnumber = re.search(pattern, filename, re.IGNORECASE).group(5)
            title = 'Run ' + str(runnumber)
            ax.set_title(title, fontsize=17)
        
            filestem = re.search(pattern, filename, re.IGNORECASE).group(1)
        
            if SaveFig == True:
                filestem = os.path.dirname(filename)
                tosaveas = filestem + '\Lorentzianfitplot_' + datatype + '_' + title +'.svg'
                plt.savefig(tosaveas, dpi=600, bbox_inches = 'tight', format='svg', transparent=True)
                
            return b, err[4] #return the first peak position, and the error in it for velocity analysis later!
                
        except:
            print(f'No file of processed data found in this folder! Run PlotAverageDataIntegral first!!')
                
            
    ###################################################################################################        
    #      THE FOLLOWING FUNCTIONS ARE IMPORTANT FOR VELOCITY ANALYSIS                                #
    ###################################################################################################

    def GenerateFrequencySpectra(self,filename, windowsize, starttime, endtime, PlotFreqSpec, HFfixed):
        """This function splits the angled TOF data into windows, and then generates a frequency spectrum for each window.
            Args:
                filename (string): filepath for the unprocessed data for the angled run. Not the full filename- internally
                                    UnpickleUnprocessedData will add the filename suffix and look for the data
                windowsize (float): Size of the windows in ms.
                starttime (float): Desired start time to begin taking windows (ie about the start of the TOF hump, so we're
                                actually looking at a time with molecules).
                endtime (float): Desired start time to stop taking windows (ie about the end of the TOF hump, so we're
                                only looking at times with molecules).
                PlotFreqSpec (bool): if True, will plot the frequency spectrum for each time window. Good for visual diagnostics
                HFfixed (bool): if True, will fit the window data frequency spectra with the peak spacings fixed. Otherwise,
                                these spacings will be free fit params.
                                
            Returns:
                windowcentres (list): List of the central time values of each window in ms. 
                F1peakcentres (list): List of the F = 1- peak position in each window. Given in MHz (as converted from p2-p1 difference)
                F1peakcentres_err (list) : List of error in the F = 1- peak position in each window as determined from the Lorentzian fit.
                """
                
                
        #access the unprocessed data for the angled run
        avgp2diff, avgdata, title = UnpickleUnprocessedData(filename)
        
        #generate the time axis
        buff_length = range(16384)
        dec = 32
        rate = 125*10**6/dec
        time = [x / rate *10**3 for x in buff_length]
    # print(time[1000])
        
        print(time[1000])
        #to 'remove' YAG peak, ignore the first 1000 data points
        avgdata = avgdata[:,1000:]
        time = time[1000:]
        
        print(time[0])
        
        #first, need to sort through the data into windows
        
        #total number of windows needed to span all of the TOF
        windownumber = int((max(time)-time[0])/windowsize)
        #size of window in index units, not ms
        windowsize_index = int(15384/windownumber) #hmm unsure about this minus 1 here!!!
        
        #work out which window the start and end time fall in - we're not actually going to consider the whole TOF
        #got the -time[0]ms here to account for the fact that we disregard the first 1000 points because of the YAG
        starttime_window = int((starttime-time[0])/windowsize)
        endtime_window = int((endtime-time[0])/windowsize)
        print(starttime_window)
        print(endtime_window)
        
        
        #convert the p2-p1 difference to frequency: Currently using 233 MHz/ms conversion
        freq = np.array(avgp2diff)*233
        #freq = freq[:-20]

        

        print(f'Total number of windows needed: {endtime_window-starttime_window} {windownumber}, number of data points per window: {windowsize_index}')
        
        print(f'Shape of the avgdata array: {np.shape(avgdata)}')
        
        #for testing purposes, visually show that the windows have been generated okay

        
        #finding the background level, so we can remove it later
        avgTOF = np.mean(avgdata,axis=0)
        initialguess = [max(avgTOF), time[np.argmax(avgTOF)], 0.5, 0.005]
        popt, pcov = scipy.optimize.curve_fit(gaussian, time, avgTOF, p0=initialguess)
        a, b, c, d = popt
        background = d
        
        fig = plt.figure(figsize=(7,5))
        ax = fig.add_subplot()
        ax.tick_params(axis='x', labelsize=16,direction="in")
        ax.tick_params(axis='y', labelsize=16,direction="in")
        ax.set_ylabel('Signal (background removed)', fontsize=17)
        ax.set_xlabel('Time (ms)', fontsize=17)
        #ax.scatter(time, avgTOF, color='lightgray', s=3)
        ax.scatter(time, avgTOF-background, color='darkgray', s=3)
        ax.axvline(starttime, color='k')
        ax.axvline(endtime, color='k')
        
        
        ax.plot(time, gaussian(time, *popt) - background, color='k', linestyle='--')
        print(f'background level is {d}')
        #ax.set_xlim(1.4, 1.6)
        
        #create an empty list for the F=1 peak centres
        windowcentres = []
        F1peakcentres = []
        F1peakcentres_err = []
        peakwidths = []
        peakwidths_err = []
        windownumber = []
        spacing1 = []
        spacing2 = []
        spacing3 = []
        spacing1err = []
        spacing2err = []
        spacing3err = []
        #so many lists oh no 
        
        
        
        #fit the data to lorentzians
        for i in range(starttime_window, endtime_window):
        #for i in [124]:
            #separate out the TOF data that is in the arrival time window
            windowdata = avgdata[:, i*windowsize_index + i: (i+1)*windowsize_index + i] 
            
            #plotting the window data in the figure generated above, to check that it's okay visually
            #BACKGROUND CORRECTED
            ax.scatter(time[i*windowsize_index + i:(i+1)*windowsize_index + i], np.mean(windowdata,axis=0)-background, s=3, color=colour_list[i%16])
            
            #print(time[i*windowsize_index + i] - time[(i+1)*windowsize_index + i -1])
            #print(time[(i+1)*windowsize_index + i -1])
            
            
            #to test, just work with the average of the data in the window rather than integral etc
            #ie average the height of the data in the window
            windowdata_avg = np.mean(windowdata,axis=1)
            windowdata_avg = np.array(windowdata_avg[0:]) - background
            #print(np.shape(windowdata_avg))
            
            if len(windowdata_avg) != len(freq):
                print('oh no! not the same length for some reason')
                
                if len(windowdata_avg) > len(freq):
                    lendiff = -len(freq) + len(windowdata_avg)
                    windowdata_avg = windowdata_avg[0:-lendiff]
                    
                if len(windowdata_avg) < len(freq):
                    lendiff =  len(freq) - len(windowdata_avg)
                    #print(lendiff)
                    #print(len(peak2)-lendiff)
                    freq = freq[0:len(freq)-lendiff]
                    
            if PlotFreqSpec == True:
                #plot each window's data as a freq spectrum
                fig = plt.figure(figsize=(7,5))
                ax1 = fig.add_subplot()
                ax1.tick_params(axis='x', labelsize=16,direction="in")
                ax1.tick_params(axis='y', labelsize=16,direction="in")
                ax1.scatter(freq, windowdata_avg,  color=colour_list[i%16])
                ax1.set_ylabel('Signal - background (arb)', fontsize=17)
                ax1.set_xlabel('Peak 2 - peak 1 diff (MHz)', fontsize=17)
                ax1.set_title(f'Freq spectra, window {i}, time window start {time[i*windowsize_index + i]}, avg.')
                #ax1.set_ylim(0.007,0.014)
            
            
            try:
                firstindexguess = freq[np.argmax(windowdata_avg)]-140
                if firstindexguess < freq[-1]:
                    firstindexguess = freq[np.argmax(windowdata_avg)]
                    
                if HFfixed == False:
                    initialguess = [2*max(windowdata_avg)/3, max(windowdata_avg)/3, max(windowdata_avg), max(windowdata_avg), firstindexguess, firstindexguess+74,  firstindexguess+74+48,  firstindexguess+74+48+24, 40, 0]
                    
                    #fit the data- 
                    popt, pcov = scipy.optimize.curve_fit(fourlorentz, freq, windowdata_avg, p0=initialguess)
                    a,a2,a3,a4,b,b2,b3,b4,c,d= popt
                    err = np.sqrt(np.diag(pcov))
                    
                    if PlotFreqSpec == True:
                        #plot the fits of the data
                        ax1.plot(freq, fourlorentz(freq, *popt), color='k', linestyle='--')
                
                        ax1.plot(freq, lorentz(freq, a, b, c)+d, color='darkgray', linestyle='-.')
                        ax1.plot(freq, lorentz(freq, a2, b2, c)+d, color='darkgray', linestyle='-.')
                        ax1.plot(freq, lorentz(freq, a3, b3, c)+d, color='darkgray', linestyle='-.')
                        ax1.plot(freq, lorentz(freq, a4, b4, c)+d, color='darkgray', linestyle='-.')
                        #ax1.set_title(f'Window {i}: peaks at {b:.4}, {b2:.4}, {b3:.4}, {b4:.4} MHz', fontsize=16)
                        
                        ax1.set_title(f'Window {i}: spacings {b4-b3:.3}, {b3-b2:.3}, {b2-b:.3} MHz \n width: {c:.4} MHz\ntime window start {time[i*windowsize_index + i]}')
                        
                        
                else: 
                    initialguess = [2*max(windowdata_avg)/3, max(windowdata_avg)/3,  max(windowdata_avg), max(windowdata_avg), firstindexguess, 30, background]

                    popt, pcov = scipy.optimize.curve_fit(fourlorentzHF, freq, windowdata_avg, p0=initialguess)
                    a,a2,a3,a4,b,c,d = popt
                    err = np.sqrt(np.diag(pcov))
                    
                    if PlotFreqSpec == True:
                        #plot the fits of the data
                        ax1.plot(freq, fourlorentzHF(freq, *popt), color='k', linestyle='--')
                
                        ax1.plot(freq, lorentz(freq, a, b, c)+d, color='darkgray', linestyle='-.')
                        ax1.plot(freq, lorentz(freq, a2, b+74, c)+d, color='darkgray', linestyle='-.')
                        ax1.plot(freq, lorentz(freq, a3, b+48+74, c)+d, color='darkgray', linestyle='-.')
                        ax1.plot(freq, lorentz(freq, a4, b+48+74+24, c)+d, color='darkgray', linestyle='-.')
                        #ax1.set_title(f'Window {i}: peaks at {b:.4}, {b2:.4}, {b3:.4}, {b4:.4} MHz', fontsize=16)
                        
                        ax1.set_title(f'Window {i}: width: {c:.4} MHz\ntime window start {time[i*windowsize_index + i]}')
                        
                
                print(f'Window {i} width of peaks: {c:.4} MHz')
                #ax.axvline((time[(i+1)*windowsize_index + i]-time[i*windowsize_index + i])/2)
                
                #quick check that the fit is okay- ie we expect all the amplitudes to be positive
                if a > 0 and a2 > 0 and a3 > 0 and a4 > 0:
                    F1peakcentres.append(b)
                    F1peakcentres_err.append(err[4])
                    #ax.axvline(time[i*windowsize_index + i]+((time[(i+1)*windowsize_index + i]-time[i*windowsize_index + i])/2))
                    windowcentres.append(time[i*windowsize_index + i]+((time[(i+1)*windowsize_index + i]-time[i*windowsize_index + i])/2))
                    peakwidths.append(c)
                    peakwidths_err.append(err[2])
                    windownumber.append(i)
                
                if HFfixed == False:
                    #quick check that the fit is okay- ie we expect all the amplitudes to be positive
                    if a > 0 and a2 > 0 and a3 > 0 and a4 > 0:
                        spacing1.append(b2-b)
                        spacing2.append(b3-b2)
                        spacing3.append(b4-b3)
                        spacing1err.append(np.sqrt(err[1]**2 + err[5]**2))
                        spacing2err.append(np.sqrt(err[7]**2 + err[5]**2))
                        spacing3err.append(np.sqrt(err[7]**2 + err[9]**2))
                
                
            except RuntimeError:
                #print(firstindexguess)
                print(f'Lorentz fit failed: window {i}')


        print(f'Length of peak centres array: {len(F1peakcentres)}')
        print(f'Length of window centres array: {len(windowcentres)}')
        
        #plot b, the position of the first peak
        fig = plt.figure(figsize=(7,5))
        ax1 = fig.add_subplot()
        ax1.tick_params(axis='x', labelsize=16,direction="in")
        ax1.tick_params(axis='y', labelsize=16,direction="in")
        ax1.errorbar(windownumber, F1peakcentres, yerr=F1peakcentres_err, fmt='o', color=new_colour[3])
        ax1.set_xlabel('Window number', fontsize=17)
        ax1.set_ylabel('First peak centre (MHz)', fontsize=17)   
        #ax1.set_ylim(700,800)
        
        #plot c, the peak widths
        fig = plt.figure(figsize=(7,5))
        ax1 = fig.add_subplot()
        ax1.tick_params(axis='x', labelsize=16,direction="in")
        ax1.tick_params(axis='y', labelsize=16,direction="in")
        ax1.errorbar(windownumber, peakwidths, yerr=peakwidths_err, fmt='o', color=new_colour[2])
        ax1.set_xlabel('Window number', fontsize=17)
        ax1.set_ylabel('Peak widths (MHz)', fontsize=17)
        
        
        if HFfixed == False:
        #plot the peak spacings for diagnostic purposes
            fig = plt.figure(figsize=(7,5))
            ax1 = fig.add_subplot()
            ax1.tick_params(axis='x', labelsize=16,direction="in")
            ax1.tick_params(axis='y', labelsize=16,direction="in")
            ax1.errorbar(windownumber, spacing1, yerr=spacing1err, fmt='o', color=new_colour[0])
            ax1.set_xlabel('Window number', fontsize=17)
            ax1.set_ylabel('Spacing 1 (MHz)', fontsize=17)
            ax1.axhline(74, color='darkgrey')
            ax1.set_ylim(0,100)
            
            fig = plt.figure(figsize=(7,5))
            ax1 = fig.add_subplot()
            ax1.tick_params(axis='x', labelsize=16,direction="in")
            ax1.tick_params(axis='y', labelsize=16,direction="in")
            ax1.errorbar(windownumber, spacing2, yerr=spacing2err, fmt='o', color=new_colour[1])
            ax1.set_xlabel('Window number', fontsize=17)
            ax1.set_ylabel('Spacing 2 (MHz)', fontsize=17)
            ax1.axhline(48, color='darkgrey')
            ax1.set_ylim(0,100)
            
            fig = plt.figure(figsize=(7,5))
            ax1 = fig.add_subplot()
            ax1.tick_params(axis='x', labelsize=16,direction="in")
            ax1.tick_params(axis='y', labelsize=16,direction="in")
            ax1.errorbar(windownumber, spacing3, yerr=spacing3err, fmt='o', color=color_list[4])
            ax1.set_xlabel('Window number', fontsize=17)
            ax1.set_ylabel('Spacing 3 (MHz)', fontsize=17)
            ax1.axhline(24, color='darkgrey')
            ax1.set_ylim(0,100)
        
        
        return windowcentres, F1peakcentres, F1peakcentres_err
        

    #now want to actually convert this curve to a velocity profile

    def CurveToFit(self,v, a, a1):
        """This is the function that we fit the velocity curve to, from the IC 2017 paper. Only using one power of v for now, but could increase this if needed?"""
        v = np.array(v)
        return a + a1/v**1

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx



    def MakeVelocityDistribution(self,angledfilename, perpfirstpeak, perpfirstpeakerr, angledfirstpeak, angledfirstpeakerr, arrivaltimeold):
        """This function is designed to take in the perpendicular spectra data, and the data from the angled beam and generate
        a vt plot, as well as the final velocity distribution.
        Produces multiple plots: a fitted vt plot, the angled TOF data with the new time windows superimposed, 
        the many sets of fake vt data generated,and the final velocity distribution.
        Args:
            angledfilename (string): filepath of the PMT/setpoints data for the angled beam
            perpfirstpeak (float): The peak position of the F=1- peak for the perpendicular data
            perpfirstpeakerr (float): The error in the F=1- peak position for the perp data, from fit
            angledfirstpeak (list/array): The F=1- peak positions for the angled beam data
            angledfirstpeakerr (list/array): The error in the F=1- peak positions for the angled beam data, from fit
            arrivaltimeold (list/array): The central time values of the windows taken when processing the angled TOF
            
        """
        #first, convert the frequency values to a mean forward velocity
        resfreqPERP = 494432.13*10**3 #in MHz
        meanvelocityold = []
        #print(perpfirstpeak)
        
        for i in range(len(angledfirstpeak)):
            v= c*np.cos(np.pi/4)*(-angledfirstpeak[i]+perpfirstpeak)/resfreqPERP
            meanvelocityold.append(v)
            #print(angledfirstpeak[i], v, arrivaltimeold[i])
            
            
        #doing some error propagation, lets hope im doing it okay
        velocity_errold = (c*np.cos(np.pi/4)/resfreqPERP)*np.sqrt(np.array(angledfirstpeakerr)**2 + perpfirstpeakerr**2)
            

        #access the unprocessed data for the angled run
        avgp2diff, avgdata, title = UnpickleUnprocessedData(angledfilename)
        
        print('Making velocity distribution...')
        fig = plt.figure(figsize=(7,5))
        ax = fig.add_subplot()
        ax.tick_params(axis='x', labelsize=16,direction="in")
        ax.tick_params(axis='y', labelsize=16,direction="in")
        ax.set_ylabel('Arrival time (ms)', fontsize=17)
        ax.set_xlabel('Mean velocity (m/s)', fontsize=17)
        #ax.errorbar(meanvelocityold[7:], arrivaltimeold[7:], xerr= velocity_errold[7:], fmt='o', color=colour_list[3], markersize='3')
        ax.set_xlim(100,180)
        
        #print(len(meanvelocity))
        
        meanvelocity = []
        arrivaltime = []
        velocity_err = []
        #remove the data points that have a really large error to stop them skewing the fit
        for i in range(len(meanvelocityold)):
            if velocity_errold[i] < 5:
                meanvelocity.append(meanvelocityold[i])
                velocity_err.append(velocity_errold[i])
                arrivaltime.append(arrivaltimeold[i])
                
            
        #sort the data points so they're in order of ascending mean velocity
        meanv_sorted, arrivalt_sorted = map(list, zip(*sorted(zip(meanvelocity[7:], arrivaltime[7:]), key = lambda x: x[0])))
        meanv_sorted, meanverr_sorted = map(list, zip(*sorted(zip(meanvelocity[7:], velocity_err[7:]), key = lambda x: x[0])))
        

        ax.errorbar(meanv_sorted, arrivalt_sorted, xerr= meanverr_sorted, fmt='o', color=colour_list[5], markersize='3')
        
        #np.save('vforvtcurve.npy', meanv_sorted)
        #np.save('tforvtcurve.npy', arrivalt_sorted)
        #np.save('errforvtcurve.npy', meanverr_sorted)
            
        initialguess = [[-0.9, 400]]

        #ax.plot(meanv_sorted, -0.9 + 400/np.array(meanv_sorted))
        
        #fit the sorted data to the curve function above
        popt, pcov = scipy.optimize.curve_fit(CurveToFit, meanv_sorted, arrivalt_sorted, p0=initialguess)
        a,a1= popt
        err = np.sqrt(np.diag(pcov))
        
        ax.plot(meanv_sorted, CurveToFit(meanv_sorted, *popt), color='k', linestyle='--')
        #ax.set_title(f'Fit parameters: {a:.4} +/- {err[0]:.4}, {a1:.4} +/- {err[1]:.4}', fontsize=17)
        
        
        
        #TOF profile 
        buff_length = range(16384)
        dec = 32
        rate = 125*10**6/dec
        time = [x / rate *10**3 for x in buff_length]
        
        #use from 1000 on to remove the YAG peak
        TOFdata = np.mean(avgdata,axis=0)[1000:] 
        background = np.mean(np.mean(avgdata,axis=0)[1000:][0:1000])
        print(background)
        TOFdata = TOFdata- 0.00131#0.00794  # this bit is an attempt to remove the background- printed out from last time we fitted a gaussian to this data #np.mean(TOFdata[0:-100])
        timeaxis = time[1000:]
        
        #print(list(TOFdata))
        
        fig = plt.figure(figsize=(7,5))
        ax = fig.add_subplot()
        ax.tick_params(axis='x', labelsize=16,direction="in")
        ax.tick_params(axis='y', labelsize=16,direction="in")
        ax.set_ylabel('Signal (arb)', fontsize=17)
        ax.set_xlabel('Time (ms)', fontsize=17)
        
        ax.scatter(timeaxis, TOFdata, color=new_colour[1], s=3)
        
        
        #fitting the TOF profile to a gaussian so we have something to integrate under
        initialguess = [0.004, 1.9, 0.05, 0.005]
        #try:
        poptTOF, pcovTOF = scipy.optimize.curve_fit(gaussian, timeaxis, TOFdata, p0=initialguess)
        aTOF, bTOF, cTOF, dTOF = poptTOF
        errTOF = np.sqrt(np.diag(pcovTOF))
            
        ax.plot(timeaxis, gaussian(timeaxis, *poptTOF), color='k', linestyle = '--')
        
        signal = []
        sizeofvwindow = 2
        
        
        ax.set_title(f'Visualising time windows that correspond to  {sizeofvwindow} m/s\n' + title, fontsize=17)
        
        #go through and find the ts that link to the vs
        testv = range(int(min(meanv_sorted)), int(max(meanv_sorted)), sizeofvwindow)
        print(f'min, max velocity: {int(min(meanv_sorted))}, {int(max(meanv_sorted))} m/s')
        testv = range(100, 250, sizeofvwindow)
        for i in range(len(testv)):
            lowert = CurveToFit(testv[i]+sizeofvwindow, *popt)
            highert = CurveToFit(testv[i]-sizeofvwindow, *popt)
            
            #print(lowert, highert)
            #plot the t windows on the TOF profile for sanity checking purposes
            ax.axvline(lowert, color=color_list[i%16])
            ax.axvline(highert, color=color_list[i%16])
            
            #find our 'signal' for this t window by integrating the gaussian between t1 and t2
            indlowest = find_nearest(timeaxis, lowert)
            indhighest = find_nearest(timeaxis, highert)
            intsignal = np.trapz(TOFdata[indlowest:indhighest+1], timeaxis[indlowest:indhighest+1])
            
            
            #print(intsignal)
            #intsignal = integrate.quad(gaussian, lowert, highert, args=(aTOF, bTOF, cTOF, dTOF))
            #signal.append(intsignal[0])
            signal.append(intsignal)
            
        #print(np.shape(testv))
        #print(np.shape(signal))
        
        
        
        #okay, now we're doing some confidence intervals! Follow method in 2017 Truppe paper like the rest of this
        
        #to start, for each point in vt curve we want to generate some new v values from a normal dist
        numberoffakevtcurves = 400 #this is the number to generate
        print(f'For confidence intervals, generating {numberoffakevtcurves} fake datasets...')
        
        
        varray = np.zeros([len(meanv_sorted), numberoffakevtcurves])
        fitparams = np.zeros([numberoffakevtcurves, 2])
        
        
        for i in range(len(meanv_sorted)):
            varray[i] = np.random.normal(meanv_sorted[i], meanverr_sorted[i], numberoffakevtcurves)
            

        flipvarray = varray.transpose() #this is now 400 v data sets, that can produce 400 vt curves

        #for visualisation purposes:
        fig = plt.figure(figsize=(7,5))
        ax = fig.add_subplot()
        ax.tick_params(axis='x', labelsize=16,direction="in")
        ax.tick_params(axis='y', labelsize=16,direction="in")
        ax.set_ylabel('Arrival time (ms)', fontsize=17)
        ax.set_xlabel('Mean velocity (m/s)', fontsize=17)
        ax.set_title('The fake datasets used for confidence intervals', fontsize=17)
        for i in range(numberoffakevtcurves):
            #for visualisation purposes:
            ax.scatter(flipvarray[i], arrivalt_sorted, s=3, alpha=0.5)
        
            initialguess = [[-0.9, 400]]

            #THIS BIT IS IMPORTANT
            #fit the 'fake' vt curves and extract the parameters
            popt, pcov = scipy.optimize.curve_fit(CurveToFit, flipvarray[i], arrivalt_sorted, p0=initialguess)
            a,a1= popt
            fitparams[i] = popt
            
            ax.plot(flipvarray, CurveToFit(flipvarray, *popt))
        
        
        #then for each of these sets of parameters (ie each 'fake' vt curve), find the equivalent v distribution
        
        fakesignal = np.zeros([numberoffakevtcurves, len(testv)])
        #go through and find the ts that link to the vs
        for n in range(numberoffakevtcurves):
            testsignal = []
            for i in range(len(testv)):
                lowert = CurveToFit(testv[i]+1, *fitparams[n])
                highert = CurveToFit(testv[i]-1, *fitparams[n])
        
                #find our 'signal' for this t window by integrating the gaussian between t1 and t2
                #intsignal = integrate.quad(gaussian, lowert, highert, args=(aTOF, bTOF, cTOF, dTOF))
                #intsignal = np.trapz(backgroundfreedata[1000:-5000], time[1000:-5000])
                #print(intsignal)
                
                indlowest = find_nearest(timeaxis, lowert)
                indhighest = find_nearest(timeaxis, highert)
                intsignal = np.trapz(TOFdata[indlowest:indhighest+1], timeaxis[indlowest:indhighest+1])
                
                
                #testsignal.append(intsignal[0])
                testsignal.append(intsignal)
            fakesignal[n] = testsignal
        
        
        #print(np.shape(fakesignal))
        
        meanvelocity = np.mean(fakesignal, axis=0)
        
            
        fig = plt.figure(figsize=(7,5))
        ax = fig.add_subplot()
        ax.tick_params(axis='x', labelsize=16,direction="in")
        ax.tick_params(axis='y', labelsize=16,direction="in")
        ax.set_ylabel('Normalised signal (arb)', fontsize=17)
        ax.set_xlabel('Velocity (m/s)', fontsize=17)
        #the original method:
        #ax.plot(testv, np.array(signal)/max(signal), color = 'k', linestyle='--')
        #the average of the fake profile:
        ax.plot(testv, meanvelocity/max(signal), color = QLMred)
        
        lowerbound = []
        upperbound = []
        
        #for testing purposes: 
        #for i in range(numberoffakevtcurves):
        #    ax.plot(testv, np.array(fakesignal[i])/max(fakesignal[i]))
            
        fakesignal = fakesignal/max(signal)
        #generate the 68% intervals
        for i in range(len(testv)):
            upperbound.append(np.percentile(fakesignal.transpose()[i], 84))
            lowerbound.append(np.percentile(fakesignal.transpose()[i], 16))
        
        ax.fill_between(testv, lowerbound, upperbound, color=QLMred, alpha= 0.5)

        #for testing purposes - plots an example of a hist for one of the data points (ie hist of the 400 points for one v value)
        #plus the mean and 68% intervals so you can see if they look alright
        #fig = plt.figure(figsize=(7,5))
        #ax = fig.add_subplot()
        #ax.tick_params(axis='x', labelsize=16,direction="in")
        #ax.tick_params(axis='y', labelsize=16,direction="in")
        #ax.hist(fakesignal.transpose()[20])
        #ax.axvline(meanvelocity[20], color='k')

        #ax.axvline(np.percentile(fakesignal.transpose()[20], 16), color='k')
        #ax.axvline(np.percentile(fakesignal.transpose()[20], 84), color='k')
        #np.save('vforvdist.npy', testv)
        #np.save('signalforvdist.npy', np.array(signal)/max(signal))
        #print(list(signal))
        
        #np.save('lowerboundforvdist.npy', lowerbound)
        #np.save('upperboundforvdist.npy', upperbound)
        #print(list(signal))
        
        
            
    def GenerateVelocityDistribution(self,filepathperp, perpdatatype, perpinitialguess, perpcutoff, perpforceHF, filepathangled, windowsize, starttime, endtime, PlotFreqSpec, HFfixedangle):
        """This function looks in the folders provided to find the processed data and then processes it to generate
        a velocity distribution. If you're trying to generate a v distribution from data which has yet to be processed, 
        I think it should kick up errors. Generated many plots for diagnostics!
        Args:
            filepathperp (string): Folder that contains the processed data for the perpendicular beam
            perpdatatype (string): 'amp', 'quad' or 'trapz'. The type of data to use when plotting the perpendicular data
            perpinitialguess (array): array of initial guess parameters for the perpendicular lorentzian fit
            perpcutoff (float): cutoff (float): this is the y (signal) value above which you don't want to consider 
                            points. Essentially there to help remove points from anomalous gaussian fits which could 
                            affect the lorentzian fit.
            perpforceHF (boolean): if True, this will fit the spectra with lorentzians fixed at 74, 48 and 24 MHz spacings. 
                                If not, the spacings will be a free parameter in the fit.
            filepathangled (string): Folder that contains the processed data for the angled beam.
            windowsize (float): Size of the windows in ms.
            starttime (float): Desired start time to begin taking windows (ie about the start of the TOF hump, so we're
                            actually looking at a time with molecules).
            endtime (float): Desired start time to stop taking windows (ie about the end of the TOF hump, so we're
                            only looking at times with molecules).
            PlotFreqSpec (bool): if True, will plot the frequency spectrum for each time window. Good for visual diagnostics
            HFfixedangle (bool): if True, will fit the angled window data frequency spectra with the peak spacings fixed. 
                                Otherwise, these spacings will be free fit params.

        """
        #assume that we've already created the processed data files for the angled and perp data
        
        #produce the perpendicular spectrum and extract the F=1- peak position, to use as the reference point
        print('Generating perpendicular spectrum...')
        perpfirstpeak, perpfirstpeakerr = FitDataToLorentzians(filepathperp, perpdatatype, perpinitialguess, perpcutoff, perpforceHF, True, True)

        #split angled TOF into windows, extract the central times of the windows, and the F=1- peak positions for each window (plus their errors)
        arrivaltime, angledfirstpeak, angledfirstpeakerr = GenerateFrequencySpectra(filepathangled, windowsize, starttime, endtime, PlotFreqSpec, HFfixedangle)

        #generate the vt curve
        MakeVelocityDistribution(filepathangled, perpfirstpeak, perpfirstpeakerr, angledfirstpeak, angledfirstpeakerr, arrivaltime)




    

    def load_data(self):
        npy_files = [f for f in os.listdir(self.run_folder) if f.endswith(".npy") and "_run_PMT_" in f]
        if not npy_files:
            raise FileNotFoundError(f"No matching .npy files found in {self.run_folder}")
        data_path = os.path.join(self.run_folder, npy_files[0])
        return np.load(data_path)

    def compute_time_axis(self):
        buff_length = range(16384)
        rate = self.sampling_rate / self.decimation
        time = np.array([x / rate * 1e3 for x in buff_length])  # ms
        return time

    def smooth_data(self, data):
        return savgol_filter(data, window_length=self.window_length, polyorder=self.polyorder)

    def find_peaks(self, data):
        peaks, properties = find_peaks(
            data,
            height=self.peak_height,
            distance=self.peak_distance,
            prominence=self.peak_prominence
        )
        return peaks

    def plot(self, time, smoothed_data, peaks, raw_data):
        plt.figure(figsize=(12, 6))
        plt.plot(time, smoothed_data, label="Smoothed Data", color='black')
        plt.plot(time[peaks], smoothed_data[peaks], "ro", label="Peaks")
        plt.scatter(time, raw_data, marker='o', label="Raw Data", s=10, alpha=0.3)
        plt.xlabel("Time (ms)")
        plt.ylabel("Signal (a.u.)")
        plt.title("TOF Signal with Peaks")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def averageTOF(self):
        data = self.load_data()
        time = self.compute_time_axis()
        raw_data = data[self.buffer:]
        time = time[self.buffer:]

        smoothed_data = self.smooth_data(raw_data)
        peaks = self.find_peaks(smoothed_data)
        tof_times = time[peaks]

        if self.show_plot:
            self.plot(time, smoothed_data, peaks, raw_data)

        if self.return_peaks:
            return np.round(tof_times, 3)
        else:
            print("TOF peak times (ms):", np.round(tof_times, 3))
