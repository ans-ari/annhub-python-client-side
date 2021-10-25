import streamlit as st
import pandas as pd
import base64
import requests
import json
import os


st.set_page_config(page_title="Sale Price Prediction", 
                   page_icon=":robot_face:",
                   layout="wide",
                   initial_sidebar_state="expanded"
                   )

st.write('''# *Sale Price Prediction*''')


uploaded_file = st.file_uploader("Upload a CSV file", type="csv")


OUTPUT = 'total_earnings (output)'
URL = '{}/api/v1/predict'.format('http://18.140.115.149:8080')

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
    ### Input Data ({} Records)
    '''.format(input_df.shape[0])
    )
    st.dataframe(input_df)
    st.write('')

    # Remove output column in test set
    if OUTPUT in input_df.columns:
        X = input_df.drop([OUTPUT],axis=1)

    price_list = []
    for row in X.iterrows():
        price_list.append(predict(row))
    
    price_series = pd.Series(price_list)

    result_df = input_df.merge(price_series.rename('sale price'),left_index=True, right_index=True)
    csv = result_df.to_csv(index=False)
    
    b64 = base64.b64encode(csv.encode()).decode()
    st.write('''''')
    st.write('''''')
    st.write('''### **⬇️ Download Predicted Sale Price**''')
    href = f'<a href="data:file/csv;base64,{b64}" download="sale_price.csv">Download csv file</a>'
    st.write(href, unsafe_allow_html=True)