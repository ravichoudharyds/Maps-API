import googlemaps
import json

# Add your own Google Maps API
gmaps = googlemaps.Client(key='')
borough_list = ['Queens','Brooklyn','Bronx','Manhattan','Staten Island']

# Function to get Borough Names
def get_boro_name(lat,long):
    
    # Get the JSON address data from Google Maps reverse geocode
    json_address_data = gmaps.reverse_geocode((lat,long))
    
    # Check if any of the top 5 address component part of the JSON has one of borough names.
    # If matched return the Boro Name, Else return Not NYC
    for i in range(5):
        if json_address_data[0]['address_components'][i]['long_name'] in borough_list:
            return pickup_location_json.loc[row][0]['address_components'][i]['long_name']
    return 'Not NYC'

# Apply the function on each row
pickup_location_json = model_data.apply(lambda x: get_boro_name(x['pickup_latitude'],x['pickup_longitude']),axis=1)
dropoff_location_json = model_data.apply(lambda x : get_boro_name((x['Dropoff_latitude'],x['Dropoff_longitude'])), axis=1)    
