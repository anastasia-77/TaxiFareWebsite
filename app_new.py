import streamlit as st  # put to requirements.txt
import pandas as pd     # put to requirements.txt
import numpy as np      # put to requirements.txt

from PIL import Image   # built in lib
import datetime         # built in lib 
import json             # built in lib
import requests         # built in lib

# Add a Header
"""
# New York City Taxi Fare
"""

image = Image.open('new-york-taxis.jpg')
st.image(image, caption='NYC taxis')

'''
## Are you ready to go ?
### Please, enter the number of passengers:
'''

line_count = st.slider('from 1 to 8:', 1, 8, 3)



"""### When do you go:
"""

d = st.date_input("Choose a departure date, please:",
                    datetime.date(2021, 6, 4))

t = st.time_input('Time', datetime.time(14, 00))

"""### Please, enter your pickup longitude:
"""
pickup_longitude = st.number_input('example pickup longitude: -73,98')
st.write('The current number is ', pickup_longitude)

"""### Please, enter your pickup latitude:
"""
pickup_latitude = st.number_input('example pickup latitude: 40,77')
st.write('The current number is ', pickup_latitude)


"""### Please, enter your dropoff longitude:
"""
dropoff_longitude = st.number_input('example pickup longitude: -73,88')
st.write('The current number is ', dropoff_longitude)


"""### Please, enter your dropoff latitude:
"""
dropoff_latitude = st.number_input('example dropoff latitude: 40,78')
st.write('The current number is ', dropoff_latitude)

# to transform latitude and longitude 
geo_url = "https://nominatim.openstreetmap.org"

def get_pickup():
        # Récupérer les points cardinaux de l'adresse de départ
        params = {"q": pickup, "format": "json"}

        response = requests.get(geo_url, params=params).json()
        pickup_longitude = response[0]["lon"]
        pickup_latitude = response[0]["lat"]

        return pickup_longitude, pickup_latitude

def get_dropoff():
        # Récupérer les points cardinaux de l'adresse d'arrivée
        params = {"q": dropoff, "format": "json"}

        response = requests.get(geo_url, params=params).json()
        dropoff_longitude = response[0]["lon"]
        dropoff_latitude = response[0]["lat"]

        return dropoff_longitude, dropoff_latitude

pickup_longitude, pickup_latitude = get_pickup()
dropoff_longitude, dropoff_latitude = get_dropoff()
pickup_datetime = f"{d} {t}"

#---Prediction

params = {"pickup_datetime": pickup_datetime,
          "pickup_longitude": pickup_longitude,
          "pickup_latitude": pickup_latitude,
          "dropoff_longitude": dropoff_longitude,
          "dropoff_latitude": dropoff_latitude,
          "passenger_count": line_count}

@st.cache
def get_predict():
    
    # my_url = 'https://docker-tfm-ipbs6r3hdq-ew.a.run.app/predict'
    my_url = 'https://api-ipbs6r3hdq-ew.a.run.app/predict'
    url_wagon = 'https://taxifare.lewagon.ai/predict'
    
    response = requests.get(url_wagon, params=params) # my_url
    taxi_fare = response.json()
    
    return round(taxi_fare['fare'], 2) #prediction


st.write('Taxi fare:' + str(get_predict()) + "$")

#---Map

@st.cache
def get_map_data():
    print('get_map_data called')
    return pd.DataFrame([[float(pickup_latitude), float(pickup_longitude)],
                        [float(dropoff_latitude), float(dropoff_longitude)]])

st.map(get_map_data())

# else:
#     from PIL import Image
#     image = Image.open('')
#     st.image(image, caption='map', use_column_width=False)

st.markdown("""# Lets start your trip !""")

if st.button('More 🎈🎈🎈 please!'):
    st.balloons()