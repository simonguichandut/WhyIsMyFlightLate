"""
# App
Will my flight be late?
"""

debug = False

import streamlit as st
import pandas as pd
import datetime
import app_interface

##############################################################
# Load ressources with proper caching

@st.cache_data
def load_airports_carriers():
    airport_stats = pd.read_csv("data/airport_stats.csv", nrows=21)
    carrier_stats = pd.read_csv("data/carrier_stats.csv")

    # Airports and carriers trained on
    # Copied from data/Get_clean_dataset.py
    airport_ids = [10397,13930,11298,11292,12892,14107,14771,11057,12266,12889,14747,13487,11433,13204,10721,12953,11618,12478,14869,11278]
    carrier_codes = ['WN','DL','AA','OO','UA','B6','AS','NK']

    # Convert to names using the stats file
    airport_names = [airport_stats.loc[airport_stats['ID']==id, 'Name'].values[0] for id in airport_ids]
    carrier_names = [carrier_stats.loc[carrier_stats['Code']==c, 'Name'].values[0] for c in carrier_codes]

    return airport_stats, carrier_stats, airport_ids, carrier_codes, airport_names, carrier_names

airport_stats, carrier_stats, airport_ids, carrier_codes, airport_names, carrier_names = load_airports_carriers()

@st.cache_resource
def load_model():
    return app_interface.load_model()
model = load_model()

@st.cache_data
def predict(_model, air_time, carrier_, origin_, dest_, datetime_, carrier_codes, airport_ids):  # underscode before model because cant hash it
    return app_interface.predict(_model, air_time, carrier_, origin_, dest_, datetime_, carrier_codes, airport_ids)

##############################################################
# Main program

st.title("Will My Flight Be Late?")

#flight = st.text_input("Your flight number: ")

col1,col2 = st.columns(2)

with col1:
    carrier = st.selectbox(
            "Flight carrier",
            carrier_names,
            index=None,
            placeholder="Select carrier")

    orig = st.selectbox(
            "Origin Airport",
            airport_names,
            index=None,
            placeholder="Select airport")

    dest = st.selectbox(
            "Destination Airport",
            airport_names,
            index=None,
            placeholder="Select airport")

with col2:
    date = st.date_input("Flight Date", value=None)
    time = st.time_input("Departure Time", value=None)
    airtime = st.slider("Flight duration (hours)", 0.5, 12., value=1., step=0.25)

if carrier:
    carrier_code = carrier_stats.loc[carrier_stats['Name']==carrier, 'Code'].values[0]
    # carrier_code = carriers[carrier]
if orig:
    orig_id = airport_stats.loc[airport_stats['Name']==orig, 'ID'].values[0]
    # orig_id = airports[orig]
if dest:
    dest_id = airport_stats.loc[airport_stats['Name']==dest, 'ID'].values[0]
    # dest_id = airports[dest]
if date and time:
    full_datetime = datetime.datetime.combine(date,time)

check_button = st.button("Evaluate", type="primary")

def check():

    # Escape if info is not entered
    if carrier is None or orig is None or dest is None or date is None or time is None:
        st.write("Enter all info!")
        return
    
    # Testing input
    if debug:
        st.write(carrier,':', carrier_code)
        st.write(orig,':', orig_id)
        st.write(dest,':', dest_id)
        st.write(date,time, full_datetime)
        st.write(airtime)

    # import random
    # if random.random() > 0.5:
    if predict(model, airtime, carrier_code, orig_id, dest_id, full_datetime, carrier_codes, airport_ids):
        st.markdown("<h1 style='text-align: center; color: red;'>YES!</h1>", unsafe_allow_html=True)
        st.text("Our model thinks your flight will be more than 15 minutes late")
    else:
        st.markdown("<h1 style='text-align: center; color: green;'>NO!</h1>", unsafe_allow_html=True)
        st.text("Our model thinks your flight will not be late by more than 15 minutes.")


    with st.expander("Statistics about your flight:"):
        st.write("Over the last 10 years (but excluding pandemic years):")

        st.markdown(":red[%.0f%%] of flights from your carrier have been delayed (:red[%.0f%%] in 2023 only)"%\
                    (carrier_stats.loc[carrier_stats['Name']==carrier, 'delay_frac'].values[0]*100,
                    carrier_stats.loc[carrier_stats['Name']==carrier, 'delay_frac_2023'].values[0]*100))
        
        st.markdown(":red[%.0f%%] of flights from your origin have been delayed (:red[%.0f%%] in 2023 only)"%\
                    (airport_stats.loc[airport_stats['Name']==orig, 'delay_frac_from'].values[0]*100,
                    airport_stats.loc[airport_stats['Name']==orig, 'delay_frac_from_2023'].values[0]*100))
        
        st.markdown(":red[%.0f%%] of flights to your destination have been delayed (:red[%.0f%%] in 2023 only)"%\
                    (airport_stats.loc[airport_stats['Name']==dest, 'delay_frac_to'].values[0]*100,
                    airport_stats.loc[airport_stats['Name']==dest, 'delay_frac_to_2023'].values[0]*100))

if check_button: check()

# About section
st.markdown("### About this app")
st.write("Current model: Random Forest with 10 estimators")
st.markdown("By [Ketan Sand](https://www.linkedin.com/in/ketansand/), [Simon Guichandut](https://www.linkedin.com/in/simonguichandut/) and [Tim Hallatt](https://www.linkedin.com/in/tim-hallatt-904539273/).")
st.write("We thank the Erdös Institute and our mentor Gleb Zhelezov.")
