import pandas as pd
from geopy.distance import geodesic

players_df = pd.read_csv(r'C:\Users\nateb\OneDrive\Documents\ACCPlayerCase\Geocoded_ACC_Players_Hometowns.csv')
schools_df = pd.read_csv(r'C:\Users\nateb\OneDrive\Documents\ACCPlayerCase\Geocoded_ACC_Schools.csv')

# merge the two datasets on the "School" column
merged_df = pd.merge(players_df, schools_df, on="School")

# calculate distance between two sets of coordinates
def calculate_distance(row):
    hometown_coords = (row['Hometown Lat'], row['Hometown Lon'])
    school_coords = (row['School Lat'], row['School Lon'])
    return geodesic(hometown_coords, school_coords).miles

# apply the calculation to the data frame
merged_df['Distance_mi'] = merged_df.apply(calculate_distance, axis=1)

# save merged csv
merged_df.to_csv(r'C:\Users\nateb\OneDrive\Documents\ACCPlayerCase\Player_School_Distances.csv', index=False)


