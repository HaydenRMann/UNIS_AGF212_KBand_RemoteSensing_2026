"""
Author: Hayden Mann

Description: Plots and maps snow depth from the radar transect data. 
Requires GPS input.
"""


###
# IMPORTS
###

from radar import ReadFile, SkyCalibration, Combine_channels
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import geopandas as gpd
import matplotlib.ticker as mticker
import cartopy.mpl.ticker as cticker
import matplotlib.colors as mcolors
import pyproj


"""
Objectives:

1. Get gps data and corresponding time (slowtime)
2. Get snow thickness and corresponding slowtime
3. Plot gps data
4. Add color for depth
5. Turn into map
"""


###
# TRANSECT DIRECTORY 
###
"""
MOVING:

09/03 _ 7 - NO
10/03 - 3, 5, 6, 7, 8
"""


###
# PLACE STAND-ALONE TRANSECTS FILENAMES HERE
###

filenames_moving = ["10_03_2026_3", "10_03_2026_5", "10_03_2026_6", "10_03_2026_7", "10_03_2026_8"]
# filenames_moving = ["09_03_2026_7", "10_03_2026_5", "10_03_2026_7", "10_03_2026_8"]



###
# Starting Data Processing
###

# Instantiate arrays for plotting
lats = []
lons = []
z = []

# IMPORT Sky-calibrate filename
FILENAME_SKY_CALIBRATION = "09_03_2026_1"

# Loop through all desired filenames
for filename in filenames_moving:

    # Read filename to get snow thickness
    inp = pd.read_csv('Radar_DATAAA/' + filename + '_pick_vars.csv')  # now it's a DataFrame
    snow_thickness = inp['snow_thickness']  
    slowtime_thickness = inp['slowtime']

    # Read/calibrate to receive time and gps. Timestamps match with snow thickness
    SKY_CALIBRATION = ReadFile(FILENAME_SKY_CALIBRATION)
    radar_data = SkyCalibration(SKY_CALIBRATION, ReadFile(filename))
    radar_data = Combine_channels(radar_data)
    slowtime_radar = radar_data['slowtime']
    gps_data = radar_data['gps']

    # Temporary arrays
    file_lats = []
    file_lons = []
    file_time_gps_array = []

    # Extract GPs
    for loc in gps_data:
        try:
            file_lats.append(loc.latitude)
            file_lons.append(loc.longitude)
            file_time_gps_array.append(loc.time)
        except:
            continue

    file_latslats = np.array(file_lats)
    file_lonslons = np.array(file_lons)

    # Extend arrays (keeps indices consistent)
    lats.extend(file_latslats)
    lons.extend(file_lonslons)
    z.extend(snow_thickness.values)

# Final arrays
lats = np.array(lats)
lons = np.array(lons)
z = np.array(z)


###
# IF YOU HAVE OVERLAPPING TRANSECTS: if not, you can comment out
# this section takes the mean when multiple people have picked data from the same transect, 
# in order to save time/CPU on interpolation and avoid linear algebraic errors.
###
overlapped_lats = []
overlapped_lons = []
overlapped_z = []

# Same logic as above section, just taking the mean instead of extending. 
filenames_moving = ["10_03_2026_4_pick_vars_hayden.csv", "10_03_2026_4_pick_vars_niklas.csv", "10_03_2026_4_pick_vars_Carla.csv", "10_03_2026_4_pick_vars_chloe.csv"]
filename_og_04 = "10_03_2026_4"
for filename in filenames_moving:
    inp = pd.read_csv('Radar_DATAAA/' + filename)  # now it's a DataFrame
    snow_thickness = inp['snow_thickness']  # * -1
    slowtime_thickness = inp['slowtime']

    SKY_CALIBRATION = ReadFile(FILENAME_SKY_CALIBRATION)
    radar_data = SkyCalibration(SKY_CALIBRATION, ReadFile(filename_og_04))
    radar_data = Combine_channels(radar_data)
    slowtime_radar = radar_data['slowtime']
    gps_data = radar_data['gps']

    file_lats = []
    file_lons = []
    file_time_gps_array = []
    # snow_thickness = []

    for loc in gps_data:
        try:
            file_lats.append(loc.latitude)
            file_lons.append(loc.longitude)
            file_time_gps_array.append(loc.time)
        except:
            continue

    file_latslats = np.array(file_lats)
    file_lonslons = np.array(file_lons)

    overlapped_lats.append(file_latslats)
    overlapped_lons.append(file_lonslons)
    overlapped_z.append(snow_thickness.values)
    print(len(snow_thickness))

# Format arrays
overlapped_lats_arr = np.stack(overlapped_lats)
overlapped_lons_arr = np.stack(overlapped_lons)
overlapped_z_arr   = np.stack(overlapped_z)

overlapped_lats_correct = np.mean(overlapped_lats_arr, axis=0)
overlapped_lons_correct = np.mean(overlapped_lons_arr, axis=0)
overlapped_z_correct    = np.mean(overlapped_z_arr, axis=0)

lats = np.concatenate([lats, overlapped_lats_correct])
lons = np.concatenate([lons, overlapped_lons_correct])
z = np.concatenate([z, overlapped_z_correct])


#print(len(z))

###
# Scatter Map Plot
###

# ESRI World Imagery tiles (real satellite)
class ESRIImagery(cimgt.GoogleTiles):
    def _image_url(self, tile):
        x, y, z = tile
        return (
            "https://services.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ).format(z=z, y=y, x=x)
image = ESRIImagery()

# Set figure size
# fig = plt.figure(figsize=(8, 8))
fig = plt.figure(figsize=(8, 6))
ax = plt.axes(projection=image.crs)

# Retreive interpolation extent
tellbreen_extent = gpd.read_file("tellbreen_extent_converted.shp")

# 3143 is for north but also rotates it (need to learn projection specificts). apparently 32633 also uses meters only so won't distorr
# doesnt affect plots at all, just for extent
TARGET_CRS = "epsg:32633" 

#  convert tellbreen extent shapefile to target crs
tellbreen_extent = tellbreen_extent.to_crs(TARGET_CRS)
s_minx, s_miny, s_maxx, s_maxy = tellbreen_extent.total_bounds
ax.set_extent(
    [s_minx - 250, s_maxx + 250, s_miny - 250, s_maxy + 250],
    crs=ccrs.UTM(33)
)

ax.add_image(image, 14) 

sc = ax.scatter(
    lons,
    lats,
    c=z,
    cmap="plasma_r",
    s=10,
    transform=ccrs.PlateCarree(),
    edgecolors='black', 
    linewidths=0.03
)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# SCATTER TICKS
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
import cartopy.mpl.ticker as cticker

gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=True,
    linewidth=0.5,
    color='gray',
    alpha=0.6,
    linestyle='--'
)

gl.top_labels = False
gl.right_labels = False
gl.left_labels = True
gl.bottom_labels = True
# gl.xlines = False
# gl.ylines = False

# Formatting
gl.xformatter = cticker.LongitudeFormatter()
gl.yformatter = cticker.LatitudeFormatter()

gl.xlocator = mticker.MaxNLocator(nbins=5)
gl.ylocator = mticker.MaxNLocator(nbins=5)

gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

plt.colorbar(
    sc,
    ax=ax,
    orientation='vertical',
    pad=0.02,
    fraction=0.0238, # adjust this to set colorbar height
    label="Snow Thickness [m]"
)
# sc.set_clim(0, 2)
# sc.set_clim(0.36, 1.65) # Can hard-code or not hard-code.

# print(z.min())
# print(z.max())
plt.savefig('latest_transects.png', dpi=600)





###
# Save Data Points
###

df_out = pd.DataFrame({
    "latitude": lats,
    "longitude": lons,
    "snow_thickness": z
})

df_out.to_csv("gps_snow_depth.csv", index=False)

print(min(z))
print(max(z))
print(np.mean(z))



"""
Linear Trend: Longitudinal
"""

# convert from lat/lon into x/y
proj = pyproj.Transformer.from_crs("epsg:4326", "epsg:32633", always_xy=True)
x, y = proj.transform(lons, lats)

x0 = x - x.min()
y0 = y - y.min()

x0_km = x0 / 1000
y0_km = y0 / 1000

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
(fig, ax1) = plt.subplots(1, 1, figsize=(12,5))

# Plot East-West 
sc = ax1.scatter(x0_km,
             z, 
             s=10, 
             alpha=0.5,
             c=lats)

m1, b1 = np.polyfit(x0_km, z, 1)

idx = np.argsort(x0_km)
ax1.plot(x0_km[idx], m1*x0_km[idx] + b1, color='red', label=f'Trend: y={m1:.2f}x +{b1:.2f}')

ax1.set_xlabel("Distance East from Westernmost Measurement [km]")
ax1.set_ylabel("Snow Thickness [m]")
ax1.set_title("Snow Thickness vs East-West Position")
ax1.grid(True, alpha=0.3)
ax1.legend()

cbar = plt.colorbar(sc, ax=ax1)
cbar.set_label("Latitude")

plt.savefig('longitudinal.png', dpi=600)

plt.show()


# Plot North-South 
# ax2.scatter(y0_km, z, s=10, alpha=0.5, color='red')

# m2, b2 = np.polyfit(y0_km, z, 1)

# idx = np.argsort(y0_km)
# ax2.plot(y0_km[idx], m2*y0_km[idx] + b2, color='black', label=f'Trend: y={m2:.2f}x+{b2:.2f}')

# ax2.set_xlabel("Distance North from Southernmost Measurement [km]")
# # ax2.set_ylabel("Snow Thickness [m]")
# ax2.set_title("Snow Thickness vs North-South Position")
# ax2.grid(True, alpha=0.3)
# ax2.legend()

# plt.tight_layout()
# plt.show()
