import json
import requests
import pandas as pd
from datetime import datetime
from pprint import pprint
import os.path


def clean_spaces_to_df(response_obj):
    list_of_spaces = pd.DataFrame(response_obj.json()['data']['spaces'])
    return list_of_spaces


def adding_no_of_members_to_df(spaces_df):
    spaces_df['no_of_members'] = spaces_df['members'].apply(lambda x: len(x))
    return spaces_df


def takes_csv_spaces_and_downloads_it(df):
    today_date = datetime.today().date().strftime("%Y-%m-%d")
    file_name = "datasets/spaces/{}_spaces_v0.csv".format(today_date)
    for i in range(10):
        if (os.path.isfile(file_name)):
            file_name = file_name.replace("v"+str(i), "v"+str(i+1))
    df.to_csv(file_name)


query = '''
query {
  spaces(
    first: 3000,
    skip: 0,
    orderBy: "created",
    orderDirection: asc
  ) {
    id
    name
    about
    network
    symbol
    strategies {
      name
      params
    }
    admins
    members
    filters {
      minScore
      onlyMembers
    }
    plugins
  }
}
'''
try:
    response = requests.post(
        'https://hub.snapshot.org/graphql',
        '',
        json={"query": query}
        )
except Exception as e:
    print(e)
    print("Error encountered when trying to download spaces dataset")

try:
    space_df = clean_spaces_to_df(response)

except Exception as e:
    print(e)
    print("Error encountered when trying to convert json to df")

space_df = adding_no_of_members_to_df(space_df)
takes_csv_spaces_and_downloads_it(space_df)

print("Spaces data downloaded and saved")
