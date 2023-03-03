import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
ss=StandardScaler()
import pickle
st.title('Host Optimal Price Prediction')

# Load Model

rf_model=pickle.load(open('airbnb.pickle','rb'))





host_is_superhost=str(st.radio('Superhost ?',options=['Yes','No']))
host_identity_verified=str(st.radio('ID Verified ?',options=['Yes','No']))
instant_bookable=str(st.radio('Instantly bookable ?',options=['Yes','No']))

review_dict={'Recent':1,'Unknown':2}
room_dict={'Hotel room':1,'Shared room':2,'Private room':3}
host_dict={'Middle Term':1,'Novice':2}
region_dict={'North East':1,'South East':2,'West':3}
neighbourhood_dict={'DC':1,'FL':2,'HI':3,'IL':4,'NV':5,'NY':6,'TN':7,'WA':8}
budget_dict={'Moderate':1,'High':2,'Luxury':3}

room_type=st.radio('Room type',tuple(room_dict.keys()))
review_category=st.radio('Review period',tuple(review_dict.keys()))
host_rank=st.radio('Host ranking',tuple(host_dict.keys()))
Region=st.radio('Select your region of interest',tuple(region_dict.keys()))
neighbourhood_state=st.radio('Select your neighbourhood of interest',tuple(neighbourhood_dict.keys()))
property_budget=st.radio('What is your budget?',tuple(budget_dict.keys()))



accommodates=st.number_input('Number of accomodates',0,16,key='1')
bathrooms=st.number_input('Number of bathrooms',0,50,1,key='2')
bedrooms=st.number_input('Number of bedrooms',0,50,1,key='3')
beds=st.number_input('Number of beds',0,66,1,key='4')
minimum_nights=st.number_input('Minimum number of nights',1,100000000,1,key='5')
maximum_nights=st.number_input('Maximum number of nights',1,2147483647,1,key='6')
availability_365=st.number_input('Days of availability',0,365,1,key='7')
amenities_count=st.number_input('Number of amenities',0,24,1,key='8')
latitude=22.0515
longitude=-159.33409
number_of_reviews=10
calculated_host_listings_count=0.01298701
host_months=100
neighborhood_market=500
property_rate=173
amenities_score=1.89859016


host_is_superhost= 1 if host_is_superhost=='t' else 0
host_identity_verified= 1 if host_identity_verified=='t' else 0
instant_bookable= 1 if instant_bookable=='t' else 0

hotel,private,shared = 0,0,0
if room_type=='Hotel room':
    hotel=1
elif room_type=='Shared room':
    shared=1
else:
    private=1
    
recent, unknown= 0,0
if review_category=='Recent':
    recent=1
else:
    unknown=1
    
mid, nov=0,0
if host_rank=='Middle Term':
    mid=1
else:
    nov=1
    
ne, se, w =0,0,0
if Region=='North East':
    ne=1
elif Region=='South East':
    se=1
else:
    w=1
    
dc, fl, hi, il, nv, ny, tn, wa= 0,0,0,0,0,0,0,0
if neighbourhood_state=='DC':
    dc=1
elif neighbourhood_state=='FL':
    fl=1
elif neighbourhood_state=='HI':
    hi=1
elif neighbourhood_state=='IL':
    il=1
elif neighbourhood_state=='NV':
    nv=1
elif neighbourhood_state=='NY':
    ny=1
elif neighbourhood_state=='TN':
    tn=1
else:
    wa=1
    
mod, high, lux= 0,0,0
if property_budget=='Moderate':
    mod=1
if property_budget=='High':
    high=1
else:
    lux=1
    
    
    
d1={'host_is_superhost':host_is_superhost,
            'host_identity_verified':host_identity_verified,
            'instant_bookable':instant_bookable,
            'room_type':[hotel,private,shared],
            'review_category':[recent, unknown],
            'host_rank':[mid, nov],
            'Region':[ne, se, w], 
            'neighbourhood_state':[dc, fl, hi, il, nv, ny, tn, wa],
            'property_budget':[mod, high, lux],
            'accommodates':accommodates,
            'bathrooms':bathrooms, 
            'bedrooms':bedrooms,
            'beds':beds, 
            'minimum_nights':minimum_nights, 
            'maximum_nights':maximum_nights, 
            'availability_365':availability_365,  
            'amenities_count':amenities_count}

features=[host_is_superhost,
            host_identity_verified,
            instant_bookable,
            d1['room_type'][0],d1['room_type'][1],d1['room_type'][2],
            d1['review_category'][0],d1['review_category'][1],
            d1['host_rank'][0],d1['host_rank'][1],
            d1['Region'][0],d1['Region'][1],d1['Region'][2],
            d1['neighbourhood_state'][0],d1['neighbourhood_state'][1],d1['neighbourhood_state'][2],
            d1['neighbourhood_state'][3],d1['neighbourhood_state'][4],d1['neighbourhood_state'][5],
            d1['neighbourhood_state'][6],d1['neighbourhood_state'][7],
            d1['property_budget'][0],d1['property_budget'][1],d1['property_budget'][2],
            accommodates,bathrooms, bedrooms,beds, minimum_nights, 
          maximum_nights, availability_365,  amenities_count, latitude, longitude, number_of_reviews,
       calculated_host_listings_count, host_months, neighborhood_market,
       property_rate, amenities_score]


sample=np.array(features).reshape(1,-1)

predictions=rf_model.predict(sample)
st.subheader('Host Price')
if st.button('Predict'):
    st.write(predictions)
