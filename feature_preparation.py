import pandas as pd

def feature_preparation(df: pd.DataFrame, 
                        use_years_to_pension = True):
    df['event'] = 0
    df.loc[df['STATUS'] != 'Actief', 'event'] = 1
    
    if use_years_to_pension:
        df['years_to_pension'] = 65 - df['derived_age']
        df.drop('derived_age', axis=1)
        age_col = 'years_to_pension'
    else: 
        age_col = 'derived_age'
    
    return df[['stad', 'afdeling', 'geslacht', 'BUSINESS_UNIT', age_col, 'derived_experience', 'event']]

def transform_categorical_variables(df: pd.DataFrame,
                                    categorical_variables):
    df_dummies = pd.get_dummies(df[categorical_variables], drop_first=True)
    df = df.drop(categorical_variables, axis=1)
    
    return pd.concat([df, df_dummies], axis=1)   