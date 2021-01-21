import pandas as pd


def transform_cases(cases):
    """Transforms cases dataframe, adds iso3, lat, long, population, and continent"""
    country = pd.read_csv('https://storage.googleapis.com/ve-public/country_iso.csv')
    continent = pd.read_csv('https://pkgstore.datahub.io/JohnSnowLabs/country-and-continent-codes-list/country-and-continent-codes-list-csv_csv/data/b7876b7f496677669644f3d1069d3121/country-and-continent-codes-list-csv_csv.csv')
    cases_group = cases.groupby(['Country'], as_index=False).sum()
         
    for c, i in enumerate(cases_group['Country']): #Get data from country csv
        try: cases_group.loc[c, 'iso3'] = country.loc[country['country'] == i]['iso3'].item()
        except: cases_group.loc[c,'iso3'] = 'NaN'
        try: cases_group.loc[c, 'Lat'] = country.loc[country['country'] == i]['Lat'].item()
        except: cases_group.loc[c,'Lat'] = 'NaN'
        try: cases_group.loc[c, 'Long_'] = country.loc[country['country'] == i]['Long_'].item()
        except: cases_group.loc[c,'Long_'] = 'NaN'
        try: cases_group.loc[c, 'Population'] = country.loc[country['country'] == i]['Population'].item()
        except: cases_group.loc[c,'Population'] = 'NaN'
    for c, i in enumerate(cases_group['iso3']): #Get data from continent csv
        try: cases_group.loc[c, 'continent'] = continent.loc[continent['Three_Letter_Country_Code'] == i]['Continent_Name'].item()
        except: cases_group.loc[c,'continent'] = 'NaN'
    cases_transformed = cases_group.melt(id_vars = ['Country','iso3','Lat','Long_','Population','continent' ], var_name = 'Date', value_name = 'Cases')
    cases_transformed['Date'] = pd.to_datetime(cases_transformed['Date'], format = '%m/%d/%y')
    return cases_transformed
 
    
def transform_sequence(sequence):
    """Converts string date to pandas datetime, renames columns"""
    sequence['date'] = pd.to_datetime(sequence['date'], format = '%Y/%m/%d')
    sequence_transform = sequence.rename(columns={'date':'Date','country':'Country'})  
    return sequence_transform
    

def transform_merge(sequence_trasnform, cases_transformed):
    """Merges both the cases and sequences dataframes"""
    full_data = cases_transformed.merge(sequence_trasnform, on=['Country','Date'], how='left')
    full_data['new_sequences'].fillna(0, inplace = True)
    full_data['Cases'].fillna(0, inplace = True)
    full_data['total_sequence'] = full_data.groupby('Country')['new_sequences'].cumsum()
    # full_data['cases_pop'] = full_data['Cases']/full_data['Population'] *100
    # full_data['sequence_case'] = full_data['total_sequence']/full_data['Cases'] *100
    # full_data_diffq = (full_data["Cases"].max() - full_data["Cases"].min()) / 219
    # full_data["Cases_scale"] = (full_data["Cases"] - full_data["Cases"].min()) / full_data_diffq + 1
    full_data_diffq = (full_data["total_sequence"].max() - full_data["total_sequence"].min()) / 219
    full_data["total_sequence_scale"] = (full_data["total_sequence"] - full_data["total_sequence"].min()) / full_data_diffq 
    # #full_data['Date'] = full_data['Date'].dt.strftime('%d-%m-%Y')
    # full_data['case_sequence_dif'] = full_data['Cases'] - full_data['total_sequence']
    full_data['case_sequence_ratio'] = (full_data['total_sequence']/(full_data['Cases']))
    return full_data
