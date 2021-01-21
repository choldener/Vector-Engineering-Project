import pandas as pd
from pipeline.transform import transform_cases, transform_sequence, transform_merge


def call_full_data():
    """Calls all the data and performs the required transformations"""
    cases = pd.read_csv('https://storage.googleapis.com/ve-public/covid_case_counts2.csv')
    cases_transformed = transform_cases(cases)
    sequence = pd.read_csv('https://storage.googleapis.com/ve-public/covid_new_sequences.csv')
    sequence_trasnform = transform_sequence(sequence)
    full_data = transform_merge(sequence_trasnform, cases_transformed)
    return full_data


# df = call_full_data()
#df_day = df.loc[df['Date'] == df['Date'].max()]