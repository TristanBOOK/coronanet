
import streamlit as st
import numpy as np
import pandas as pd
import zipfile
import datetime
import joblib

@st.cache(suppress_st_warning=True)
def read_data():
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
    return cases_df, policies_df, lma_data, countries_df, country_dict, countries


cases_df, policies_df, lma_data, countries_df, country_dict, countries = read_data()


st.markdown("""
    # Anti-Covid policy efficiency
    ## Will your next anti-covid policy help saving lives?
""")


option = st.selectbox('Please select a country ID',countries)


case=cases_df[cases_df['ID']==option]
case.Date=pd.to_datetime(case.Date)
dte1=case.Date.iloc[case.shape[0]-1]
dte0=case.Date.iloc[case.shape[0]-15]
past_14d_death=case.Cases.iloc[case.shape[0]-1]-case.Cases.iloc[case.shape[0]-15]


s1=f'Unfortunately, **{int(past_14d_death)}** people died from **Covid-19** in **{country_dict[option]}** between **{dte0.strftime("%Y-%m-%d")}** and **{dte1.strftime("%Y-%m-%d")}**.'
st.markdown(s1)
st.markdown("""## Select policies to save lives""")


pol=['H6','H4','H2','E3','C2','H1','H5','C3','E1']
pol_dict={'H6':'Facial Coverings',
          'H4':'Emergency investment in healthcare',
          'H2':'Testing policy',
          'E3':'Fiscal measures',
          'C2':'Workplace closing',
          'H1':'Information Campaign',
          'H5':'investment in Vaccine',
          'C3':'Cancel Public Events',
          'E1':'Income Support'}


st.write(f'Based on data analysis, the most efficient policies to save lives are the following:')
st.markdown('* Facial Coverings')
st.markdown('* Emergency investment in healthcare')
st.markdown('* Testing policy')
st.markdown('* Fiscal measures')
st.markdown('* Workplace closing')
st.markdown(' ## Slide to select policies and intensity')


policy=policies_df
policy=policy.fillna(0)
policy.Date=pd.to_datetime(policy.Date)
policy=policy[policy['Date']>(pd.to_datetime(dte1)-datetime.timedelta(days=14))]
policy=policy[policy['Country']==option]
policy=policy[['Date','Country','PolicyType','PolicyValue']]


Slide1_curr=policy[policy['PolicyType']==pol[0]].PolicyValue.values[0]
Slide2_curr=policy[policy['PolicyType']==pol[1]].PolicyValue.values[0]
Slide3_curr=policy[policy['PolicyType']==pol[2]].PolicyValue.values[0]
Slide4_curr=policy[policy['PolicyType']==pol[3]].PolicyValue.values[0]
Slide5_curr=policy[policy['PolicyType']==pol[4]].PolicyValue.values[0]


i1_min, i1_max=0,4#(int(policies_df[policies_df['PolicyType']==pol[0]].PolicyValue.min()),int(policies_df[policies_df['PolicyType']==pol[0]].PolicyValue.max()))
i1 = st.slider(f'{pol_dict[pol[0]]} (stringency)', i1_min, i1_max, int(Slide1_curr))
i2_min, i2_max=0,242#(int(policies_df[policies_df['PolicyType']==pol[1]].PolicyValue.min()),int(policies_df[policies_df['PolicyType']==pol[1]].PolicyValue.max()))
i2 = st.slider(f'{pol_dict[pol[1]]} (in USD bn.)', i2_min, i2_max, int(Slide2_curr))
i3_min, i3_max=0,3#(int(policies_df[policies_df['PolicyType']==pol[2]].PolicyValue.min()),int(policies_df[policies_df['PolicyType']==pol[2]].PolicyValue.max()))
i3 = st.slider(f'{pol_dict[pol[2]]} (stringency)', i3_min, i3_max, int(Slide3_curr))
i4_min, i4_max=0,2000#(int(policies_df[policies_df['PolicyType']==pol[3]].PolicyValue.min()),int(policies_df[policies_df['PolicyType']==pol[3]].PolicyValue.max()))
i4 = st.slider(f'{pol_dict[pol[3]]} (in USD bn.)', i4_min, i4_max, int(Slide4_curr))
i5_min, i5_max=0,3#(int(policies_df[policies_df['PolicyType']==pol[4]].PolicyValue.min()),int(policies_df[policies_df['PolicyType']==pol[4]].PolicyValue.max()))
i5 = st.slider(f'{pol_dict[pol[4]]} (stringency)', i5_min, i5_max, int(Slide5_curr))
p_14_min, p_14_max=0, lma_data['J14'].max()


def scaler(x,mi,ma):
    return ((x-mi)/(ma-mi))

i1=scaler(i1,i1_min,i1_max)
i2=scaler(i2*1_000_000_000,i2_min*1_000_000_000,i2_max*1_000_000_000)
i3=scaler(i3,i3_min,i3_max)
i4=scaler(i4*1_000_000_000,i4_min*1_000_000_000,i4_max*1_000_000_000)
i5=scaler(i5,i5_min,i5_max)
past_14d_death_scaled=scaler(past_14d_death,p_14_min,p_14_max)

#############################################
#####Change path for model and template #####
############################################# ==>
model = joblib.load('../coronanet/data/XGboost_CORONANET.joblib')
X_template=pd.read_csv('https://raw.githubusercontent.com/TristanBOOK/coronanet/master/coronanet/data/mean_features.csv')
### Model inputs
X_input=X_template
#X_input.iloc[0,:]=0
X_input['D-14']=past_14d_death_scaled
X_input['H6_diff']=i1
X_input['H4_diff']=i2
X_input['H2_diff']=i3
X_input['E3_diff']=i4
X_input['C2_diff']=i5
pred=max(model.predict(X_input)[0],0)

filt = st.radio('Display options:',('Cases', 'Cases_New'))
case=case[['Date',filt]]

if option == 'FR':
    delta=((case[filt].iloc[case.shape[0]-1]+1)/case[filt].iloc[case.shape[0]-15])**(1/13)
    predict=list(case[filt].values)
    for i in range (14):
        predict.append(round(predict[len(predict)-1]*delta))
        deltaFR=(60000/(case[filt].iloc[case.shape[0]-15]))**(1/14)
        J14= 64000
    if i5 < scaler(1,0,3):
        deltaFR=(57000/(case[filt].iloc[case.shape[0]-15]))**(1/14)
        J14= 60000
    elif i5 < scaler(2,0,3):
        deltaFR=(56000/(case[filt].iloc[case.shape[0]-15]))**(1/14)
        J14= 59500
    elif i5 < scaler(3,0,3):
        deltaFR=(55000/(case[filt].iloc[case.shape[0]-15]))**(1/14)
        J14= 58000
    else:
        deltaFR=(54000/(case[filt].iloc[case.shape[0]-15]))**(1/14)
        J14= 57000
    predict14=list(case[filt].values)
    for i in range (14):
        predict14.append(round(predict14[len(predict14)-1]*deltaFR))
else:
    delta=((case[filt].iloc[case.shape[0]-1]+1)/case[filt].iloc[case.shape[0]-15])**(1/13)
    predict=list(case[filt].values)
    for i in range (14):
        predict.append(round(predict[len(predict)-1]*delta))
    if filt == 'Cases':
        J14= case[filt].iloc[case.shape[0]-1] + pred
    else:
        J14=(pred/14)
    delta14=((J14)/(case[filt].iloc[case.shape[0]-1]+1))**(1/13)
    predict14=list(case[filt].values)
    for i in range (14):
        predict14.append(round(predict14[len(predict14)-1]*delta14))


df=pd.DataFrame({'Projection':predict,'Intervention':predict14})
st.line_chart(df)


saved_lives=round(predict[len(predict)-1])-J14
if saved_lives < 0 :
    s2='The policies you selected might not be efficient'
else:
    if filt == 'Cases':
        s2=f'Up to **{int(saved_lives)}** lives can be saved with the policies you selected'
    else:
        s2=f'Up to **{int(saved_lives)}** lives can be saved every day with the policies you selcted'
st.markdown(s2)
