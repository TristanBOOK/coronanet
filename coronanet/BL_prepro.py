import numpy as np
import pandas as pd
import datetime
import pyreadr
import pandas as pd
from IPython.display import display

from sklearn.preprocessing import OneHotEncoder

class my_prepro():

    def __init__(self):
        pass
    def Coco_prepro(df):
        df['date_announced'] = pd.to_datetime(df['date_announced'])
        df['date_start'] = pd.to_datetime(df['date_start'])
        df['date_end'] = pd.to_datetime(df['date_end'])
        df['date_start'] = df['date_start'].clip(lower=df['date_announced'])
        df_select = df[['record_id', 'policy_id','date_start', 'ISO_A3', 'type', 'compliance']]
        df_select= df_select.drop_duplicates(subset=['policy_id'])
        return df_select

    def compliance_mask(df):
        df = df[df['compliance'].notna()]
        mask = df['compliance'].value_counts() > 1000
        df = df[df['compliance'].isin(mask.index)]
        return df

    def handle_compliance(x):
        if 'Voluntary/Recommended' in x:
            return 0
        if 'Mandatory (Unspecified/Implied)' in x:
            return
        if 'Mandatory with Fines' in x:
            return 2
        if 'Mandatory with Exceptions' in x:
            return 3
        if 'Mandatory with Legal Penalties' in x:
            return 4

    def compliance_encode(df):
        df['n_compliance'] = df['compliance'].map(handle_compliance)
        return df


    def get_type(df):
        df = pd.get_dummies(df, columns=["type"])
        return df

    def missing_ISO(df):
        df['ISO_A3'] = np.where(df['ISO_A3'] == '-', df['country'], df['ISO_A3'])
        df['ISO_A3'] = df['ISO_A3'].fillna(df['country'])
        df['ISO_A3'] = df['ISO_A3'].replace('Northern Cyprus', 'CYP')
        df['ISO_A3'] = df['ISO_A3'].replace('Kosovo', 'XK')
        df['ISO_A3'] = df['ISO_A3'].replace('CÙte díIvoire', 'CIV')
        df['ISO_A3'] = df['ISO_A3'].replace('European Union', 'EU')
        df['ISO_A3'] = df['ISO_A3'].replace('S„o TomÈ & PrÌncipe', 'STP')
        df['ISO_A3'] = df['ISO_A3'].replace('Macau', 'MAC')
        df['ISO_A3'] = df['ISO_A3'].replace('Timor Leste', 'TLS')

        return df








