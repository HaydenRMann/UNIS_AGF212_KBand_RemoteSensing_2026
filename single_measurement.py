'''
Imports
'''

import radar
import matplotlib.pyplot as plt

import numpy as np
from time import time, sleep


'''
/// Main Part ///

In the following it is shown how the Main class is used to connect a Radar
Module and to read/change some parameters.  
Later one of three examples can be chosen by setting the "if 0:" to "if 1:".
These examples are using some of the Main class functions to read measurement 
data and to plot it. 
'''
                
# Get an instance of the main class
main = radar.Main()

# Specify your interface and try to connect it.
main.Connect()

if main.connected:


    # Read some Radar Module specific parameters
    main.GetHwParams()

    # These parameters can be accessed by e.g. main.hwParams.radarNumber
    print("Number of the connected Radar Module: ", main.hwParams.radarNumber)


    # Change some of the system parameters, e.g.
    main.sysParams.minFreq = 23500
    main.sysParams.manualBW = 2500
    main.sysParams.t_ramp = 1
    main.sysParams.active_RX_ch = 15
    main.sysParams.freq_points = 150


    # Check if the frontend is off
    if main.sysParams.frontendEn == 0:
        main.sysParams.frontendEn = 1   # turns it on

    # Unlock full band
    # key = 0xCFA4A24C756E
    main.sysParams.key = [np.uint16(0xCFA4),np.uint16(0xA24C),np.uint16(0x756E)]
    main.UnlockFullBand()


        
    # Send the changed parameters to the Radar Module
#    main.cmd.execute_cmd("CMDID_UNLOCK_FULL_BAND")
    main.SetSysParams()

    # Always read back the system parameters because some read only parameters changed
    main.GetSysParams()
    # Verify that the parameters have changed
    print("Frequency [MHz]: ", main.sysParams.minFreq)
    print("Bandwidth [MHz]: ", main.sysParams.manualBW)
    print("Ramp-time [ms]: ", main.sysParams.t_ramp)        
    print("")




    # Specify a measurement type, let the Radar perform it and read the data
    measurement = "UP-Ramp"
    print('Measuring!')


    # Check if the frontend is off
    if main.sysParams.frontendEn == 0:
        main.sysParams.frontendEn = 1   # turns it on

    main.GetFdData(measurement) #Make the measurement!

    main.sysParams.frontendEn = 0 #Turn off the radar!
    


    
    # Plot the measured data dependent on the activated channels
    # Only magnitude data will be plotted
    mag_data = []

    if main.sysParams.FFT_data_type == 0:   # only magnitudes were transmitted
        mag_data = main.FD_Data.data

    if main.sysParams.FFT_data_type == 2:   # real/imaginary 
        comp_data = [complex(float(main.FD_Data.data[n]), float(main.FD_Data.data[n+1])) for n in range(0, len(main.FD_Data.data), 2)]
        mag_data = np.abs(comp_data)

    if main.sysParams.FFT_data_type == 1 or main.sysParams.FFT_data_type == 3:      # magnitudes/phase or magnitudes/object angle
        mag_data = [main.FD_Data.data[n] for n in range(0, len(main.FD_Data.data), 2)]

    # Convert to dBm
    min_dbm = -60   # [dBm]
    for n in range(len(mag_data)):
        try:
            mag_data[n] = 20*np.log10(mag_data[n]/2.**21)
        except:
            mag_data[n] = min_dbm

    # Sort for active channels
    fd_data = []
    n = 0
    for ch in range(4):     # maximum possible channels = 4
        if main.sysParams.active_RX_ch & (1<<ch):
            ind1 = n * main.FD_Data.nSamples
            ind2 = ind1 + main.FD_Data.nSamples
            n += 1
            fd_data.append(mag_data[ind1:ind2])
        else:
            fd_data.append([0]*main.FD_Data.nSamples)   

    # Generate x-axis data, here the distance in [m] 
    x_data = [main.sysParams.tic*n/main.sysParams.zero_pad/1.0e6 for n in range(main.FD_Data.nSamples)]

    # Add the data as lines to the plot
    plt.plot(x_data, fd_data[0], 'b',  
             x_data, fd_data[1], 'g',
             x_data, fd_data[2], 'c',
             x_data, fd_data[3], 'm')
    plt.grid(True)
    plt.title("Frequency domain data plot")
    plt.xlabel("Distance [m]")
    plt.ylabel("Magnitude [dBm]")
    plt.show()

else:
    print('No radar connected! Check cables / network IP and interface etc!')


print('All done, disconnecting radar!')
main.Disconnect()
