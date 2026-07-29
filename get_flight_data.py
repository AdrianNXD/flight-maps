import requests
import pandas as pd
import time

def get_data(latitude_min:float, 
             longitude_min:float, 
             latitude_max:float, 
             longitude_max:float, 
             number_of_scans:int=1, 
             delay_between_scans:int=60
            ) -> pd.DataFrame:
    '''
        This method scans an area for flights. The area is defined by a rectangular bounding 
        box from (latitude_min, longitude_min) to (latitude_max, longitude_max) using WGS84 
        coordinates. The data is gathered from the OpenSky API (https://opensky-network.org)
        and stored in a DataFrame. The DataFrame uses columns that equal the fields of the 
        state vectors predetermined by the API (see https://openskynetwork.github.io/opensky-api/rest.html). 
        Besides other information it mainly contains the ICAO 24-bit address as a unique 
        identifier with the corresponding location coordinates. The API returns live data that 
        can be used for a geographical scatter plot or other analysis. To visualize tracks over 
        time multiple requests with delays between them are required. number_of_scans can 
        therefore be increased with delay_between_scans as a delay in seconds. Note that too 
        many requests or to short delays between requests might end up with the server forcing 
        a cooldown or even block your IP.       

    '''

    url = "https://opensky-network.org/api/states/all"

    # create an empty dataframe
    df = pd.DataFrame(columns=[
        "time",
        "icao24",
        "callsign",
        "origin_country",
        "time_position",
        "last_contact",
        "longitude",
        "latitude",
        "baro_altitude",
        "on_ground",
        "velocity",
        "true_track",
        "vertical_rate",
        "sensors",
        "geo_altitude",
        "squawk",
        "spi",
        "position_source",
        "category"])

    for k in range(number_of_scans):

        response = requests.get(url, params={"lamin": latitude_min,"lamax": latitude_max,"lomin": longitude_min,"lomax": longitude_max})

        if response.status_code != 200:
            print("AN HTML ERROR OCCURED", response.status_code)
            break

        # extract the data from the response
        data = response.json()

        timestamp = data["time"]
        states = data["states"]

        if not states:  # if no data found, write a error message
            print(f"no data at time={timestamp}.")
            continue
      
        # append every flight to the dataframe
        for state in states:
            row = [timestamp] + state

            # sometimes the category (last field) is missing
            if len(row) == 18: row += [""]

            df.loc[len(df)] = row

        # delay the next request if multiple scans should be made
        if number_of_scans > 1: 
            print(f"scans done: {k+1}/{number_of_scans}")
            time.sleep(delay_between_scans)

    return df
