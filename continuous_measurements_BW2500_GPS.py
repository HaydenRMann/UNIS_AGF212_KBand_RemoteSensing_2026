'''
Imports
'''

import radar
import time
import os
import subprocess
import select
import pickle
import radar
import gps

import numpy as np


# measurement settings
plot_every = 200


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

subprocess.run(["ubxtool", "-p", "RESET"]) 

#create gpsd interface
session = gps.gps(mode=gps.WATCH_ENABLE)

gps_not_ok = True

print("Looking for GPS!")
while (session.read() == 0 & gps_not_ok) :
    if (gps.isfinite(session.fix.latitude) & (session.fix.latitude>70)): #USE ONLY FOR SVALBARD!!!
        gps_fix = session.fix
        print("GPS alive and sane (we are on Svalbard)! WILL NOT START WITHOUT IT!!!")
        gps_not_ok = False
        break

# init measurement number for today. Will be adjusted if any already exist
measnr = 1


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
    main.SetSysParams()

    # Always read back the system parameters because some read only parameters changed
    main.GetSysParams()
    # Verify that the parameters have changed
    print("Frequency [MHz]: ", main.sysParams.minFreq)
    print("Bandwidth [MHz]: ", main.sysParams.manualBW)
    print("Ramp-time [ms]: ", main.sysParams.t_ramp)        
    print("")


    # Check if the frontend is off
    if main.sysParams.frontendEn == 0:
        main.sysParams.frontendEn = 1   # turns it on

    # Specify a measurement type, let the Radar perform it and read the data
    measurement = "UP-Ramp"
    print('Measuring!')

    if True:
        # Starting looping measurement

        # set start time

        main.SetSysParams()
        main.GetSysParams()

        print('Starting measurement!')

        # Save sys params
        with open('data/sysParams.pkl', 'wb') as sysout:
            pickle.dump(main.sysParams, sysout, pickle.HIGHEST_PROTOCOL)
        # Save hw params
        with open('data/hwParams.pkl', 'wb') as hwout:
            pickle.dump(main.hwParams, hwout, pickle.HIGHEST_PROTOCOL)

        # Save a rolling "last frame" file
        with open('data/latest.pkl', 'wb') as last_out:
            pickle.dump(main.FD_Data, last_out, pickle.HIGHEST_PROTOCOL)

#        gpsout = open('data/gps.pkl','wb')

            
        # Loop measurement and check Run condition
        with open('data/data.pkl', 'ab+') as dataout:
            counter = 0 
            start_time = time.time()
    
            try:
            
                while True:

                    if session.read() == 0:
                        if (gps.MODE_SET & session.valid):
                            gps_fix = session.fix

                    
                    
                    if main.connected:
                        # specify a measurement type, let the Radar perform it and read the data
                        measurement = "UP-Ramp"
                        main.GetFdData(measurement)
                        print("GPS " + "Lat: " + str(gps_fix.latitude) + " Lon: " + str(gps_fix.longitude))
                        print(gps_fix.time)

                        # only save if data exists
                        if hasattr(main.FD_Data, "data") and len(main.FD_Data.data) > 0:
                            FD_data_tmp = main.FD_Data
                            FD_data_tmp.gps_fix = gps_fix
                            pickle.dump(FD_data_tmp, dataout, pickle.HIGHEST_PROTOCOL)
 #                           pickle.dump(gps_fix, gpsout, pickle.HIGHEST_PROTOCOL)
                            counter =+ 1

                        else:
                            continue

                        # print rate every 100 measurements
                        #if counter % 100 == 0:
                            #elasped = time.time() - start_time
                            #rate = counter / elapsed
                            #print(f"Measurements: {counter}, Rate: {rate:.2f} Hz")

                        # throttle to 0.02 s per measurement
                        #time.sleep(0.02)

                    else:
                        print('Not connected')
                        break

            except KeyboardInterrupt:
                print('\Measurement stopped by user.')
                        

        newname0 = time.strftime("%d_%m_%Y")
        newname = "storage/%s_1" % (newname0)
        if os.path.exists(newname):
            while os.path.exists(newname):
                measnr += 1
                newname = "storage/%s_%d" % (newname0, measnr)
            os.rename("data", newname)
        else:
            os.rename("data", newname)
        if not os.path.exists("data"):
            os.makedirs("data")
        print('--------------------------------')
        print('--------------------------------')
        print('Measurement completed:')
        print(newname)
        print('--------------------------------')
        print('--------------------------------')




    

    main.sysParams.frontendEn = 0 #Turn off the radar!
    


    
print('All done, disconnecting radar!')
main.Disconnect()
