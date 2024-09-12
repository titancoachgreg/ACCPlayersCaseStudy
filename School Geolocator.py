import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

df_schools = pd.read_csv(r'C:\Users\nateb\OneDrive\Documents\ACCSchoolLocations.csv')

# geocode the hometowns of each school using Nominatim
geolocator = Nominatim(user_agent="school_geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
def get_school_coordinates(location):
    try:
        loc = geocode(location)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None
    except:
        return None, None

df_schools['Full Location'] = df_schools['School'] + ', ' + df_schools['State']

# progress bar for school geolocation
tqdm.pandas(desc="Geocoding school locations")

# add full geocoded coordinates column
df_schools['School Coordinates'] = df_schools['Full Location'].progress_apply(get_school_coordinates)

# split full coordinates into latitude and longitude for heat map
df_schools['School Lat'], df_schools['School Lon'] = zip(*df_schools['School Coordinates'])

df_schools.to_csv('Geocoded_ACC_Schools.csv', index=False)

