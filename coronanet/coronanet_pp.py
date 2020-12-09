import numpy as np
import pandas as pd
import datetime
import pyreadr
import pandas as pd
from IPython.display import display
from sklearn.preprocessing import OneHotEncoder
from nltk.corpus import stopwords
import string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from coronanet.data import Coronanet

class Prepro_coronanet:

    def __init__(self):
        self.df = Coronanet().get_raw_data()

    def tristans_columns(self):
        df = self.df.copy()
        df['date_announced'] = pd.to_datetime(df['date_announced'])
        df['date_start'] = pd.to_datetime(df['date_start'])
        df['date_end'] = pd.to_datetime(df['date_end'])
        df['date_announced'].fillna(df['date_start'], inplace = True)
        df['date_start'].clip(lower=df['date_announced'], inplace=True)
        df_select = df[['policy_id', 'date_start', 'country',
           'type', 'ISO_A3','compliance']]
        df_select.drop_duplicates(subset=['policy_id'], inplace=True)
        return df_select

    def compliance_mask(self, df_select):
        '''
        This method drop the nan registers in colomn "compliance"
        '''
        df = df_select.copy()
        df = df[df['compliance'].notna()]
        mask = df['compliance'].value_counts() > 1000
        df = df[df['compliance'].isin(mask.index)]
        return df

    def encode_compliance(self, df_select):
        df = df_select.copy()

        def handle_compliance(x):
            if 'Voluntary/Recommended' in x:
                return 0
            if 'Mandatory (Unspecified/Implied)' in x:
                return 1
            if 'Mandatory with Fines' in x:
                return 2
            if 'Mandatory with Exceptions' in x:
                return 3
            if 'Mandatory with Legal Penalties' in x:
                return 4

        df['n_compliance'] = df['compliance'].map(handle_compliance)
        return df

    def get_type(self, df_select):
        df = df_select.copy()
        df = pd.get_dummies(df, columns=["type"])
        return df

    def missing_ISO(self, df_select):
        df = df_select.copy()
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

    def prepro_data(self):
        df = self.df.copy()
        df = self.tristans_columns()
        df = self.compliance_mask(df)
        df = self.encode_compliance(df)
        df = self.get_type(df)
        df = self.missing_ISO(df)
        return df

if __name__ == '__main__':
    #from coronanet.data import Coronanet
    #coronanet_instance = Coronanet()
    #df = coronanet_instance.get_raw_data()
    #print(df.head())

    from coronanet.coronanet_pp import Prepro_coronanet

    # prepro_instance.df is the raw_data

    prepro_instance = Prepro_coronanet()
    #print(prepro_instance.df.head())

    # Test tristans_columns method
    #df_select = prepro_instance.tristans_columns()
    #print(df_select.shape)

    # Test compliance_mask method
    #print(df_select['compliance'].isnull().sum())
    #df_select = prepro_instance.compliance_mask(df_select)
    #print(df_select['compliance'].isnull().sum())
    #print(df_select.shape)

    # test handle_compliance method
    #df_select = prepro_instance.encode_compliance(df_select)
    #print(df_select.shape)

    # test get_dummies method
    #df_select = prepro_instance.get_type(df_select)
    #print(df_select.shape)
    #print(df_select['ISO_A3'].unique())

    # test missing_ISO method
    #df_select = prepro_instance.missing_ISO(df_select)
    #print(df_select['ISO_A3'].unique())



    # test new_table function
    #df_select = prepro_instance.new_table(df)
    df_select = prepro_instance.prepro_data()
    print(df_select.head())
    print(df_select.shape)
    print(df_select['ISO_A3'].unique())

