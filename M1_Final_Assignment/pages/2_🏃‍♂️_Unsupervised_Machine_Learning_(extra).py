import streamlit as st
import pandas as pd
import pickle
import requests
import itertools


st.set_page_config(
    page_title="UML",
    page_icon="🛫",
)

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

# Function for loading model components
@st.cache_data  # Cache the function to enhance performance
def load_components():

    # Define path of components
    path = 'https://raw.githubusercontent.com/imads20/BDS23/main/M1_Final_Assignment/model_components/'

    # Load the components
    df = pd.read_json(path + 'df.json')

    # For pickle files we first need to download the files onto the server as pickle is only designed to get files locally. 
    # To do this we have made a function, which we can apply
    euclidean_matrix = get_pickle("euclidean_matrix.pkl", path)

    return df, euclidean_matrix

df, euclidean_matrix = load_components()
st.write("# Unsupervised Machine Learning")

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)