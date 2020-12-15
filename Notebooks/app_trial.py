
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

st.markdown("""
    # Anti-Covid policy efficnecy
    ## Will your next anti-covid policy help saving lives?
""")

st.write()
#st.markdown("Hello World")

countries=['FR','US','RU',]

option = st.selectbox('Please selct a country ID',countries)

J_14=1000
date='2020-10-01'


s=f'**{J_14}** people died from **Covid-19** in **{option}** since **{date}**. Select policies to save lifes'
st.markdown(s)

pol=['H1','G5','DFhghg']
st.write(f'The most efficient policies to save lives are the following: {pol}')


#@st.cache
#def get_slider_data():
#    print('get_slider_data called')
#    return pd.DataFrame({
#          'first column': list(range(1, 11)),
#          'second column': np.arange(10, 101, 10)
#        })

#df = get_slider_data()

i_C1 = st.slider('Select C1 Intensity', 1, 3, 0)
i_H2 = st.slider('Select H2 Intensity', -1, 4, -1)
i_E5 = st.slider('Select E5 Intensity', 0, 9, 0)
i_C3 = st.slider('Select C3 Intensity', 0, 9, 5)
i_E1 = st.slider('Select E1 Intensity', 0, 9, 4)

#filtered_df = df[df['first column'] % option == 0]

#st.write(filtered_df)

baseline_cases=[1,3,2,3,4,5,6,7]
pred=[1,3,2,3,4,5,i_C3,i_E1]

df = ({option:baseline_cases,'Prediction':pred})

st.line_chart(df)
