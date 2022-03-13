import pandas as pd
from pprint import pprint

df = pd.read_csv('data/survey_results_public.csv')
schema_df = pd.read_csv('data/survey_results_schema.csv')
pprint(df.shape)
pprint(df.info())
pprint(schema_df)