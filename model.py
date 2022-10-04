from xmlrpc.client import Boolean
from data_cleaning import *
from feature_preparation import *
import sys
import os

def preprocessing_pipeline(df: pd.DataFrame,
                           most_recent_entry: Boolean = True, 
                           impute_age: Boolean = True, 
                           impute_experience: Boolean = True,
                           remove_missing: Boolean = True):
    if most_recent_entry:
        df = get_most_recent_entry(df)
    
    if impute_age:
        df = impute_missing_age(df, drop_age_column=True)
    
    if impute_experience:
        df = impute_missing_experience(df, drop_experience_column=True)
        
    if remove_missing:
        df = remove_missing_data(df, missing_columns=['stad', 'afdeling'])
        
    return df


def cox_model_preparation(df: pd.DataFrame):
    df_features = feature_preparation(df)
    df_transformed = transform_categorical_variables(df_features, categorical_variables=['stad', 'afdeling', 'geslacht', 'BUSINESS_UNIT'])
    
    return df_transformed