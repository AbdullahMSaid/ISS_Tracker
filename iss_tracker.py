import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import time
import os

# Page setup
st.set_page_config(page_title="Real-Time ISS Tracker", layout="wide")

# Title and header
st.title("Real-Time ISS Tracker 🌍")
st.markdown("This app tracks the current position of the International Space Station (ISS) in real-time.")

# Define function to get ISS current location
def get_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()
    return data

# Get the current ISS location
iss_data = get_iss_location()
iss_position = iss_data['iss_position']
iss_lat = float(iss_position['latitude'])
iss_lon = float(iss_position['longitude'])

# Display the ISS position
st.write(f"**Current Latitude**: {iss_lat}")
st.write(f"**Current Longitude**: {iss_lon}")

# Create a map centered around the ISS
map_center = [iss_lat, iss_lon]
m = folium.Map(location=map_center, zoom_start=2)

# Define the file path for the custom icon (make sure this path is correct)
iss_icon_path = os.path.join(os.getcwd(), "iss.gif")  # Assuming iss.gif is in the current directory

# Step 1: Initialize a Folium map centered on an approximate ISS starting position
m = folium.Map(location=[0, 0], zoom_start=2)

# Step 2: Add the marker to the map using the ISS icon
folium.Marker(
    location=[0, 0],  # Starting position for the ISS marker (latitude, longitude)
    icon=folium.CustomIcon(icon_image=iss_icon_path, icon_size=(30, 30)),  # Adjust size as needed
    popup="International Space Station",
).add_to(m)


# Save the map to an HTML file
m.save("iss_map.html")






# Display the map
st_data = st_folium(m, width=725, height=500)

# Sidebar: Show astronauts on the ISS
st.sidebar.header("Astronauts Currently on the ISS")
url = "http://api.open-notify.org/astros.json"
response = requests.get(url)
astronaut_data = response.json()
number_of_astronauts = astronaut_data['number']
st.sidebar.write(f"**Number of astronauts on board**: {number_of_astronauts}")

# List of astronauts
people = astronaut_data["people"]
astronaut_names = pd.DataFrame(people, columns=["name", "craft"])
st.sidebar.table(astronaut_names)

# Footer information
st.markdown("---")
st.markdown("**Note**: This application uses data from the public [Open Notify API](http://open-notify.org/Open-Notify-API/) to get real-time ISS information.")
