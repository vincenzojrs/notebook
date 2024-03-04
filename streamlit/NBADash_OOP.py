# Inspired by the Data Professor's "Build 12 Data Science Apps with Python and Streamlit - Full Course" video

import streamlit as st
import pandas as pd
import base64
import numpy as np

class NBAWebsite():
    def __init__(self):
        self.title = st.title("NBA Player Stats Explorer")
        self.markdown = st.markdown("""
                                    This app performs simple webscraping of NBA players' statistics
                                    * **Python libraries used**: base64, pandas, streamlit
                                    * **Data Source:** [Basketball-reference.com](https://basketball-reference.com/)
                                    """)
                                    
    def sidebar(self):
        """
        Create a sidebar and place a selectbox which returns a year as a filter

        """
        st.sidebar.header("User input interface")
        selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))
        return selected_year

    def load_data(self, year):
        """
        Create the dataset, filtered by the year returned by the sidebar
        """
        url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
        html = pd.read_html(url, header=0)
        df = html[0]
        raw = df.drop(df[df.Age == 'Age'].index)
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis = 1)
        return playerstats
    
    def team_selection(self, df):
        """
        Create a multiselection box, from the "Team" column of the dataset and return a list
        """
        sorted_unique_team = sorted(df.Tm.unique())
        selected_team = st.sidebar.multiselect('Team', sorted_unique_team)
        return selected_team
        
    def position(self, df):
        """
        Create a multiselection box, from the "Position" column of the dataset and return a list
        """
        sorted_unique_position = sorted(df.Pos.unique())
        selected_pos = st.sidebar.multiselect('Position', sorted_unique_position)
        return selected_pos

        
    def run(self):
        # Display the sidebar and return the year selected as a variable
        selected_year = self.sidebar()
        
        # Return a dataframe, whose year is filtered by the selected_year
        df = self.load_data(selected_year)  
        
        # Return the team chosen and display the selection box
        selected_team = self.team_selection(df)
        
        # Return the position chosen and display the selection box
        selected_position = self.position(df)
        
        # Once both filters have been chosen, filter the dataframe
        if selected_team and selected_position:
            df = df[df['Tm'].isin(selected_team) & df['Pos'].isin(selected_position)]
        
        # Display the dataframe
        st.write(df)
        
if __name__ == '__main__':
    app = NBAWebsite()
    app.run()
        
