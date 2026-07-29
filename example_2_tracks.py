# In this example the get_flight_data method is used multiple
# times to track aircraft positions over a certain time to 
# plot a map with the flight tracks of those crafts above italy.
# This script will run until all data is grabbed.

from get_flight_data import get_data

import matplotlib.pyplot as plt
import contextily as ctx
from pyproj import Transformer
from matplotlib.collections import LineCollection
import numpy as np


if __name__ == "__main__":

    # define the borders of the bounding box
    latitude_min = 36.1
    longitude_min = 4.5
    latitude_max = 47.2
    longitude_max = 20.3

    # get the positions of all flight above italy
    df = get_data(
        latitude_min = latitude_min, longitude_min = longitude_min,
        latitude_max = latitude_max, longitude_max = longitude_max,
        number_of_scans = 20, delay_between_scans = 60
    )

    # in this example we want to plot the tracks of airplanes above the map.
    # Therefore we only need flights where we recorded at least two positions.
    # We also group the data by the ICAO number as an unique identifier for the flight.
    df = df[df.groupby("icao24")["icao24"].transform("size") >= 2]


    # transform the bounding box to Web Mercator coordinates (see Example 1)
    transformer = Transformer.from_crs(
            "EPSG:4326",
            "EPSG:3857",
            always_xy=True
        )

    xmin, ymin = transformer.transform(longitude_min, latitude_min)
    xmax, ymax = transformer.transform(longitude_max, latitude_max)

    # the data is already grouped by the ICAO number. We sort each group by the
    # timestamp. We can then create a track (which is a set of lines between the
    # distinct points) for each individual group.
    tracks = {
        icao: group.sort_values("time")[[
            "longitude",
            "latitude"
        ]]
        for icao, group in df.groupby("icao24")
    }

    # now create the line segments for the track.
    all_segments = []
    all_alpha = []

    for icao in tracks.keys():

        track = tracks[icao].dropna()

        # transform the coordinates of the locations EPSG4326 -> EPSG3857
        x, y = transformer.transform(
            track.longitude.values,
            track.latitude.values
        )

        points = np.column_stack([x, y])

        # create the segments
        segments = np.stack(
            [
                points[:-1],
                points[1:]
            ],
            axis=1
        )

        all_segments.extend(segments)

        # to stylize the plot and to visualize the direction of a flight
        # we can use a fading opacity.
        alpha = np.linspace(
            0.2,
            0.8,
            len(segments)
        )

        all_alpha.extend(alpha)

    # now plot everything
    fig, ax = plt.subplots(figsize=(10, 10))

    # set the bounding box
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_axis_off()

    # create a collection of all segments and then plot the whole
    # collection (this is faster than plotting each line separate)
    lc = LineCollection(
        all_segments,
        colors="brown",
        linewidths=2,
        alpha=all_alpha
    )

    ax.add_collection(lc)

    # create the map in the background. Other sources for the map
    # can be used such as source=ctx.providers.CartoDB.Positron or
    # source=ctx.providers.CartoDB.VoyagerNoLabels to get a different
    # style of the map.
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    plt.title("example 2 - current flight tracks above italy")

    plt.savefig(
        "example_2_tracks.png",
        dpi=450,
        bbox_inches="tight"
    )

    plt.show()
