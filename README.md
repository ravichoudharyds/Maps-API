This repository was created to test and use Google Maps API and Bing Maps API. This repository has 2 python files with a function in each one. 

The get_boro_name.py file has a function to get Borough names of a NYC Latitude and Longitude data using Google Maps API. If the location is not present in NYC according to Google Maps, it returns "Not NYC".

The Nearest_Pickup.py file creates a KDTree based on a given list of of Latitude and Longitude data. For my use case I used NYC Taxi dataset which gives us a KDTree of NYC Taxi Pickup locations. The file also has a function which gives a list of closest pickup locations from a given latitude and longitude using Manhattan distance and trip time calculated using Bing Maps API. 
