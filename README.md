# UNIS_AGF212_KBand_RemoteSensing_2026
Data and Code for UNIS AGF-212 Remote Sensing project

# Scripts

## Initial Radar Processing
- *ConfigClasses.py<sup>I</sup>*: specifies system parameters
- *200_measurements_BW2500.py*: script to operate the radar and conduct exactly 200 measurements in the field, saving data to "data.pkl"-file, files will be stored in a folder named after date and a continuously increasing counter for each measurement: "dd_mm_yyyy_counter"
- *200_plot_radar*: creates simple plots (radargram, final range profile of every channel) to check whether collected data makes sense
- *check_code.py*: checks to see if the original radar code is working
- *continuous_measurements_BW2500.py*: like "200_measurements_BW2500.py", but measurement number is not limited by 200 and operation has to be terminated by a user input
- *continuous_measurements_BW2500_GPS.py*: same as "continuous_measurements_BW2500.py", but also records GPS-data
- *radar_niklas2.py: includes the Main-class used for operating the radar and thus is imported in "200_measurements_BW2500.py", "continuous_measurements_BW2500.py*" and "continuous_measurements_BW2500_GPS.py". Also includes useful functions for reading in .pkl-files, sky calibration, propagation speed correction, combining of channels and normalization --> maybe just rename to radar and delete the other radar.py, change the imports of some scripts ?
- *signalling.py*: seems to be the same as "plot_data_with_GPS" do we need it ?
- *single_measurement.py*: same as "200_measurements_BW2500.py" but only performs one single measurement instead of 200



## Picking, Data Processing
- *picking_working.ipynb*: Jupyter notebook to manually identify and pick the height of snow surface and snow-ice interface. This is done by clicking on the radargram of a given measurement file. The heights of both interfaces as well as the calculated snow depth will be saved as both a .csv-file and a .npz-file
- *stationary_SWE.py*: Jupyter notebook to calculate the signal propagation speed in snow, the snow density and the SWE from given values of radar-measured snow thickness and actual measured snow thickness. Uncertainties can be specified and processed with Gaussian error propagation



## Plotting
- *interpolating.py*: ?
- *multi_gps_track_depth*: ?
- *plot_data_with_GPS.py*: same as '200_plot_radar', but additionally creates plot of the GPS track
- *plot_first_frame.py*: same as '200_plot_radar' do we need it ?
- *plot_last_frame.py*: same thing ?


