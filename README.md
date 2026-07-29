This Python code uses the The OpenSky Network, https://opensky-network.org API to gather live flight data. The method `get_data` in `get_flight_data.py` uses a rectangular bounding box defined by minimum and maximum longitudinal and latitudinal coordinates. The method returns a dataframe with information about all flights from the moment of the request inside that bounding box.

The columns of the DataFrame represent the fields used by the API. I recommend checking out the documentation for a description of the different fields at https://openskynetwork.github.io/opensky-api/rest.html.

The data can be used for various purposes. This project includes two example applications.

## Example 1 - plotting a map with all current flight positions

This example uses a bounding box above germany with latitudinal coordinates from 45.2 to 56.1 and longitudinal coordinates from 1.5 to 17.5. The OpenSky Network API is then called once to get all current aircraft positions. Some aircrafts may be featured in the data with an active transponder which are currently on the ground. This information is included in the data with the field `on_ground` and those airplanes are removed for this plot.

![](example_1_positions.png)


## Example 2 - plotting a map with flight tracks

This example uses a bounding box above italy. To plot flight tracks the positions of the aircrafts need to be tracked over time. The method `get_data` has two additional parameters `number_of_rescans` and `delay_between_rescans`. For the tracks above a country with a size of italy its sufficient to rescan the positions once a minute. The plot then interpolates these positions with line segments. The number of rescans can then be selected for the required length of a track. If you want to create tracks that represent exactly one hour then you could use `number_of_rescans = 60` and `delay_between_rescans = 60`. For smaller boxes increase `delay_between_rescans = 100`.

![](example_2_tracks.png)

Some notes on using multiple scans. This code uses the anonymous access to the OpenSky Network API which is restricted to a time resolution of 10 seconds. Using a `delay_between_rescans < 10` will not result in a higher resolution. Your API requests should also be made with care. Too many requests or to short delays between rescans might end up in the server putting you in a cooldown or even to block your IP so dont exaggerate it.

This script also isnt meant for scale. If you do a bunch of rescans the script will run until the final batch of data is gathered. Each bundle of gathered data is only stored in the cache. If you want to run this over multiple hours or even days you should use `number_of_rescans = 1` and store each response (for example in a SQLite databse). 

Also see the original paper for the OpenSky Network:

Matthias Schäfer, Martin Strohmeier, Vincent Lenders, Ivan Martinovic and Matthias Wilhelm.
"Bringing Up OpenSky: A Large-scale ADS-B Sensor Network for Research".
In Proceedings of the 13th IEEE/ACM International Symposium on Information Processing in Sensor Networks (IPSN), pages 83-94, April 2014.
