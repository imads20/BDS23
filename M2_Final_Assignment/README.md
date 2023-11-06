This ZIP-file contains 2 folders, which is Natural_Language_Processing and Network_Analysis. Each of these folders contains its respective part of the assignment for the M2 module!

The Natural_Language_Processing folder contains the following:

NLP.ipynb
The NLP.ipynb is a Python file which contains the analysis of the Medical Bios by CoastalCPH. This file creates a SML model which will predict professions given a written bio. 

app.py
The python file app.py contains information from NLP. ipynb   and uses this information to deploy a Gradio App. The link for this app can be found in the bottom of this textfile. 

requirements.txt
This txt file contains the necessary packages which must be downloaded and installed before the Gradio app can run.

components
The components folder contains 2 files, df.json and pipe_log.pkl. This is a json and a pickle file, which is the components saved from the NLP.ipynb file which is used in the app.py file.

The Network_Analysis folder contains the following:

NWA.ipynb
The NWA.ipynb  is a Python file which contains the analysis of the High-Energy Physics theory Citation Network.

app.py
The python file app.py contains information from NWA.ipynb and deploys the finding from this file on a streamlit app. This makes the network analysis easy to access. The link for this app can be found in the bottom of this text file. 

requirements.txt
This txt file contains the necessary packages which must be downloaded and installed before the Streamlit app can run.

components
The components folder contains 2 files, df_res.json and pipe_log.pkl. This is a json and a pickle file, which is the components saved from the NLP.ipynb file which is used in the app.py file.


Lastly, the different links which is used for this assignment. 

The first link is for the Gradio app demo:
https://panopto.aau.dk/Panopto/Pages/Viewer.aspx?id=2625b954-c87d-424f-9b78-b0b1012c27b6&start=0

The second link is for the streamlit app:
https://bds-m2-exam-assignment.streamlit.app

The third and final link is for the GitHub page which the information/files are uploaded to: 
https://github.com/imads20/BDS23/tree/main/M2_Final_Assignment
