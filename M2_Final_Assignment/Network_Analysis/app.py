import streamlit as st
import pickle
import requests
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Remove warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

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

# Function for loading components
@st.cache_data  # Cache the function to enhance performance
def load_components():

    # Define path of components
    path = 'https://raw.githubusercontent.com/imads20/BDS23/main/M2_Final_Assignment/Network_Analysis/components/'

    # For pickle files we first need to download the files onto the server as pickle is only designed to get files locally. 
    # To do this we have made a function, which we can apply
    G = get_pickle("G.pkl", path)
    cent_degree = get_pickle("cent_degree.pkl", path)
    cent_between = get_pickle("cent_between.pkl", path)
    cent_eigen = get_pickle("cent_eigen.pkl", path)

    df_top = pd.read_json(path + 'df_top.json')

    return G, cent_degree, cent_between, cent_eigen, df_top

G, cent_degree, cent_between, cent_eigen, df_top = load_components()

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

######## One-Mode Visualization ########
st.write("## One-Mode Visualization")

fig = nx.draw(G, with_labels=False, node_size=25)
st.pyplot(fig)


# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

######## Centrality Visualizations ########
st.write("## Centrality Visualizations")

central_select = st.selectbox(label = "Centrality Measure",
                              options=['Degree Centrality', 'Betweenness Centrality', 'Eigenvector Centrality'])

G_layout = nx.layout.fruchterman_reingold_layout(G)

if central_select == 'Degree Centrality': 
    node_sizes = [2.5*cent_degree[node] for node in G.nodes()]
    fig1 = nx.draw(G, with_labels=False, node_size=node_sizes)
    st.pyplot(fig1)
elif central_select == 'Betweenness Centrality': 
    node_sizes = [2.5*cent_between[node] for node in G.nodes()]
    fig2 = nx.draw(G, with_labels=False, node_size=node_sizes)
    st.pyplot(fig2)
elif central_select == 'Eigenvector Centrality': 
    node_sizes = [4.5*cent_eigen[node] for node in G.nodes()]
    fig2 = nx.draw(G, with_labels=False, node_size=node_sizes)
    st.pyplot(fig2)

st.dataframe(df_top)