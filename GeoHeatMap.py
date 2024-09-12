import pandas as pd
import folium
from folium.plugins import HeatMap
import os

# load the geocoded player and school data
df_players = pd.read_csv(r'C:\Users\nateb\OneDrive\Documents\ACCPlayerCase\Geocoded_ACC_Players_Hometowns.csv')
df_schools = pd.read_csv(r'C:\Users\nateb\OneDrive\Documents\ACCPlayerCase\Geocoded_ACC_Schools.csv')

# directory where logos are stored
logo_folder = r'C:\Users\nateb\OneDrive\Documents\Logos'

# create folder to store the HTML files
output_folder = 'heatmaps_with_schools'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# add a column to df_schools with paths to logo images (ensure the file paths are correct)
# create a new column 'Logo_Path' which contains the full path to the logo for each school
df_schools['Logo_Path'] = df_schools['School'].apply(lambda x: os.path.join(logo_folder, f"{x.lower().replace(' ', '_')}_logo.png"))

# function to generate a heatmap for the selected school and overlay the school's location with a logo marker
def generate_heatmap_with_school(school):
    # filter the players by the selected school
    filtered_players = df_players[df_players['School'] == school]

    # get the school location and logo
    school_location = df_schools[df_schools['School'] == school]

    if not filtered_players.empty:
        # center the map around the average of players' coordinates
        center_lat = filtered_players['Hometown Lat'].mean()
        center_lon = filtered_players['Hometown Lon'].mean()
    else:
        # fallback to a default US center if no average
        center_lat = 37.0902
        center_lon = -95.7129

    # base map
    school_map = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    # prepare data for the heatmap (players' hometowns)
    heat_data = [
        [row['Hometown Lat'], row['Hometown Lon']]
        for index, row in filtered_players.iterrows()
        if not pd.isnull(row['Hometown Lat'])
    ]

    # add the heatmap layer
    HeatMap(heat_data).add_to(school_map)

    # add a custom logo marker for the school's location
    if not school_location.empty:
        logo_path = school_location['Logo_Path'].values[0]
        if os.path.exists(logo_path):  # check if logo file exists
            logo_icon = folium.CustomIcon(logo_path, icon_size=(45, 45))  # adjust size as needed
            folium.Marker(
                location=[school_location['School Lat'].values[0], school_location['School Lon'].values[0]],
                popup=school,
                icon=logo_icon
            ).add_to(school_map)

    # save map to folder
    map_filename = os.path.join(output_folder, f"{school}_heatmap_with_school.html")
    school_map.save(map_filename)
    print(f"Map for {school} saved as '{map_filename}'.")

    return school_map

# function to generate a heatmap for all schools combined
def generate_acc_heatmap():
    # base map centered around the average location of all players
    center_lat = df_players['Hometown Lat'].mean()
    center_lon = df_players['Hometown Lon'].mean()

    acc_map = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    # prepare data for the heatmap (all players' hometowns)
    heat_data = [
        [row['Hometown Lat'], row['Hometown Lon']]
        for index, row in df_players.iterrows()
        if not pd.isnull(row['Hometown Lat'])
    ]

    # add the heatmap layer with player hometowns
    HeatMap(heat_data).add_to(acc_map)

    # add markers for all schools with logos
    for index, row in df_schools.iterrows():
        logo_path = row['Logo_Path']
        if os.path.exists(logo_path):
            logo_icon = folium.CustomIcon(logo_path, icon_size=(45, 45))  # Adjust size
            folium.Marker(
                location=[row['School Lat'], row['School Lon']],
                popup=row['School'],
                icon=logo_icon
            ).add_to(acc_map)

    # save the map to an HTML file
    map_filename = os.path.join(output_folder, "ACC_and_Schools_Heatmap.html")
    acc_map.save(map_filename)
    print(f"Combined heatmap saved as '{map_filename}'.")

    return acc_map

# generate the combined heatmap for the ACC and other schools
generate_acc_heatmap()

# loop through all schools and generate the map for each school
schools = df_players['School'].unique()
for school in schools:
    generate_heatmap_with_school(school)
