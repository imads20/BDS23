import streamlit as st
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
import pickle
import requests
import itertools


st.set_page_config(
    page_title="SML",
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
    model_rf = get_pickle("model_rf.pkl", path)
    scaler = get_pickle("scaler.pkl", path)
    ohe = get_pickle("ohe.pkl", path)
    le = get_pickle("le.pkl", path)

    return model_rf, scaler, df, ohe, le

model_rf, scaler, df, ohe, le = load_components()



# Create pipeline for making predictions
def predict_price(airline, duration, distance, stop, city_from, city_to, dep_time, 
                  arr_time, price=0):

    airline = le.transform([airline])
    
    city_from = "from_" + city_from
    city_to = 'to_' + city_to
    dep_time = "dep_" + dep_time
    arr_time = "arr_" + arr_time
    
    cats = list(itertools.chain(*ohe.categories_))

    new_cat = pd.DataFrame({'to':city_to,
                            'from': city_from,
                            'dep_time': dep_time,
                            'arr_time': arr_time}, index=[0])
    new_values_cat = pd.DataFrame(ohe.transform(new_cat), columns = cats, index=[0])
    
    new_num = pd.DataFrame({
      'price': [price],
      'airline':[airline],
      'distance':[distance],
      'duration_minutes':[duration],
      'stop':[stop],
      })

    new_values_num = pd.DataFrame(scaler.transform(new_num), columns = new_num.columns, index=[0])
    new_values_num = new_values_num.drop('price', axis=1) 

    line_to_pred = new_values_num.join(new_values_cat)
    prediction = model_rf.predict(line_to_pred)

    prediction_value = prediction[0].round(2)

    string = f"Estimated flight price is {prediction_value} INR"

    return string


st.write("# Supervised Machine Learning")

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

with st.expander("Click to learn more about the model"):
    st.markdown(
        'This is some text explaning our model'
    )

# Input fields for stop and duration
selected_airline = st.selectbox("Select Airline 🌏", ['Air India', 'Vistara'])
selected_from = st.selectbox("Select Departure 🌏", df['from'].unique().tolist())
selected_to = st.selectbox("Select Destination 🌏", df['to'].unique().tolist())
selected_dep = st.selectbox("Select Departure Time 🌏", df['dep_time'].unique().tolist())
selected_arr = st.selectbox("Select Arrival Time 🌏", df['arr_time'].unique().tolist())
selected_stop = st.number_input("Select Number of Stops", min_value=0, max_value=2, step=1, value=1)
selected_distance = st.number_input("Select Distance", min_value=250, max_value=2000, step=50, value=1000)
selected_duration = st.number_input("Select Duration (minutes)", min_value=120, max_value=1800, step=30, value=360)

# Button to trigger price estimation
if st.button("Estimate Flight Price"):
    result = predict_price(airline=selected_airline, 
                           duration=selected_duration, 
                           distance=selected_distance, 
                           stop=selected_stop, 
                           city_from=selected_from, 
                           city_to=selected_to, 
                           dep_time=selected_dep, 
                           arr_time=selected_arr)
    st.write(result)