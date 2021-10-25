FROM python:3.7
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
ENV host http://18.140.115.149:8085
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run app.py