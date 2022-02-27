import pandas as pd
from cleaning_csv.common_utils import create_formated_date

def clean_trials(df_trials):
    # fix row id NCT03490942 by removing duplicate and fixing missing values
    # Here it is done manually because every case is to be discussed
    df_trials.iloc[5]['journal'] = 'Journal of emergency nursing'
    df_trials.iloc[7]['journal'] = 'Journal of emergency nursing'
    df_trials = df_trials.drop(labels=[6], axis=0)
    df_trials = df_trials.reset_index(drop=True)

    # removing row with empty title
    df_trials = df_trials.drop(labels=[2], axis=0)

    # create new column with same format for dates
    df_trials_final = create_formated_date(df_trials)

    return df_trials_final

if __name__ == '__main__':
    df_trials = pd.read_csv('csv/clinical_trials.csv')
    df_trials_clean = clean_trials(df_trials)