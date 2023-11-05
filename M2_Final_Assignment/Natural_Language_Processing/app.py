import gradio as gr
import pickle
import pandas as pd
import requests
import preprocessor as prepro
import spacy 
nlp = spacy.load('en_core_web_sm') 
from lime.lime_text import LimeTextExplainer 
import plotly.express as px


# Load components
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

# Define path of components
path = 'https://raw.githubusercontent.com/imads20/BDS23/main/M2_Final_Assignment/Natural_Language_Processing/components/'

# For pickle file we first need to download the files onto the server as pickle is only designed to get files locally. 
# To do this we have made a function, which we can apply
pipe_log = get_pickle("pipe_log.pkl", path)



# Make function for text preprocessing
prepro.set_options(prepro.OPT.URL, # removes URLs
                   prepro.OPT.NUMBER, # removes numbers
                   prepro.OPT.RESERVED, # removes reserved words
                   prepro.OPT.MENTION, # removes any mentions
                   prepro.OPT.SMILEY) # removes emojis

def text_prepro(texts: pd.Series) -> list:
    """
    Preprocess a series of texts.

    Parameters:
    - texts: A pandas Series containing the text to be preprocessed.
    - nlp: A spaCy NLP model.

    Returns:
    - A list of preprocessed texts.

    Steps:
    - Clean twitter-specific characters using a predefined 'prepro' method.
    - Normalize the text by lowercasing and lemmatizing.
    - Remove punctuations, stopwords, and non-alphabet characters.
    """

    # Clean specific characters and other special characters
    texts_cleaned = texts.map(prepro.clean)
    texts_cleaned = texts_cleaned.str.replace('#', '')

    # Initialize container for the cleaned texts
    clean_container = []

    # Use spaCy's nlp.pipe for efficient text processing
    for doc in nlp.pipe(texts_cleaned, disable=["tagger", "parser", "ner"]):

        # Extract lemmatized tokens that are not punctuations, stopwords, or non-alphabetic characters
        tokens = [token.lemma_.lower() for token in doc # make into lower characters
                  if token.is_alpha # only take alphabetic characters
                  and not token.is_stop # remove stopwords
                  and not token.is_punct] # remove punctuation 

        clean_container.append(" ".join(tokens))

    return clean_container

def lime_plot(text):
  # Clean the text using the predefined function of text preprocessing
  text_cleaned = []
  text_cleaned = text_prepro(pd.Series(text))

  class_names = ['psychologist', 'surgeon', 'nurse', 'dentist', 'physician']
  explainer = LimeTextExplainer(class_names = class_names)
  
  exp = explainer.explain_instance(text_cleaned[0], pipe_log.predict_proba,
                                   num_features = 5, # how many words should be displayed that are significant for the model's reasoning
                                   top_labels=3) # only show the top 3 labels 
  
  lime_values = exp.as_list()

  features, values = zip(*lime_values)

  data = pd.DataFrame()
  data['Word'] = features
  data['Value'] = values
  
  # create a new plot
  p = px.bar(data, x='Word', y='Value')

  return p

# Build function
def classify_label(text):
  # Clean the text using the predefined function of text preprocessing
  text_cleaned = []
  text_cleaned = text_prepro(pd.Series(text))

  # Based on the cleaned text, figure out which label the bio most likely belongs to
  result = pipe_log.predict(text_cleaned)

  # Find the probablilty of how likely it is to belong to this class
  result2= pipe_log.predict_proba(text_cleaned)

  # Get plot of lime values
  p = lime_plot(text)

  if result == 0:
    return "Psychologist, " "probability = " + str(result2[0][0].round(2)), p
  if result == 1:
    return "Surgeon, " "probability = " + str(result2[0][1].round(2)), p
  if result == 2:
    return "Nurse, " "probability = " + str(result2[0][2].round(2)), p
  if result == 3:
    return "Dentist, " "probability = " + str(result2[0][3].round(2)), p
  if result == 4:
    return "Physician, " "probability = " + str(result2[0][4].round(2)), p



#text = 'He had been at the hospital for many years and was quite efficient with his scalpel'

# Define interface for app
demo = gr.Interface(fn=classify_label, 
                    inputs=[gr.Textbox(label = "Insert bio to find medical profession")], 
                    outputs=[
                       gr.Text(label='Profession'), 
                       gr.Plot(label='Lime values')
                       ],
                    title="Find Medical Profession")

demo.launch(share=True)