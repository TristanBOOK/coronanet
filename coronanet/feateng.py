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
    df.iloc[318,0] = ''
    df.dropna(axis='columns', inplace=True)
    return df

def lou(csv):
    from sklearn.preprocessing import MinMaxScaler
    df_15weeks = pd.read_csv(f'{csv}')
    df_15weeks.drop(columns='index', inplace=True)
    df_15weeks.insert(2,'PolicyFamily','')
    df_15weeks['PolicyFamily']  = df_15weeks['PolicyType'].astype(str).str[0]
    temp = df_15weeks.columns.to_list()[9:]
    temp_neg = temp[:7]
    temp_pos = temp[8:16]
    temp_neg.reverse()
    df_15weeks['d_j-7'] = (df_15weeks['Cases'] / df_15weeks['J-7'])**(1/6)
    for i in temp_neg:
        df_15weeks[f'i_{i}'] = (df_15weeks['Cases'] / df_15weeks[f'{i}'])**(1/((1+temp_neg.index(i))*7-1))
    for i in temp_pos:
        df_15weeks[f'i_{i}'] = (df_15weeks[f'{i}'] / df_15weeks['Cases'])**(1/((1+temp_pos.index(i))*7-1))
    pol_type = ['E3_diff', 'H2_diff', 'H6_diff', 'C3_diff', 'C6_diff', 'E1_diff', 'C2_diff', 'C1_diff', 'C5_diff', 'H1_diff', 'H3_diff', 'H4_diff', 'C8_diff', 'E2_diff', 'C4_diff', 'E4_diff', 'C7_diff', 'H5_diff']
    for i in pol_type:
        df_15weeks[i] = -100000
        df_15weeks[i] = df_15weeks[df_15weeks['PolicyType']==i]['value']
        df_15weeks[i] = df_15weeks[i].fillna(0)
        scaler = MinMaxScaler()
        scaler.fit_transform(df_15weeks[[i]])
        df_15weeks[i] = scaler.transform(df_15weeks[[i]])
    return df_15weeks
