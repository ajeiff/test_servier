import pandas as pd
from common_utils import create_formated_date

if __name__ == '__main__':
    df_pubmed = pd.read_csv('csv/pubmed.csv')
    df_pubmed_clean = create_formated_date(df_pubmed)