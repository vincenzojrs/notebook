import streamlit as st
import numpy as np
import pandas as pd

np.random.seed(42)

class webpage():
    def __init__(self, title, stringa, dataframe):
        self.title = title
        self.stringa = stringa
        self.dataframe = dataframe
        
    def stampa(self):
        """
        Print the content of the webpage
        """
        
        # Display the title
        st.title(self.title)
        
        # Display the string
        st.write(self.stringa)
        
        # Display the checkbox for hiding/showing the dataframe
        if st.checkbox("Show related dataframe"):
            st.dataframe(
                            self.dataframe,
                            use_container_width = True
                        )
            
        # Display the linechart
        st.line_chart(
                            self.dataframe,
                            x = self.dataframe.columns[0],
                            y = self.dataframe.columns[1:-1]
                     )

toy_dataframe = pd.DataFrame({'Date': pd.date_range(start = "2022-01-01",
                                                    end = "2022-01-10",
                                                    freq = "D"),
                              'Numbers1': np.random.randint(0, 50, size = 10),
                              'Numbers2': np.random.randint(50, 80, size = 10),
                              'Letters': ["A", "B", "C", "A", "B", "C","A", "B", "C", "A"]})


paginaweb = webpage(
    title = "That's the title",
    stringa = "That's the stringa",
    dataframe = toy_dataframe
    )

paginaweb.stampa()
