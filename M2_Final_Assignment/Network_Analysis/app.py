import streamlit as st
import pickle
import requests

def get_pickle(filename, path):
    # Function for downloading pickle files

    # To download the data we use request library: 
    url = path + filename
    response = requests.get(url)

    # Afterward we check if the request was successful (status code 200)
    if response.status_code == 200:
        # Load the pickled model from the content
        file = pickle.loads(response.content)
    else:
        print('Failed to retrieve the pickle file.')
    
    return file

st.title("High-Energy Physics Citation Network")

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

st.markdown(
    """
    Greetings

    We are delighted to introduce our Flight Price Prediction Tool.

    Within this elegant Streamlit application, you will discover a comprehensive analysis dedicated to the realm of business class 
    flight fares. This analytical resource grants you valuable insights into the factors that influence flight prices, equipping 
    your esteemed organization with a strategic advantage in the competitive marketplace. To access our cutting-edge prediction 
    model, kindly navigate to the "Flight Price Predictor" tab.

    Our dedicated team takes immense pride in presenting this predictive model, and we trust it will deliver substantial value to 
    your discerning needs. Should our work resonate with your discerning taste, please do not hesitate to engage with us for a 
    tailored data handling proposal tailored to your company's distinctive requirements.

"""
)

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

st.write("## One-Mode Visualization")
