from radar_niklas2 import ReadFile, SkyCalibration, Combine_channels
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

"""
Goals:

1. Get gps data and corresponding time (slowtime)
2. Get snow thickness and corresponding slowtime
3. Plot gps data
4. Add color for depth
5. Turn into map
"""

"""
MOVING:

09/03 _ 7
10/03 - 3, 5, 6, 7, 8
"""


filename = "09_03_2026_7"
FILENAME_SKY_CALIBRATION = "09_03_2026_1"

inp = pd.read_csv('Radar_DATAAA/' + filename + '_pick_vars.csv')  # now it's a DataFrame
snow_thickness = inp['snow_thickness']  # * -1
slowtime_thickness = inp['slowtime']

SKY_CALIBRATION = ReadFile(FILENAME_SKY_CALIBRATION)
radar_data = SkyCalibration(SKY_CALIBRATION, ReadFile(filename))
radar_data = Combine_channels(radar_data)
slowtime_radar = radar_data['slowtime']
gps_data = radar_data['gps']

print(gps_data[1].latitude)
print(gps_data[1].longitude)


lats = []
lons = []
time_gps_array = []
# snow_thickness = []

for loc in gps_data:
    try:
        lats.append(loc.latitude)
        lons.append(loc.longitude)
        time_gps_array.append(loc.time)
    except:
        continue

lats = np.array(lats)
lons = np.array(lons)

x = lons
y = lats
z = snow_thickness.values  


"""
SCATTER
"""

# ESRI World Imagery tiles (real satellite)
class ESRIImagery(cimgt.GoogleTiles):
    def _image_url(self, tile):
        x, y, z = tile
        return (
            "https://services.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ).format(z=z, y=y, x=x)
image = ESRIImagery()

fig = plt.figure(figsize=(8, 8))

ax = plt.axes(projection=image.crs)

# PlateCarree for GPS coords
ax.set_extent(
    [lons.min()-0.0075, lons.max()+0.0075,
     lats.min()-0.0025, lats.max()+0.0025],
    crs=ccrs.PlateCarree()
)


ax.add_image(image, 14) 

sc = ax.scatter(
    lons,
    lats,
    c=z,
    cmap="viridis",
    s=10,
    transform=ccrs.PlateCarree()
)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.colorbar(sc, label="Snow Thickness")
plt.title("GPS Track on Satellite Map (ESRI)")



## SCATTER TICKS
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
gl.xlines = False
gl.ylines = False

# formattingg
gl.xformatter = cticker.LongitudeFormatter()
gl.yformatter = cticker.LatitudeFormatter()

# how many ticks
gl.xlocator = mticker.MaxNLocator(nbins=5)
gl.ylocator = mticker.MaxNLocator(nbins=5)

gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}



plt.show()









# """
# LINE PLOT
# """

# points = np.column_stack([x, y])
# segments = np.stack([points[:-1], points[1:]], axis=1)

# lc = LineCollection(segments, cmap='viridis')
# lc.set_array(z[:-1])
# lc.set_linewidth(3)

# fig, ax = plt.subplots()
# ax.add_collection(lc)

# ax.set_xlim(x.min(), x.max())
# ax.set_ylim(y.min(), y.max())
# ax.autoscale()


# # Fix axes labels
# ax = plt.gca()
# ax.ticklabel_format(useOffset=False, style='plain')


# plt.colorbar(lc, label="Snow Thickness")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.grid()

# plt.show()


# ax.plot(slowtime_radar, snow_thickness, 'k-', linewidth=2)
# ax.set_xlabel("Time (s)")
# ax.set_ylabel("Snow thickness (m)")
# ax.set_title("Snow thickness")
# ax.grid(True, alpha=0.3)
# plt.show()


# """"

# for copying




# block_size = 100
# n_blocks = len(x) // block_size + (len(x) % block_size != 0)
# surface_pts = []
# for num in range(n_blocks):
#     x_block = x[num * block_size : (num + 1) * block_size]
#     data_block = data[:, num * block_size : (num + 1) * block_size]

#     fig, ax = plt.subplots(figsize=(14, 7))

#     ax.pcolormesh(
#         x_block,
#         y,
#         data_block,
#         vmin=0,
#         vmax=1,
#         shading="auto"   # important for safety with pcolormesh
#     )

#     ax.invert_yaxis()
#     ax.set_title(f"Block {num+1}/{n_blocks}: Click surface points, then press Enter")

#     plt.show()

#     surface_pts_block = plt.ginput(n=-1, timeout=0)
#     plt.close(fig)

#     surface_pts_block = np.asarray(surface_pts_block, dtype=float)
#     if surface_pts_block.size > 0:
#         surface_pts.append(surface_pts_block)  

# surface_pts = np.concatenate(surface_pts, axis=0)

# """