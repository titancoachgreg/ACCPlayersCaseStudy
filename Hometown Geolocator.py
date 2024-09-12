import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

df = pd.read_csv(r'C:\Users\nateb\OneDrive\Documents\ACCPlayers.csv')

# clean the CSV file (same CSV will be used for chi squared and the heatmap, but chi sq requires the school state)
df_cleaned = df[['Player', 'School', 'Hometown', 'State']].copy()
df_cleaned.columns = ['Player', 'School', 'Hometown', 'Hometown State']

# geocode the hometowns of each player using Nominatim
geolocator = Nominatim(user_agent="hometown_geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
def get_coordinates(location):
    try:
        loc = geocode(location)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None
    except:
        return None, None

df_cleaned['Hometown Full'] = df_cleaned['Hometown'] + ', ' + df_cleaned['Hometown State']

# progress bar for hometown geogocoding
tqdm.pandas(desc="Geocoding hometowns")

# add full geocoded coordinates column
df_cleaned['Hometown Coordinates'] = df_cleaned['Hometown Full'].progress_apply(get_coordinates)

# split full coordinates into latitude and longitude for heat map
df_cleaned['Hometown Lat'], df_cleaned['Hometown Lon'] = zip(*df_cleaned['Hometown Coordinates'])

df_cleaned.to_csv('Geocoded_ACC_Players_Hometowns.csv', index=False)

