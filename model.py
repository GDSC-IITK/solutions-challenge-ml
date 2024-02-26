from flask import Flask, jsonify, request
import pandas as pd
from sklearn.cluster import KMeans

rest = pd.read_csv('restaurants.csv')
kiosk = pd.read_csv('coordinates_output.csv')

rest = rest[(rest['longitudes'] >= 88) & (rest['latitudes'] <= 23)]

kiosk.columns = ['latitudes', 'longitudes']
combined = pd.concat([rest, kiosk])
combined['labels'] = ['rest'] * len(rest) + ['kiosk'] * len(kiosk)

def find_same_kiosks(df, latitude, longitude, k):
    latitude = float(latitude)
    longitude = float(longitude)
    km = KMeans(n_clusters=k)
    X = df[['latitudes', 'longitudes']].values
    y_pre = km.fit_predict(X)
    df['map'] = y_pre

    # Define tolerance for float comparison
    tolerance = 1e-6

    # Check if any row satisfies the condition within tolerance
    filtered_df = df[(abs(df['latitudes'] - latitude) < tolerance) & 
                     (abs(df['longitudes'] - longitude) < tolerance)]
    if(filtered_df.empty==1):
        return []
    restaurant_number = filtered_df['map'].iloc[0]

    same_kiosks = df[(df['labels'] == 'kiosk') & (df['map'] == restaurant_number)]

    kiosk_latitudes = same_kiosks['latitudes'].tolist()
    kiosk_longitudes = same_kiosks['longitudes'].tolist()
    lat_lon_strings = [f"{lat},{lon}" for lat, lon in zip(kiosk_latitudes, kiosk_longitudes)]
    if(len(lat_lon_strings)<5 and len(lat_lon_strings)>0):
        return lat_lon_strings
    else : 
        return lat_lon_strings[:5]



# print(find_same_kiosks(combined,22.5080547, 88.3533289, 5))

# app = Flask(__name__)
# @app.route('/users/<string:username>')
# def hello_world(username=None):
#     s = ""
#     try:
#         l = find_same_kiosks(combined,  'Chinese Food Corner', 3)
#         test = 0
#         for i in l:
#             test += 1
#             s += str(i) + " |\n"
#             if test == 5:
#                 break
#     except:
#         s = "No nearby restaurant found"
#     return(s)

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

@app.route('/kiosks')
def get_kiosks():
    # Extract latitude and longitude from query parameters as strings
    latitude_str = request.args.get('lat', default=None, type=str)
    longitude_str = request.args.get('lon', default=None, type=str)

    lat_lon_list= find_same_kiosks(combined, latitude_str, longitude_str, 5)
    print(lat_lon_list)
    if len(lat_lon_list) == 0 :
        return jsonify({"error": "No kiosks found for the given coordinates."}), 404

    # Convert string coordinates to tuples of floats (if needed)
    coordinates = [tuple(map(float, coord.split(','))) for coord in lat_lon_list]
    
    # Return a JSON response containing the coordinates
    return jsonify(coordinates)
