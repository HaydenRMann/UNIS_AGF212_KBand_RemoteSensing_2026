




'''
Imports
'''

# Main classes for the Ethernet interface
from Interfaces.Ethernet.EthernetConfig import EthernetParams
from Interfaces.Ethernet.IPConnection import IPConnection
from Interfaces.Ethernet.Commands import IPCommands

# Parameter and data classes
import ConfigClasses as cfgCl

# To create a simple plot
import matplotlib.pyplot as plt

import numpy as np
import pickle

from time import time, sleep
from datetime import datetime, timedelta
from scipy.signal import find_peaks

class Main():
    def __init__(self):
        
        # initialize needed parameters classes
        self.hwParams = cfgCl.HwParams()
        self.sysParams = cfgCl.SysParams()
        self.htParams = cfgCl.HtParams()
        
        # initialize needed data classes
        self.FD_Data = cfgCl.FD_Data()
        self.TD_Data = cfgCl.TD_Data()
        self.HT_Targets = cfgCl.HtTargets()
        
        # load the Ethernet parameters and change them
        self.etherParams = EthernetParams()
        self.etherParams.ip = "192.168.0.2" #default radar IP
        self.etherParams.port = 1024
        
        self.myInterface = None
        self.connected = False
        self.error = False
        
        
    '--------------------------------------------------------------------------------------------'
    # function to connect to a specified interface
    def Connect(self):
        
        print('========================')
        print('Connect')

        self.myInterface = IPConnection(self)
        
        # try to connect
        if not self.myInterface.connect():
            print("Connection to "+self.etherParams.ip+":"+str(self.etherParams.port)+" failed.")
            self.error = True
            return
        
        # if the connection has been established, load the command class
        self.cmd = IPCommands(connection=self.myInterface, main_win=self)
        self.connected = True
            
    '--------------------------------------------------------------------------------------------'
    # function to get the Radar specific parameters
    def GetHwParams(self):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return
        
        print('========================')
        print('GetHwParams')
        
        # execute the respective command ID
        try:
            self.cmd.execute_cmd("CMDID_SEND_INFO")
        except:
            print("Error in receiving hardware parameters.")
            self.error = True
            return
        
        # if no error occurred, the received data can be found in hwParams
        
    '--------------------------------------------------------------------------------------------'
    # function to get the Radar system parameters
    def GetSysParams(self):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return
        
        print('========================')
        print('GetSysParams')
        
        # execute the respective command ID
        try:
            self.cmd.execute_cmd("CMDID_SEND_PARAMS")
        except:
            print("Error in receiving system parameters.")
            self.error = True
            return
        
        # if no error occurred, the received data can be found in sysParams
        
    '--------------------------------------------------------------------------------------------'
    # function to set the Radar system parameters
    def SetSysParams(self):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return
        
        print('========================')
        print('SetSysParams')
        
        # execute the respective command ID
        try:
            self.cmd.execute_cmd("CMDID_SETUP")
        except:
            print("Error in setting system parameters.")
            self.error = True
            return
            
    '--------------------------------------------------------------------------------------------'    
    # function to get frequency domain data with or without a previous measurement
    # the parameter 'measurement' specifies the type of measurement    
    # possible values are: "UP-Ramp", "DOWN-Ramp", "CW" or "None"
    def GetFdData(self, measurement="UP-Ramp"):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return
        
        print('========================')
        print('GetFdData')
        
        # execute the respective command ID
        try:
            if measurement == "UP-Ramp":
                self.cmd.execute_cmd("CMDID_UP_RMP_FD")                
            elif measurement == "DOWN-Ramp":
                self.cmd.execute_cmd("CMDID_DN_RMP_FD")
            elif measurement == "CW":
                self.cmd.execute_cmd("CMDID_GP_FD")
            elif measurement == None or measurement == "None":
                self.cmd.execute_cmd("CMDID_FDATA")
            else:
                print("No valid measurement type.")
                self.error = True
                return
            
        except:
            print("Error in receiving frequency domain data.")
            self.error = True
            return
        
        # the received data can be found in FD_Data
        
    '--------------------------------------------------------------------------------------------'
    # function to get time domain data with or without a previous measurement
    # the parameter 'measurement' specifies the type of measurement    
    # possible values are: "UP-Ramp", "DOWN-Ramp", "CW" or "None"
    def GetTdData(self, measurement="UP-Ramp"):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return
        
        print('========================')
        print('GetTdData')

        # execute the respective command ID
        try:
            if measurement == "UP-Ramp":
                self.cmd.execute_cmd("CMDID_UP_RMP_TD")                
            elif measurement == "DOWN-Ramp":
                self.cmd.execute_cmd("CMDID_DN_RMP_TD")
            elif measurement == "CW":
                self.cmd.execute_cmd("CMDID_GP_TD")
            elif measurement == None or measurement == "None":
                self.cmd.execute_cmd("CMDID_TDATA")
            else:
                print("No valid measurement type.")
                self.error = True
                return
            
        except:
            print("Error in receiving time domain data.")
            self.error = True
            return
        
        # the received data can be found in TD_Data
        
    '--------------------------------------------------------------------------------------------'
    # function to get the Human Tracker parameters
    def GetHtParams(self):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return
        
        print('========================')
        print('GetHtParams')

        # execute the respective command ID
        try:
            self.cmd.execute_cmd("CMDID_SEND_HT_PARAMS")
        except:
            print("Error in receiving Human Tracker parameters.")
            self.error = True
            return
        
        # the received parameters can be found in htParams
        
    '--------------------------------------------------------------------------------------------'
    # function to set the Human Tracker parameters
    # Note that the Radar Module will perform some initial measurements, so it will be waited some time
    def SetHtParams(self):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return
        
        print('========================')
        print('SetHtParams')

        # execute the respective command ID
        try:
            self.cmd.execute_cmd("CMDID_HT_PARAMS")            
        except:
            print("Error in setting Human Tracker parameters.")
            self.error = True
            return
    
    '--------------------------------------------------------------------------------------------'
    # function that triggers a Human Tracker measurement
    def HtMeasurement(self):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return
        
        print('========================')
        print('HtMeasurement')

        # execute the respective command ID
        try:
            self.cmd.execute_cmd("CMDID_DO_HT")            
        except:
            print("Error in receiving Human Tracker data.")
            self.error = True
            return
        
        # the received data can be found in HT_Targets
    
    '--------------------------------------------------------------------------------------------'
    # function to disconnect the connected interface
    def Disconnect(self):
        # do nothing if not connected
        if not self.connected:
            return
    
        print('========================')
        print('Disconnect')
        
        self.myInterface.disconnect()
            
        self.connected = False

        '--------------------------------------------------------------------------------------------'

    
    def UnlockFullBand(self):
        # do nothing if not connected or an error has occurred
        if not self.connected or self.error:
            return


        # self.cmd.execute_cmd("CMDID_UNLOCK_FULL_BAND")

        # execute the respective command ID
        try:
            self.cmd.execute_cmd("CMDID_UNLOCK_FULL_BAND")
            print("Full band unlocked")

        except:
            print("Error in unlocking full band")
            self.error = True
            return

        # if no error occurred, full band is unlocked



            
'=================================================================================================='




def ReadFile(filename):

    # Load sys params
    with open('storage/'+filename+'/sysParams.pkl', 'rb') as inp:
        sysParams = pickle.load(inp, encoding='latin1')

    print(('Bandwidth',sysParams.manualBW))

    # Init variables
    I1 = []
    Q1 = []
    I2 = []
    Q2 = []
    Combined = []
    slowtime = []
    gps = []

    # Load radar object
    objs = []
    with open('storage/'+filename+'/data.pkl', 'rb') as inp:

        while 1:
            try:
                FD_Data = pickle.load(inp)

                mag_data = []
                if sysParams.FFT_data_type == 0:  # only magnitudes were transmitted
                    mag_data = FD_Data.data

                if sysParams.FFT_data_type == 2:  # real/imaginary
                    comp_data = [complex(float(FD_Data.data[n]), float(FD_Data.data[n + 1])) for n in
                                 range(0, len(FD_Data.data), 2)]
                    mag_data = np.abs(comp_data)

                if sysParams.FFT_data_type == 1 or sysParams.FFT_data_type == 3:  # magnitudes/phase or magnitudes/object angle
                    mag_data = [FD_Data.data[n] for n in range(0, len(FD_Data.data), 2)]

                # Convert to dBm
                min_dbm = -60  # [dBm]
                for n in range(len(mag_data)):
                    try:
                        mag_data[n] = 20*np.log10(mag_data[n]/2.**21)
                    except:
                        mag_data[n] = min_dbm

                # Sort for active channels
                fd_data = []
                n = 0
                for ch in range(4):  # maximum possible channels = 4
                    if sysParams.active_RX_ch & (1 << ch):
                        ind1 = n * FD_Data.nSamples
                        ind2 = ind1 + FD_Data.nSamples
                        n += 1
                        fd_data.append(mag_data[ind1:ind2])
                    else:
                        fd_data.append([0] * FD_Data.nSamples)

                I1.append(fd_data[0])
                Q1.append(fd_data[1])
                I2.append(fd_data[2])
                Q2.append(fd_data[3])
                slowtime.append(FD_Data.time0/1000)
                try:
                    gps.append(FD_Data.gps_fix)
                except:
                    pass

                # Generate x-axis data, here the distance in [m]
                x_data = [sysParams.tic * n / sysParams.zero_pad / 1.0e6 for n in range(FD_Data.nSamples)]

            except EOFError:
                break
                
        data = dict()
        data['Q1'] = np.array(Q1)
        data['Q2'] = np.array(Q2)
        data['I1'] = np.array(I1)
        data['I2'] = np.array(I2)
        data['x'] = np.array(x_data)
        data['sky_calibrated'] = False
        data['slowtime'] = np.array(slowtime)
        data['filename'] = filename
        data['gps'] = gps
        #data['start_time'] = datetime(1970,1,1) + timedelta(seconds=sysParams.start_time)
        return(data)


def Combine_channels(data):
    if data['sky_calibrated']:
        Q1 = (10**((data['Q1_calibrated']/20)))*(2**21)
        Q2 = (10**((data['Q2_calibrated']/20)))*(2**21)
        I1 = (10**((data['I1_calibrated']/20)))*(2**21)
        I2 = (10**((data['I2_calibrated']/20)))*(2**21)
    else:
        Q1 = (10**((data['Q1']/20)))*(2**21)
        Q2 = (10**((data['Q2']/20)))*(2**21)
        I1 = (10**((data['I1']/20)))*(2**21)
        I2 = (10**((data['I2']/20)))*(2**21)

    data['combined_amplitude_lin'] = ((np.sqrt((Q1**2)+(I1**2))) + (np.sqrt((Q2**2)+(I2**2)))) / 2
    data['combined_amplitude_log'] = 10*np.log10(data['combined_amplitude_lin']/(2**21))
    data['combined_power_lin'] = (((Q1**2)+(I1**2)) + ((Q2**2)+(I2**2))) / 2
    data['combined_power_log'] = 10*np.log10(data['combined_power_lin']/(2**42))

    return(data)


    
def SkyCalibration(SKY, data):
        
    data['vec_cal_Q1'] = np.mean(SKY['Q1'],0)
    data['vec_cal_I1'] = np.mean(SKY['I1'],0)
    data['vec_cal_Q2'] = np.mean(SKY['Q2'],0)
    data['vec_cal_I2'] = np.mean(SKY['I2'],0)
    num_measurements = np.shape(np.array(data['Q1']))[0]
        
    Q1_list = list()
    Q2_list = list()
    I1_list = list()
    I2_list = list()
        
    for n in np.arange(num_measurements):
        Q1_list.append(data['vec_cal_Q1'])
        Q2_list.append(data['vec_cal_Q2'])
        I1_list.append(data['vec_cal_I1'])
        I2_list.append(data['vec_cal_I2'])

    min_dbm = -60  # [dBm]
    diff_linear = (((10**(data['Q1']/20))*(2.**21)) - ((10**(np.array(Q1_list)/20))*(2.**21)))
    diff_linear[diff_linear<0] = ((10**(min_dbm/20))*(2.**21))
    data['Q1_calibrated'] = 20*np.log10(diff_linear/2.**21)
    #data['Q1_calibrated'] = data['Q1'] - np.array(Q1_list)
    diff_linear = (((10**(data['Q2']/20))*(2.**21)) - ((10**(np.array(Q2_list)/20))*(2.**21)))
    diff_linear[diff_linear<0] = ((10**(min_dbm/20))*(2.**21))
    data['Q2_calibrated'] = 20*np.log10(diff_linear/2.**21)
    #data['Q2_calibrated'] = data['Q2'] - np.array(Q2_list)
    diff_linear = (((10**(data['I1']/20))*(2.**21)) - ((10**(np.array(I1_list)/20))*(2.**21)))
    diff_linear[diff_linear<0] = ((10**(min_dbm/20))*(2.**21))
    data['I1_calibrated'] = 20*np.log10(diff_linear/2.**21)
    #data['I1_calibrated'] = data['I1'] - np.array(I1_list)
    diff_linear = (((10**(data['I2']/20))*(2.**21)) - ((10**(np.array(I2_list)/20))*(2.**21)))
    diff_linear[diff_linear<0] = ((10**(min_dbm/20))*(2.**21))
    data['I2_calibrated'] = 20*np.log10(diff_linear/2.**21)
    #data['I2_calibrated'] = data['I2'] - np.array(I2_list)
    data['sky_calibrated'] = True
        
    return data


def PlotChannel(data, str_channel):
    
    mtx_data = data[str_channel]
    slowtime = data['slowtime']
    x_data = data['x']
    
    plt.imshow(np.transpose(mtx_data),extent=[slowtime[0]-slowtime[0],slowtime[len(slowtime)-1]-slowtime[0],x_data[len(x_data)-1],x_data[0]],origin='upper', interpolation='nearest')

    plt.xlabel('Time since start [s]')
    plt.ylabel('Distance from radar [m]')

    plt.show()


def PlotNormalize(data, str_channel, max_range):
    channel_data = data[str_channel]#(10**(data[str_channel]/20))*(2.**21)
    slowtime = data['slowtime']
    x_data = data['x']
    ind = x_data <= max_range
   # print(len(x_data))
    x_data = x_data[ind]
    #print(np.shape(channel_data))
    #print(len(x_data))

    max_value = np.max(channel_data, axis=1)
    #print(len(max_value))
    channel_data = np.transpose(channel_data)/max_value

    plt.imshow(channel_data[ind][:],extent=[slowtime[0]-slowtime[0],slowtime[len(slowtime)-1]-slowtime[0],x_data[len(x_data)-1],x_data[0]],origin='upper', interpolation='nearest', clim=[0,1], aspect='auto')


def Correct_speed(data, height_radar, c_snow):
    x_data = data['x']
    c_air = 3*(10**8) #m/s
    x_data_surface = x_data[np.argmin(abs(x_data-height_radar))]
    x_data[x_data>height_radar] = ((x_data[x_data>height_radar] - x_data_surface)*(c_snow/c_air)) + x_data_surface
    data['x_corr'] = np.array(x_data)
    #print('Q1')
    return data

"""
def Peakfinder(data, str_channel, thres):
    channel_data = data[str_channel]
    x_data = data['x']

    height_idx = np.array([])

    for n_measurement in range(np.shape(channel_data)[0]):
        time_data = channel_data[n_measurement][:]
        np.append(height_idx, find_peaks(time_data, thres),1)

    return(height_idx)
"""


def MeanEchoes(data, str_channel):
    vec_mean = np.mean(data[str_channel],0)
    return vec_mean



#data = ReadFile('26_02_2026_1')
