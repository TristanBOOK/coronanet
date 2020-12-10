### The following dunction returns the date a policy was implemented for the
### first time for a given country, and for a given level of policy
### /!\ the function uses clean_df as an input (df)
### based on Policy.RData

def policy_impl_date(df,ID,policy,level):
    if ID not in df['Country'].values:
        result = 'ID unknown'
    elif policy not in df.columns:
        result = 'Policy unknown'
    elif level not in df[policy].values:
        result = np.nan
    else:
        df_temp=df[['Date','Country',policy]][df[policy]==level]
        df_t=df_temp[df_temp['Country']==ID]
        result = df_t.Date.iloc[0]
    return result
