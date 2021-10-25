import streamlit as st
import pandas as pd
import base64
import requests
import json
import os


st.set_page_config(page_title="Churn Rate Prediction", 
                   page_icon=":robot_face:",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

st.write('''# *Client Churn Predictor*''')


uploaded_file = st.file_uploader("Upload a CSV file", type="csv")


THRESHOLD = 0.22
OUTPUT = 'Churn(output)'
URL = '{}/api/v1/predict'.format(os.environ['host'])

def predict(data):
    data = data[1].values.flatten().tolist()
    data = str(data)
    resp = requests.post(URL,data=data)
    json_data = json.loads(resp.text)
    prediction = float(json_data["prediction"][0])
    return prediction

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    st.write(
    '''
    ### Input Data ({} Customers)
    '''.format(input_df.shape[0])
    )
    st.dataframe(input_df)
    st.write('')

    # Remove output column in test set
    if OUTPUT in input_df.columns:
        X = input_df.drop([OUTPUT],axis=1)

    ix_list = []
    for ix,row in enumerate(X.iterrows()):
        if predict(row) >= THRESHOLD:
            ix_list.append(ix)
    

    
    st.write('''### Number of Potentially Churning Customers''')
    st.write('''There are **{} customers** at risk of closing their accounts.'''.format(len(ix_list)))

    csv = input_df.iloc[ix_list].to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.write('''''')
    st.write('''''')
    st.write('''### **⬇️ Download At-Risk Customer Information's**''')
    href = f'<a href="data:file/csv;base64,{b64}" download="at_risk_customer.csv">Download csv file</a>'
    st.write(href, unsafe_allow_html=True)