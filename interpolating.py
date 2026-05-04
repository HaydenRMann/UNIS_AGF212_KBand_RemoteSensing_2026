"""
Author: Hayden Mann

Description: Interpolates snow depth data, provided via 
gps_snow_depth.csv within Tellbreen. Performs linear 
radial basis function interpolation. Plots the
interpolation.
"""



###
# IMPORTS
###

import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
from shapely.geometry import Point

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.ticker as mticker
import cartopy.mpl.ticker as cticker



###
# Load Data
###

df = pd.read_csv("gps_snow_depth.csv")
tellbreen_extent = gpd.read_file("tellbreen_extent_converted.shp")

# Set CRS + Grid Resolution 
TARGET_CRS = "epsg:32633"  # 3143 is for north but also rotates it (need to learn projection specificts). apparently 32633 also uses meters only so won't distorr
GRID_RES = 400  # grid points

# convert tellbreen extent shapefile to target crs
tellbreen_extent = tellbreen_extent.to_crs(TARGET_CRS)

# converting our snow depth points (lat/lon/snowdepth) into target crs
    # note that these points were made using ccrs: PLateCarree (flat lat/lon projection) -> recomended to use 4326 for this (WGS 84)
    # basically from degrees to meters
gdf_points = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="epsg:4326"
).to_crs(TARGET_CRS)

# rounds gps cordinates with one decimal point
gdf_points['x'] = gdf_points.geometry.x.round(1)
gdf_points['y'] = gdf_points.geometry.y.round(1)

# 3 steps:  
    # 1. groups all snow thickness points by their x and y coordinates, so they don't overlap
    # 2. takes the mean snow thickness
    # 3. assignes to the x/y plot and then resets the index
df_clean = gdf_points.groupby(['x', 'y'])['snow_thickness'].mean().reset_index()

# get arrays from each column in the dataframe
x_pts = df_clean['x'].values
y_pts = df_clean['y'].values
z_pts = df_clean['snow_thickness'].values




###
# Create masking grid
###

# extract min/max x, y fro, shapefile
minx, miny, maxx, maxy = tellbreen_extent.total_bounds

# create a mesh grid with desired resolution (see above)
grid_x, grid_y = np.meshgrid(
    np.linspace(minx, maxx, GRID_RES),
    np.linspace(miny, maxy, GRID_RES)
)

# flattens the grid. i used .flatten but gpt recomended .ravel (same thing mostly just quicker)
flat_grid = np.vstack([grid_x.ravel(), grid_y.ravel()]).T

# create point obejcts and put them into a geodataframe in our crs
mask_pts = [Point(p) for p in flat_grid]
mask_gdf = gpd.GeoDataFrame(geometry=mask_pts, crs=TARGET_CRS)

# make sure all points are in glacier
within_mask = gpd.sjoin(mask_gdf, tellbreen_extent, how="left", predicate="within")
valid_mask = ~within_mask.index_right.isna().values.reshape(grid_x.shape)




###
# Interpolation Fx
###

print("Interpolating " +  str(len(x_pts)) + " points in EPSG:3413...")

# linear scipy interpolation set up function
rbf = Rbf(x_pts, y_pts, z_pts, function='linear', smooth=0.2)

# # cubic scipy interpolation
# rbf = Rbf(x_pts, y_pts, z_pts, function='cubic', smooth=0.2)

# makes empty grid of NaN
z_grid = np.full(grid_x.shape, np.nan)

# runs the rbf fx on the grid x and grid y
z_grid[valid_mask] = rbf(grid_x[valid_mask], grid_y[valid_mask])

# make sure snow doesn't go below 1.1 x min or max
z_grid = np.clip(z_grid, z_pts.min() / 1.1, z_pts.max() * 1.1)



###
# Plotting
###

# Get basemap
class ESRIImagery(cimgt.GoogleTiles):
    def _image_url(self, tile):
        x, y, z = tile
        return (f"https://services.arcgisonline.com/ArcGIS/rest/services/"
                f"World_Imagery/MapServer/tile/{z}/{y}/{x}")
image = ESRIImagery()

# gets it in EPSG:32633, which is best for svalbard accordng to google
utm_crs = ccrs.UTM(zone=33, southern_hemisphere=False) 

# start plot
# fig = plt.figure(figsize=(12, 10))
fig = plt.figure()
# i checked the image crs is mercator
ax = plt.axes(projection=image.crs) 


# map bounds - based on shapefile 
s_minx, s_miny, s_maxx, s_maxy = tellbreen_extent.total_bounds

ax.set_extent(
    [s_minx - 250, s_maxx + 250, s_miny - 250, s_maxy + 250],
    crs=utm_crs  # meters!!
)

# add satellite, the 14 is what google said the best level of zoom would be (about 3x3 meter pixels)
ax.add_image(image, 14) 

# mask grid
z_masked = np.ma.masked_invalid(z_grid)

# plot interpolation
im = ax.pcolormesh(
    grid_x, grid_y, z_masked,
    cmap='seismic_r',
    transform=utm_crs,
    # zorder=10,        # put on top
    alpha=0.9,        # Transparency
    shading='auto'
)

# plotting boundary, use utm_crs to transofm to match
ax.add_geometries(
    [tellbreen_extent.geometry.iloc[0].boundary], 
    crs=utm_crs, 
    facecolor='none', 
    edgecolor='black', 
    linewidth=1.5,
    alpha = 0.6
)

# radar path
ax.scatter(
    df['longitude'], df['latitude'],
    # c=df['snow_thickness'], s=0.05, alpha=0.5, ### snow thickness
    c='black',
    s=0.01, 
    alpha=0.3, ### white!
    transform=ccrs.PlateCarree()
)

###
# Formatting
###
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
# gl.xlines = False
# gl.ylines = False # i want the lines for now

# Ticks
gl.xformatter = cticker.LongitudeFormatter()
gl.yformatter = cticker.LatitudeFormatter()
gl.xlocator = mticker.MaxNLocator(nbins=5)
gl.ylocator = mticker.MaxNLocator(nbins=5)

gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

plt.colorbar(
    im,
    ax=ax,
    orientation='vertical',
    pad=0.02,
    fraction=0.0238, # adjust this to set colorbar height
    label="Snow Thickness [m]",
)

# im.set_clim(0.36007363520912, 1.5915264699359375) # Color bar options
im.set_clim(0, 2)


plt.savefig('latest_interpolation.png', dpi=600)
# plt.title("Snow Thickness Interpolation (linear)")
plt.show()
