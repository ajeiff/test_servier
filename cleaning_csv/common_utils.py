import pandas as pd

def create_formated_date(df):
    # create new column with same formated dates
    df['date'] = pd.to_datetime(df['date'])
    df['date_format'] = df['date'].dt.strftime('%d/%m/%Y')
    df_final = df.drop(['date'], axis=1)
    return df_final