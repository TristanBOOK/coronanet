
import streamlit as st
import numpy as np
import pandas as pd
import zipfile
import datetime
from sklearn.preprocessing import MinMaxScaler

zf1 = zipfile.ZipFile('../coronanet/data/cases_new_data.csv.zip')
cases_df = pd.read_csv(zf1.open('cases_new_data.csv'))
lma_data=pd.lma_data=pd.read_csv('https://raw.githubusercontent.com/TristanBOOK/coronanet/master/coronanet/data/LMA_Data_10_semaines_and_Pol_fam.csv')
zf2 = zipfile.ZipFile('../coronanet/data/policies_raw.csv.zip')
policies_df = pd.read_csv(zf2.open('policies_raw.csv'))

countries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19_Unified-Dataset/master/COVID-19_LUT.csv')
country_dict = {}
for i in range(countries_df.shape[0]):
    country_dict[countries_df.ID[i]] = countries_df.NameID[i]

countries=lma_data.ID.unique()

st.markdown("""
    # Anti-Covid policy efficiency
    ## Will your next anti-covid policy help saving lives?
""")

option = st.selectbox('Please selct a country ID',countries)

case=cases_df[cases_df['ID']==option]
case.Date=pd.to_datetime(case.Date)
dte1=case.Date.iloc[case.shape[0]-1]
dte0=case.Date.iloc[case.shape[0]-22]
past_21d_death=case.Cases.iloc[case.shape[0]-1]-case.Cases.iloc[case.shape[0]-22]

s1=f'Unfortunately, **{int(past_21d_death)}** people died from **Covid-19** in **{country_dict[option]}** between **{dte0.strftime("%Y-%m-%d")}** and **{dte1.strftime("%Y-%m-%d")}**.'
st.markdown(s1)
st.markdown("""## Select policies to save lives""")

pol=['C1','C2','C3','H1','H2']
st.write(f'The most efficient policies to save lives are the following: {pol}. Slide to select policy intensity, and simulate the efficiency of your policy')

policy=policies_df
policy=policy.fillna(0)
policy.Date=pd.to_datetime(policy.Date)
policy=policy[policy['Date']>(pd.to_datetime(dte1)-datetime.timedelta(days=21))]
policy=policy[policy['Country']==option]
policy=policy[['Date','Country','PolicyType','PolicyValue']]

Slide1_curr=policy[policy['PolicyType']==pol[0]].PolicyValue.values[0]
Slide2_curr=policy[policy['PolicyType']==pol[1]].PolicyValue.values[0]
Slide3_curr=policy[policy['PolicyType']==pol[2]].PolicyValue.values[0]
Slide4_curr=policy[policy['PolicyType']==pol[3]].PolicyValue.values[0]
Slide5_curr=policy[policy['PolicyType']==pol[4]].PolicyValue.values[0]

int(policies_df[policies_df['PolicyType']==pol[0]].PolicyValue.max())

i1_min, i1_max=(int(policies_df[policies_df['PolicyType']==pol[0]].PolicyValue.min()),
    int(policies_df[policies_df['PolicyType']==pol[0]].PolicyValue.max()))
i2_min, i2_max=(int(policies_df[policies_df['PolicyType']==pol[1]].PolicyValue.min()),
    int(policies_df[policies_df['PolicyType']==pol[1]].PolicyValue.max()))
i3_min, i3_max=(int(policies_df[policies_df['PolicyType']==pol[2]].PolicyValue.min()),
    int(policies_df[policies_df['PolicyType']==pol[2]].PolicyValue.max()))
i4_min, i4_max=(int(policies_df[policies_df['PolicyType']==pol[3]].PolicyValue.min()),
    int(policies_df[policies_df['PolicyType']==pol[3]].PolicyValue.max()))
i5_min, i5_max=(int(policies_df[policies_df['PolicyType']==pol[4]].PolicyValue.min()),
    int(policies_df[policies_df['PolicyType']==pol[4]].PolicyValue.max()))

i1 = st.slider('C1', i1_min, i1_max, int(Slide1_curr))
i2 = st.slider('H2', i2_min, i2_max, int(Slide2_curr))
i3 = st.slider('C2', i3_min, i3_max, int(Slide3_curr))
i4 = st.slider('CT', i4_min, i4_max, int(Slide4_curr))
i5 = st.slider('C3', i5_min, i5_max, int(Slide5_curr))

def scaler(x,mi,ma):
    return ((x-mi)/(ma-mi))*(ma-mi)+mi

i1=scaler(i1,i1_min,i1_max)
i2=scaler(i2,i2_min,i2_max)
i3=scaler(i3,i3_min,i3_max)
i4=scaler(i4,i4_min,i4_max)
i5=scaler(i5,i5_min,i5_max)

inputs=[i1,i2,i3,i4,i5,past_21d_death]

############
############
# ADD MODEL#
# inputs= i1,i2,i3,i4,i5,    + past_21d_death
# return J21= number of death in 21 days predicted with model
############
############

filt = st.radio('Display options:',('Cases', 'Cases_New'))

case=case[['Date',filt]]

delta=((case[filt].iloc[case.shape[0]-1]+1)/case[filt].iloc[case.shape[0]-22])**(1/20)
predict=list(case[filt].values)
for i in range (21):
    predict.append(round(predict[len(predict)-1]*delta))

if filt == 'Cases':
    J21=60000 ### to be changed!!!! output from model
else:
    J21=100 ### to be changed!!!! output from model


delta21=((J21)/(case[filt].iloc[case.shape[0]-1]+1))**(1/20)
predict21=list(case[filt].values)
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
