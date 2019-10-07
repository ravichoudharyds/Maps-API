from sklearn.neighbors import KDTree
import requests

# Create a KDTree based on the latitude and longitude data from Cabs data
lat_long_tree = KDTree(list(zip(green_cabs_Sep15_df['Pickup_latitude'],green_cabs_Sep15_df['Pickup_longitude'])),metric='manhattan')

def nearest_pickup(customer_location,k):
    
    # Multiple of k points to be queried from the KDTree based on distance 
    max_limit=2
    
    # Please Enter your Bing Maps API Key
    bingMapsKey = ""
    
    # Query max_limit*k points from the KDTree. The Tree returns index of the closest points.
    cab_location_index = lat_long_tree.query(customer_location,k=max_limit*k,return_distance=False)    

    # Use the returned index to create a list of latitude and longitude of closest cabs 
    cab_loc_ravel = np.ravel(list(zip(green_cabs_Sep15_df.loc[cab_location_index[0],'Pickup_latitude'],green_cabs_Sep15_df.loc[cab_location_index[0],'Pickup_longitude'])))
        
    # Number of closest cabs we get from the customer location
    num_cabs = len(cab_location_index[0])
    
    # Create a string of cab latitude and Longitude for the Bing Maps API call
    # Bing Maps API requires the origin latitude and longitude in the following format
    # origins=lat1,long1;lat2,long2;lat3,long3

    str_cab_lat_long = ''

    for i in range(2*num_cabs):
        str_cab_lat_long=str_cab_lat_long+str(cab_loc_ravel[i])
        if i != 2*num_cabs-1:
            if i%2==0:
                str_cab_lat_long=str_cab_lat_long+","
            else:
                str_cab_lat_long=str_cab_lat_long+";"

    cust_long = customer_location[0][1]
    cust_lat = customer_location[0][0]
    
    # Create the final URL for Bing Maps query 
    dist_Url = "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?origins=" + str_cab_lat_long + "&destinations=" + str(cust_lat) + "," + str(cust_long) + "&travelMode=driving&key="+bingMapsKey
    header = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:63.0) Gecko/20100101 Firefox/63.0"}
    
    # Get the JSON data from Bing Maps and process it to get travel duration during driving  
    bingmaps_data = requests.get(dist_Url,headers=header)
    enc_bing_data = bingmaps_data.content.decode(encoding="utf-8")
    json_fmt_bing_data = json.loads(enc_bing_data)
    cab_loc_trip_time=[]
    for i in range(num_cabs):
        cab_loc_trip_time.append(json_fmt_bing_data['resourceSets'][0]['resources'][0]['results'][i]['travelDuration'])

    # We need to get the co-ordinates of the cab locations sorted by trip time
    # Use argsort on trip time to sort the closest cabs index received from KDTree based on trip time 
    cab_sorted_time_index = np.argsort(cab_loc_trip_time)
    sorted_cab_list = list(zip(green_cabs_Sep15_df.loc[cab_location_index[0][cab_sorted_time_index[:k]],'Pickup_latitude'],green_cabs_Sep15_df.loc[cab_location_index[0][cab_sorted_time_index[:k]],'Pickup_longitude']))
    cab_loc_trip_time.sort()
    return sorted_cab_list, cab_loc_trip_time
