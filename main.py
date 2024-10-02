import os  # Import the os module
import json
import pygame
import urllib.request
import time
import webbrowser
import geocoder
from datetime import date

from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%H:%M:%S")
print("Current Time: ", dt_string)

# Initialize pygame
pygame.init()

# Set the folder path where your images are located
image_folder = "/Users/abdullahisaid/Desktop/2024/Python Projects/Tracking ISS Python"  # Replace with the actual folder path

# Create a screen (window) for the map
screen = pygame.display.set_mode((1280, 720))

# Set up the world coordinates
world_map = pygame.image.load(os.path.join(image_folder, "map.gif"))  # Use os.path.join to construct the full path
world_rect = world_map.get_rect()

# Set up the ISS image
iss = pygame.image.load(os.path.join(image_folder, "iss.gif"))  # Use os.path.join to construct the full path
iss_rect = iss.get_rect()

# Free API
url = "http://api.open-notify.org/astros.json"

# Opening the URL using the request module
response = urllib.request.urlopen(url)

# Loading the JSON file (reading it)
result = json.loads(response.read())

# Opening the text file
file = open("iss.txt", "w")
file.write("There are currently " +
            str(result["number"]) + " astronauts on the ISS: \n\n")
people = result["people"]
for p in people:
    file.write(p['name'] + " - on board" + "\n")

# Get the current lat/long
g = geocoder.ip('me')
file.write("\nYour current lat / long is: " + str(g.latlng))
file.close()
webbrowser.open("iss.txt")



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()



    # Load the current status of the ISS in real-time
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    # Extract the ISS location
    location = result["iss_position"]
    lat = location['latitude']
    lon = location['longitude']

    # Output lon and lat to the terminal
    lat = float(lat)
    lon = float(lon)
    print("\nLatitude: " + str(lat))
    print("\nLongitude: " + str(lon))

    # Update the ISS location on the map
    iss_rect.centerx = (180 + lon) * (1280 / 360)
    iss_rect.centery = (90 - lat) * (720 / 180)

    # Clear the screen and draw the map and ISS
    screen.fill((255, 255, 255))
    screen.blit(world_map, world_rect)
    screen.blit(iss, iss_rect)
    pygame.display.flip()

    # Refresh every 5 seconds
    time.sleep(5)

