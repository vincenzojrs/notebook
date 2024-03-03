import streamlit as st
import numpy as np
import pandas as pd

np.random.seed(42)

class NUFORCReportApp:
    def __init__(self):
        self.data = self.load_data(500)
        self.data = self.preprocess_data(self.data)        
    
    def load_data(self, nrows):
        data = pd.read_csv("complete.csv", nrows=nrows)
        return data
    
    def preprocess_data(self, data):
        """
        Convert strings in the date time column so that when "24:00" appears, change it in "00:00" +1 day
        """
        twenty_fours = data['datetime'].str[-5:] == '24:00'
        data.loc[twenty_fours, 'datetime'] = data['datetime'].str[:-5] + '00:00'
        data['datetime'] = pd.to_datetime(data['datetime'], format='%d/%m/%Y %H:%M')
        data.loc[twenty_fours, 'datetime'] += pd.DateOffset(1)
        return data
        
    def display_raw_data(self):
        st.subheader("Raw Data")
        st.dataframe(self.data, use_container_width=True)
        
    def display_sighting_report_by_hour(self):
        st.subheader("Number of sighting report by hour")
        hist_values = np.histogram(self.data["datetime"].dt.hour, bins=24, range=(0, 24))[0]
        st.bar_chart(hist_values)
        
    def display_map(self):
        st.subheader("Map of sightings")
        st.map(self.data)

    def run(self):
        st.title("NUFORC Report App")
        st.write("Let's try to build an app regarding UFO seeing")
        
        self.display_raw_data()
        self.display_sighting_report_by_hour()
        self.display_map()

if __name__ == "__main__":
    app = NUFORCReportApp()
    app.run()
