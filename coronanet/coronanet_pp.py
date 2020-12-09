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

class Coronanet:

    def __init__(self):
        self.df = Coronanet().get_data()

    def tristans_columns(self):
        df['date_announced'] = pd.to_datetime(df['date_announced'])
        df['date_start'] = pd.to_datetime(df['date_start'])
        df['date_end'] = pd.to_datetime(df['date_end'])
        df['date_announced'].fillna(df['date_start'], inplace = True)
        df['date_start'].clip(lower=df['date_announced'], inplace=True)
        df_select = df[['policy_id', 'date_start', 'country',
           'type', 'ISO_A3','compliance']]
        df_select.drop_duplicates(subset=['policy_id'], inplace=True)
        return df_select

    def compliance_mask(self):
        df = df[df['compliance'].notna()]
        mask = df['compliance'].value_counts() > 1000
        df = df[df['compliance'].isin(mask.index)]
        return df

    def handle_compliance(self):
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

