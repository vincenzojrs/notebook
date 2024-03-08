import streamlit as st
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

class MachineLearningModel():
    def __init__(self):
        self.model = RandomForestClassifier()
        
    def import_data(self):
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        return X, y
        
    def fit(self, x_data, y_data):
        self.model.fit(x_data, y_data)
        
    def model_run(self):
        X, y = self.import_data()
        self.fit(X, y)  
        
    def predict(self, dataframe):
        prediction = self.model.predict(dataframe)
        prediction = self.model.predict_proba(dataframe)
        return prediction
    
class WebSite():
    def __init__(self):
        self.title = st.title('Simple Iris Flower Predictions')
        self.description = st.write('This app predicts the Iris flower type')

    def user_input_features(self):
        sepal_length = st.sidebar.slider('Sepal length', 4.3, 7.9, 5.4)
        sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.4, 3.4)
        petal_length = st.sidebar.slider('Petal length', 1.0, 6.9, 1.3)
        petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
        data = {'sepal_length' : sepal_length,
                'sepal_width' : sepal_width,
                'petal_length' : petal_length,
                'petal_width' : petal_width}
        features = pd.DataFrame(data, index = [0])
        return features
    
    def body(self):
        st.subheader('User Input Parameters')
        model = MachineLearningModel()
        df = self.user_input_features()
        st.write(df)
        model.model_run()
        prediction = model.predict(df)
        
        #st.subheader('Class labels and their corresponding index number')
        #st.write(iris.target_names)

        st.subheader('Prediction')
        st.write(prediction)
        
website = WebSite()
website.body()
