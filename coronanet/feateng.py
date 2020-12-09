import pandas as pd

def t0_creation(df):

    df['Province/State'] = df['Province/State'].fillna('')
    df['Province/State'] = df[['Country/Region', 'Province/State']].apply(' '.join, axis=1).str.strip()
    df = df.drop(columns='Country/Region').T
    df=df.reset_index()
    df= df.drop(index=[1,2])
    df.columns = df.iloc[0]
    df.drop(index=0, inplace=True)
    df.rename(columns={'Province/State':'date'}, inplace=True)
    df.date = pd.to_datetime(df.date)
    max_line = df.shape[0]
    max_col = df.shape[1]
    dico = {}
    for i in range(1,max_col):
        if df.iloc[max_line-1,i]>=10:
            dico[df.columns[i]] = df.date[min(df.iloc[:,i][df.iloc[:,i]>=10])]
    df = df.append(dico,ignore_index=True)
    tdeaths.iloc[318,0] = ''
    df.dropna(axis='columns', inplace=True)
    return df
