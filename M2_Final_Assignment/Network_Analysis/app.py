import streamlit as st
import pickle
import requests
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import community.community_louvain as community_louvain

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
    Welcome to our Streamlit app tailored for high-energy physics citations. 
    Dive into the world of scientific collaboration within this specialized field. 
    Our streamlined and user-friendly app simplifies the exploration of citation networks, 
    allowing you to visualize connections, analyze citation patterns, and identify influential 
    research effortlessly. Whether you're a physicist, researcher, or simply curious about 
    high-energy physics, our app provides valuable insights into the dynamic landscape of 
    citations in this domain. Join us in uncovering the collaborative spirit and impactful 
    work in high-energy physics through our app.

"""
)

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

######## One-Mode Visualization ########
st.write("## One-Mode Visualization")

st.markdown(
    """
    This is a One-Mode Visualization of the filtered network with the 100 most observed papers.
"""
)

fig = nx.draw(G, with_labels=False, node_size=25)
st.pyplot(fig)


# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

######## Centrality Visualizations ########
st.write("## Centrality Visualizations")

st.markdown(
    """
    Below the size of each paper is weighted by how central each node is for the network.
    Centrality can be calculated using various methods. Below you can select between three different options.
"""
)

central_select = st.selectbox(label = "Select a Centrality Measure",
                              options=['Degree Centrality', 'Betweenness Centrality', 'Eigenvector Centrality'])

G_layout = nx.layout.fruchterman_reingold_layout(G)

if central_select == 'Degree Centrality': 
    st.markdown(
        """
        Degree Centrality is the most intuitive node measure as it just counts the number 
        of adjacent egdes to a node.
        The higher the number of adjacent egdes, the higher centrality.
    """
    )
    node_sizes = [2.5*cent_degree[node] for node in G.nodes()]
    fig1 = nx.draw(G, with_labels=False, node_size=node_sizes)
    st.pyplot(fig1)
elif central_select == 'Betweenness Centrality': 
    st.markdown(
        """
        Betweenness Centrality measures the extend to which a node lies on the shortest path.
        A higher the centrality is an indication of more short paths going through the node, 
        and thus the node is more important for connecting different paths of a network.
    """
    )
    node_sizes = [2.5*cent_between[node] for node in G.nodes()]
    fig2 = nx.draw(G, with_labels=False, node_size=node_sizes)
    st.pyplot(fig2)
elif central_select == 'Eigenvector Centrality': 
    st.markdown(
        """
        Eigenvector Centrality extends the Degree Centrality by including the centrality of 
        the adjacent nodes. This results in nodes which are connected to other important nodes
        having a higher centrality measure. 
    """
    )
    node_sizes = [4.5*cent_eigen[node] for node in G.nodes()]
    fig2 = nx.draw(G, with_labels=False, node_size=node_sizes)
    st.pyplot(fig2)

st.markdown(
    """
    To compare the different centrality measures, you can explore the table below. 
    The table displays the five most central nodes according to each measure.
"""
)
st.dataframe(df_top)

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

######## Community Detection ########
st.write("## Community Detection")

st.markdown(
    """
    Below you can see the identified communities in the network. 
    The communities has been detected using the Louvain Community Detection Algorithm.
    The communities are indexed by node color, while the node size displays the Degree 
    Centrality.
"""
)

com = community_louvain.best_partition(G)
node_colors = [com[node] for node in G.nodes()]
node_sizes = [2.5*cent_degree[node] for node in G.nodes()]
fig3 = nx.draw(G, with_labels=False, node_color = node_colors, node_size=node_sizes)
st.pyplot(fig3)



