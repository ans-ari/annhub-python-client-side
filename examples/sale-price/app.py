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
URL = '{}/api/v1/predict'.format(os.environ['host'])

def predict(data):
    data = data[1].values.flatten().tolist()
    data = str(data)
    resp = requests.post(URL,data=data)
    json_data = json.loads(resp.text)
    if "prediction" in json_data:
        prediction = float(json_data["prediction"][0])
    else:
        raise ValueError(json_data['detail'])
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
        features_df = input_df.drop([OUTPUT],axis=1)
    else:
        features_df = input_df

    price_list = []
    for row in features_df.iterrows():
        predicted_revenue = predict(row)
        price_list.append(round(predicted_revenue,2))
    
    price_series = pd.Series(price_list)

    result_df = input_df.merge(price_series.rename('Predicted Revenue'),left_index=True, right_index=True)
    csv = result_df.to_csv(index=False)
    
    b64 = base64.b64encode(csv.encode()).decode()
    st.write('''''')
    st.write('''''')
    st.write('''### **⬇️ Download Predicted Sale Price**''')
    href = f'<a href="data:file/csv;base64,{b64}" download="sale_price.csv">Download csv file</a>'
    st.write(href, unsafe_allow_html=True)