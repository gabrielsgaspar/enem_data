#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This scrip scrapes data from LEITOS API in DataSUS in order to gather data for
daily infections and deaths from Covid-19.

By: @gabrielsgaspar
"""

# Import libraries
import requests, json, os, time
import pandas as pd
from flatten_json import flatten
from tqdm.auto import tqdm

# Define function to verify data directory exists
def verify_directory():
    """
    This function verifies if the data directory exists in the current folder
    for this project and creates a folder in case it doesn't.

    Argument:
        None
    Output:
        ../data: a repository

    """
    # Verify if directory exists and create directory if not
    if not os.path.exists("../data/covid"):
        os.makedirs("../data/covid")

# Define function to paginate through the API
def api_call(page, username, password):
    """
    This function makes an API call to the leitos ocupaca API within DataSUS

    Arguments:
        page: a string or integer with the number of the page to request
        username: a string with the username login information for the API
        password: a string with the password login information for the API
    Output:
        json_data: a dictionary containing the information for the requested page

    """
    # Make API request for given page
    r = requests.get("https://elastic-leitos.saude.gov.br/leito_ocupacao/_search?from={}".format(str(page)), auth = (username, password))
    # Turn data into json
    json_data = json.loads(r.text)
    # Return dictionary
    return json_data

# Define function to flatten data and store in dataframe
def json_df(json_data):
    """
    This function flattens a dictionary into a dataframe.

    Argument:
        json_data: a dictionary containing the data to be flatten
    Output:
        pd.json_normalize(flat_json): a pandas dataframe containing the flatten data

    """
    # Flatten jsons to load into dataframe
    flat_json = flatten(json_data)
    # Normalize it, load into a dataframe and return result
    return pd.json_normalize(flat_json)

# Define main call function
def main():
    """
    This is the main function of the script that calls the functions defined above
    in the right order in order to loop through the API and save the final data
    as a csv file.
    """
    # Print message for download
    print("Initiating the download of Covid data from DataSUS.\n")
    print("This might take a while, so grab a cup of coffee while this runs\n")
    print("""\
                 ( (
                  ) )
                (----)-)
                 \__/-'
                `----'      @gabrielsgaspar
        """)
    time.sleep(1)
    # Verify if data folder exists and create if it does not
    print("Verifying if data directory exists ...")
    verify_directory()
    time.sleep(1)
    # Set user name and password for leito ocupacao API
    username = "user-api-leitos"
    password = "aQbLL3ZStaTr38tj"
    # Set empty list to append dataframes for pages
    df_holder = []
    # Loop through pages in API until reach end
    print("Gathering data from API ...")
    for page in tqdm(range(1, api_call(1, username, password)["hits"]["total"]["value"])):
        json_ = api_call(page, username, password)
        # Create temporary empty list to store values for this page
        page_list = []
        # Put each id information in dataframe
        for id_ in json_["hits"]["hits"]:
            # Put json dictionary as dataframe and append to list
            temporary_df = json_df(id_)
            page_list.append(temporary_df)
        # Append dataframe for page in df_holder
        df_holder.append(pd.concat(page_list))
    # Concatenate all pages into one dataframe
    print("Concatenating data ...")
    covid_df = pd.concat(df_holder)
    # Save dataframe in the data folder
    print("Saving data ...")
    covid_df.to_csv("../data/covid/covid_data.csv", index = False, encoding = "utf-8")
    # Print complete message
    print("Download of Covid data from DataSUS complete!")


if __name__ == '__main__':
    main()
