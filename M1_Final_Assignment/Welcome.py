import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Welcome",
    page_icon="🛫",
)

st.write("# Welcome to Business Class Flight Price Predictor! 🛫")

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

image = "https://raw.githubusercontent.com/imads20/BDS23/main/M1_Final_Assignment/corgi_welcome.png"
st.image(image)

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

