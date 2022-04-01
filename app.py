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

#---Prediction

pickup_datetime = f"{d} {t}"

params = {
            "pickup_datetime": pickup_datetime,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": line_count
            }

@st.cache
def get_predict():
    
    # my_url = 'https://docker-tfm-ipbs6r3hdq-ew.a.run.app/predict'
    my_url = 'https://api-ipbs6r3hdq-ew.a.run.app/predict'
    url_wagon = 'https://taxifare.lewagon.ai/predict'
    response = requests.get(url_wagon, params=params) # my_url
    taxi_fare = response.json()
    return round(taxi_fare['fare'], 2) #prediction

"""### Your Taxi Fare $$: 
"""
st.write('', get_predict())

#---Map

@st.cache
def get_map_data():
    print('get_map_data called')
    return pd.DataFrame(
            np.random.randn(1, 2) / [50, 50] + [40.75, -73.98],
            columns=['lat', 'lon']
        )


df = get_map_data()
st.map(df)

# else:
#     from PIL import Image
#     image = Image.open('')
#     st.image(image, caption='map', use_column_width=False)

st.markdown("""# Lets start your trip !""")

if st.button('More 🎈🎈🎈 please!'):
    st.balloons()