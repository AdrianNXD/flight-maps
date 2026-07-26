# In this example the get_flight_data method is used once
# to grab all aircraft positions above germany and plot
# them on a map.


from get_flight_data import get_data

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from pyproj import Transformer


if __name__ == "__main__":

    # define the borders of the bounding box
    latitude_min = 45.2
    longitude_min = 1.5
    latitude_max = 56.1
    longitude_max = 17.5

    # get the positions of all flight above germany
    df = get_data(
        latitude_min = latitude_min, longitude_min = longitude_min,
        latitude_max = latitude_max, longitude_max = longitude_max
    )

    # now plot the positions with a map in the background

    # first select only airplanes that arent on the ground
    df = df[df["on_ground"] != True]

    # create a GeoDataFrame from the data
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326" # <- coordinates use WGS84 system
    )

    # we plot the background map with contextly which uses the 
    # Web Mercator 3857 system. convert our coordinates now to 
    # this system.
    gdf = gdf.to_crs(epsg=3857)

    # also transform the bounding box from WGS84 to Web Mercator 3857
    transformer = Transformer.from_crs(4326, 3857, always_xy=True)
    xmin, ymin = transformer.transform(longitude_min, latitude_min)
    xmax, ymax = transformer.transform(longitude_max, latitude_max)

    # now create the actual plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # you can play with the styling of the markers here. You can 
    # also split the dataframe into multiple ones and plot them
    # each with a different color encoding a different category of 
    # your interest.
    gdf.plot(
        ax          = ax,
        color       = "red", 
        markersize  = 80,
        alpha       = 0.3
    )

    # set the bounding box
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_axis_off()

    # create the map in the background. Other sources for the map
    # can be used such as source=ctx.providers.CartoDB.Positron or
    # source=ctx.providers.CartoDB.VoyagerNoLabels to get a different
    # style of the map.
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    plt.title("example 1 - current flight positions above germany")

    plt.savefig(
        "example_1_positions.png",
        dpi=450,
        bbox_inches="tight"
    )

    plt.show()
