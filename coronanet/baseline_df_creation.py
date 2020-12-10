### The goal here is to create a dataframe with the date of policy implemntation in each country
### and to analyse the impact on the growth in Covid cases / deaths.


import pandas as pd
import pyreadr


### /!\ make sure the 'COVID-19_LUT.csv' and 'Policy.RData' files are located in current dirrectory
countries_df=pd.read_csv('COVID-19_LUT.csv')
policies= pyreadr.read_r('Policy.RData')
policies_df = pd.DataFrame(policies['Policy'])
#policies_df.rename(columns={"ID": "Country"}).head()


### Create a 'clean_df' that summarises the policies implementation by date and country
p_df=policies_df
p_df=p_df.rename(columns={"ID": "Country"})
clean_df=p_df[p_df['PolicyType']=='C1'][["Country","Date"]]
col_names=list(p_df.PolicyType.unique())
for c in col_names:
    clean_df[c]=p_df[p_df['PolicyType']==c].PolicyValue.values

clean_df=clean_df.drop("ID",axis=1)
clean_df=clean_df.drop("IC",axis=1)


### Create a clean country df
clean_countries=countries_df[['ID','Population']]
clean_countries=clean_countries.sort_values('Population',ascending=False)
clean_countries.reset_index(inplace=True,drop=True)
for i in range(clean_countries.shape[0]):
    if (type(clean_countries.ID.iloc[i])!=str) or (len(clean_countries.ID.iloc[i])>2):
        clean_countries.rename(index={i:'XXXXX'},inplace=True)

clean_countries=clean_countries.drop('XXXXX')
clean_countries.reset_index(inplace=True,drop=True)


### Define a function that retreive the date a policy was implemented
def policy_impl_date(df,ID,policy):#,level):
    if ID not in df['Country'].values:
        result = 'ID unknown'
    elif policy not in df.columns:
        result = 'Policy unknown'
    #elif level not in df[policy].values:
    #    result = np.nan
    #elif level not in policies_df[policies_df['PolicyType']==policy].PolicyValue.values:
    #    result = np.nan
    elif policy not in policies_df[policies_df['ID']==ID].PolicyType.values:
        result = np.nan
    else:
        try:
            df_temp=df[['Date','Country',policy]]#[df[policy]==level]
            df_t=df_temp[df_temp['Country']==ID]
            result=df_t[df_t[policy]!=0].Date.iloc[0]
        except:
            result=np.nan
    return result


### Preprocessing
country_ID_list=list(clean_countries.ID)
policy_ID_list=list(policies_df.PolicyType.unique())
policy_ID_list.remove('I1')
policy_ID_list.remove('I2')
policy_ID_list.remove('I3')
policy_ID_list.remove('I4')
Date=[]
Policy=[]
ID=[]


### Loop over policy types and countries to create the DataFrame: create lists
for country in country_ID_list:
    for policy in policy_ID_list:
        Policy.append(policy)
        ID.append(country)
        Date.append(policy_impl_date(clean_df,country,policy))


### Transform lists into DataFrame
baseline_df=pd.DataFrame()
baseline_df['Date']=Date
baseline_df['ID']=ID
baseline_df['Policy']=Policy

baseline_df=baseline_df
