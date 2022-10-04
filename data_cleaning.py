import pandas as pd
from math import floor
import datetime

def remove_duplicates(df: pd.DataFrame):
    df = df.duplicated()
    return df

def check_for_moved_employees(df: pd.DataFrame):
    unique_cities = df['WerknemerID', 'stad'].drop_duplicates()
    city_counts = unique_cities.groupby('WerknemerID').count()
    if any(city_counts['stad']) > 1:
        moved_employees = city_counts.loc[city_counts['stad']>1].index
        raise Warning(f'Employees {moved_employees} have moved, only most recent city is taken into account') 
    else:
        pass
    
def check_for_BU_transfers(df: pd.DataFrame):
    unique_cities = df['WerknemerID', 'BUSINESS_UNIT'].drop_duplicates()
    city_counts = unique_cities.groupby('WerknemerID').count()
    if any(city_counts['BUSINESS_UNIT']) > 1:
        moved_employees = city_counts.loc[city_counts['BUSINESS_UNIT']>1].index
        raise Warning(f'Employees {moved_employees} have switches Business Unit, only most recent entry is taken into account') 
    else:
        pass
    
    
def impute_missing_age(df: pd.DataFrame, drop_age_column = True):
    days_diff = df['datum'] - df['geboortedatum']
    derived_age = list(map(floor, days_diff/datetime.timedelta(days=365)))
    df['derived_age'] = derived_age
    if drop_age_column:
        df = df.drop('leeftijd', axis=1)
    return df

def impute_missing_experience(df: pd.DataFrame, drop_experience_column = True):
    indienst_check = df['uitdiensttreding_datum'] < datetime.datetime(year=1905, month=1, day=2)
    df['last_working_date'] =  df['uitdiensttreding_datum']
    df.loc[indienst_check, 'last_working_date'] = df['datum']
    
    
    days_diff = df['last_working_date'] - df['indiensttreding_datum']
    derived_experience = list(map(floor, days_diff/datetime.timedelta(days=365)))
    df['derived_experience'] = derived_experience
    
    df = df.drop('last_working_date', axis = 1)
    if drop_experience_column:
        df = df.drop('lengte_dienst', axis=1)
    return df
    

def get_most_recent_entry(df: pd.DataFrame):
    df['rn'] = df.sort_values(by='datum', ascending=False).groupby(['WerknemerID']).cumcount() + 1
    df = df.loc[df['rn'] == 1].drop('rn', axis=1)
    return df

def remove_missing_data(df: pd.DataFrame, missing_columns):
    missing_columns.append('uitdiensttreding_reden')
    
    missing_df = df[missing_columns]
    missing_df['distribution'] = 1
    
    churn_reason_dist = missing_df[['uitdiensttreding_reden', 'distribution']].groupby('uitdiensttreding_reden').sum()
    for col in missing_columns[:-1]:
        churn_reason_dist[f'{col}_missing'] = missing_df.loc[missing_df[col].isna(), ['uitdiensttreding_reden', 'distribution']].groupby('uitdiensttreding_reden').sum()
        df = df.loc[df[col].notna()]
        
    print(churn_reason_dist.apply(lambda c: round(c*100/c.sum())))
    
    return df