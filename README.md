# UNIS_AGF212_KBand_RemoteSensing_2026
Data and Code for UNIS AGF-212 Remote Sensing project
- Overall Authors: Carla Amic, Chloé Ghibaudo, Hayden Mann, Niklas Weber
- *If anything appears to be not working or missing: Contact Hayden and Niklas (emails below)*

### Code Author Directory:
- I: Hayden Mann: hmann@bowdoin.edu (until Summer 2027), hay.mann@icloud.com
- II: Niklas Weber: we.ni@gmx.de
- III: Carla Amic: carla-kus@gmx.de
- IV: Professor Eero Rinne: eeror@unis.no
- V: Emma Mickey J. MacKie and later adapted by Niels Boelt Mortensen (external)
- VI: IMST GmbH (external)


# Scripts

## Plotting
- *interpolating.py<sup> I</sup>*: Interpolates snow depth data, provided via gps_snow_depth.csv within Tellbreen. Performs linear radial basis function interpolation.
- *multi_gps_track_depth<sup> I</sup>*: Plots and maps snow depth from the radar transect data.
- *plot_data_with_GPS.py<sup> IV</sup>*: same as '200_plot_radar', but additionally creates plot of the GPS track

## Picking, Data Processing
- *picking_working.ipynb<sup> I, II, V</sup>*: Jupyter notebook to manually identify and pick the height of snow surface and snow-ice interface. This is done by clicking on the radargram of a given measurement file. The heights of both interfaces as well as the calculated snow depth will be saved as both a .csv-file and a .npz-file. Original script via Emma Mickey J. MacKie and later adapted by Niels Boelt Mortensen before being tailored by Hayden Mann and Niklas Weber for this specific project.
- *stationary_SWE.py<sup> V, II, III</sup>*: Jupyter notebook to calculate the signal propagation speed in snow, the snow density and the SWE from given values of radar-measured snow thickness and actual measured snow thickness. Uncertainties can be specified and processed with Gaussian error propagation


## Initial Radar Processing
- *ConfigClasses.py<sup> VI</sup>*: specifies system parameters
- *200_measurements_BW2500.py*<sup> IV</sup>*: script to operate the radar and conduct exactly 200 measurements in the field, saving data to "data.pkl"-file, files will be stored in a folder named after date and a continuously increasing counter for each measurement: "dd_mm_yyyy_counter"
- *200_plot_radar<sup> IV</sup>*: creates simple plots (radargram, final range profile of every channel) to check whether collected data makes sense
- *check_code.py<sup> IV</sup>*: checks to see if the original radar code is working
- *continuous_measurements_BW2500.py<sup> IV</sup>*: like "200_measurements_BW2500.py", but measurement number is not limited by 200 and operation has to be terminated by a user input
- *continuous_measurements_BW2500_GPS.py<sup> IV</sup>*: same as "continuous_measurements_BW2500.py", but also records GPS-data
- *radar.py<sup> IV, II</sup>*: includes the Main-class used for operating the radar and thus is imported in "200_measurements_BW2500.py", "continuous_measurements_BW2500.py*" and "continuous_measurements_BW2500_GPS.py". Also includes useful functions for reading in .pkl-files, sky calibration, propagation speed correction, combining of channels and normalization. Original author is Eero Rinne, code adapted by Niklas Weber.
- *single_measurement.py<sup> IV</sup>*: same as "200_measurements_BW2500.py" but only performs one single measurement instead of 200

# Other Files

- *Tellbreen_extent....<sup> I</sup>*: Shapefile extent of Tellbreen. EPSG/CRS is attached. Created in QGIS.
- *Interfaces* (Folder): Necessary to run the radar code.
- *Radar_DATAAA<sup>* all main authors</sup>*: Radar raw data, in .pkl format, from each Tellbreen transect from 04 March to 10 March.
- *gps_snow_depth.csv<sup> I</sup>*: A formatted .csv with latitude, longitude, and snow depth from the transect measurements.


# How to Run:

## Running the Radar: (All Code Written by IV: Eero Rinne)
- Run through command line: in the format of "python3 [codename].py desired_filename"
- Contact author for help: Eero Rinne: eeror@unis.no

## Data Analysis and Plotting:
- *picking_working.ipynb<sup> I, II, V</sup>*: Input your filenames into the code and run the notebook.
- *stationary_SWE.py<sup> V, II, III</sup>*: Input your filenames into the code and run the notebook.
- *interpolating.py<sup> I</sup>*: Input your filenames into the code and run the script.
- *multi_gps_track_depth<sup> I</sup>*: Input your filenames into the code and run the script.


# Example Plots:

- Interpolation (executes with current code in interpolation.py):<img width="3840" height="1624" alt="latest_interpolation" src="https://github.com/user-attachments/assets/b7e9b1a1-b261-4d38-b302-e86bf2bacf80" />
- Transects (executes with current code in multi_gps_track_depth.py): <img width="4800" height="1998" alt="latest_transects" src="https://github.com/user-attachments/assets/d70a22a2-d97a-442e-8689-5349603f62db" />

