
import streamlit as st
import numpy as np
import pandas as pd
import zipfile
#from matplotlib import pyplot as plt

zf = zipfile.ZipFile('../coronanet/data/cases_new_data.csv.zip')
cases_df = pd.read_csv(zf.open('cases_new_data.csv'))
lma_data=pd.lma_data=pd.read_csv('https://raw.githubusercontent.com/TristanBOOK/coronanet/master/coronanet/data/LMA_Data_10_semaines_and_Pol_fam.csv')
countries=lma_data.ID.unique()

st.markdown("""
    # Anti-Covid policy efficiency
    ## Will your next anti-covid policy help saving lives?
""")

option = st.selectbox('Please selct a country ID',countries)

case=cases_df[cases_df['ID']==option]
dte1=case.Date.iloc[case.shape[0]-1]
dte0=case.Date.iloc[case.shape[0]-22]
death=case.Cases.iloc[case.shape[0]-1]-case.Cases.iloc[case.shape[0]-22]

s1=f'Unfortunately, **{death}** people died from **Covid-19** in **{option}** between **{dte0}** and **{dte1}**. Select policies to save lives'
st.markdown(s1)

pol=['H1','G5','DFhghg']
st.write(f'The most efficient policies to save lives are the following: {pol}. Slide to select policy intensity')

i_C1 = st.slider('C1', 1, 3, 0)
i_H2 = st.slider('H2', -1, 4, -1)
i_E5 = st.slider('Select **E5** Intensity', 0, 9, 0)
i_C3 = st.slider('Select **C3** Intensity', 0, 9, 5)
i_E1 = st.slider('Select **E1** Intensity', 0, 9, 4)

t = st.radio('Number of deaths',('Total (cumul.)', 'New Cases'))
if t == 'Total (cumul.)':
    filt = 'Cases'
else:
    filt = 'Cases_New'

case=case[['Date',filt]]

delta=((case.filt.iloc[case.shape[0]-1]+1)/case.filt.iloc[case.shape[0]-22])**(1/20)
predict=list(case.Cases.values)
for i in range (21):
    predict.append(round(predict[len(predict)-1]*delta))

############
############
# ADD MODEL#
# J21= number of death in 21 days predicted with model
############
############

J21=60000 ### to be changed!!!!
delta21=((J21)/(case.filt.iloc[case.shape[0]-1]+1))**(1/20)
predict21=list(case.filt.values)
for i in range (21):
    predict21.append(round(predict21[len(predict21)-1]*delta21))

df=pd.DataFrame({'Projection':predict,'Intervention':predict21})

st.line_chart(df)

saved_lives=round(predict[len(predict)-1])-J21

if saved_lives < 0 :
    s2='The policies you selected might not be efficient'
else:
    s2=f'**{saved_lives}** lives can be saved with the policies you selcted'

st.markdown(s2)
