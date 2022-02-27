# This is a sample Python script.
import pandas as pd
import json
from cleaning_csv.common_utils import create_formated_date
from cleaning_csv.clinical_trials import clean_trials
import operator
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


# function to filter the name of the drug mentionned in the title
# output: lower case name of the input string, splitted by space
def small_single_string(uncleaned_string):
    return uncleaned_string.lower().strip().split(" ")


# detect all titles containing the name of each drug
# output: concatenate pubmed publications with the clinical trials publications
# publications are identified by id, the name of the journal and the date
def publications(df_pubmed, df_trials, name_drug):
    json_value = list()
    name_drug = name_drug.replace(",", "")
    cleaned_name_drug = small_single_string(name_drug)[0]
    # check mentionning in df_pubmed
    for i_pubmed in range(len(df_pubmed)):
        if cleaned_name_drug in small_single_string(df_pubmed.iloc[i_pubmed]['title']):
            json_value.append(
                {
                    'id': float(df_pubmed['id'].iloc[i_pubmed]),
                    'title': df_pubmed['title'].iloc[i_pubmed],
                    'journal': df_pubmed['journal'].iloc[i_pubmed],
                    'date_format': df_pubmed['date_format'].iloc[i_pubmed],
                }
            )
    # check mentionning in df_trials
    for i_trials in range(len(df_trials)):
        if cleaned_name_drug in small_single_string(df_trials.iloc[i_trials]['scientific_title']):
            json_value.append(
                {
                    'id': df_trials['id'].iloc[i_trials],
                    'title': df_trials['scientific_title'].iloc[i_trials],
                    'journal': df_trials['journal'].iloc[i_trials],
                    'date_format': df_trials['date_format'].iloc[i_trials],
                }
            )
    return json_value


def create_json_file(json_dict):
    return json.dump(json_dict)


#create json output file
def create_json_dict(df_pubmed, df_trials, df_drugs):
    json_dict = dict()
    for name_drug in df_drugs['drug']:
        json_dict[small_single_string(name_drug)[0]] = publications(df_pubmed=df_pubmed_clean, df_trials=df_trials_clean, name_drug=name_drug)
    return json_dict

def top_mentionning_journal(data):
#find the name of the journal that has the highest number of different drugs mentioned
    dict_journal = dict()
    # explore each item of the json file by key, so to say by drug
    for drug in list(data.keys()):
        list_journal_drug = list()
        for i in range(len(data[drug])):
            curr_journal = str(data[drug][i]['journal'])
            if curr_journal not in list_journal_drug:
                # append a temporary list per key to have the list of all the journals that mention the current drug
                list_journal_drug.append(curr_journal)
        for elt in list_journal_drug:
            # increment the correspond value of the final dict each time a new drug is mentionned in the journal
            if elt in list(dict_journal.keys()):
                dict_journal[elt] += 1
            else:
                dict_journal[elt] = 1
    #find the journal, so to say the key, that has the highest value
    result = max(dict_journal.items(), key=operator.itemgetter(1))[0]
    return result


if __name__ == '__main__':
    df_trials = pd.read_csv('cleaning_csv/csv/clinical_trials.csv')
    df_trials_clean = clean_trials(df_trials)

    df_pubmed = pd.read_csv('cleaning_csv/csv/pubmed.csv')
    df_pubmed_clean = create_formated_date(df_pubmed)
    df_drugs = pd.read_csv('cleaning_csv/csv/drugs.csv')

    json_dict = create_json_dict(df_pubmed=df_pubmed_clean, df_trials=df_trials_clean, df_drugs=df_drugs)

    with open("output.json", "w") as write_file:
        json.dump(json_dict, write_file)



    ## part 4 of the exercise: get the journal with the highest number of different drugs mentionned

    ## loading the generated json file
    # with open('output.json', 'r') as f:
    #     data = json.load(f)

    ## call the function defined as above
    #top_mentionning_journal(data)