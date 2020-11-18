#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This scripts downloads microdata for the Enem exam from 2009 until 2019 from the
Inep website. The data contains information on exam results for different subjects
and answers to the questionnaire exam takers have to answer.

In order to do that, it downloads and unzips the data and saves the desired files
as csvs.

Output:
    data/enem_2009.csv
    data/enem_2010.csv
    data/enem_2011.csv
    data/enem_2012.csv
    data/enem_2013.csv
    data/enem_2014.csv
    data/enem_2015.csv
    data/enem_2016.csv
    data/enem_2017.csv
    data/enem_2018.csv
    data/enem_2019.csv

By: @gabrielsgaspar
"""

# Import libraries
import csv, os, wget
import urllib
import time
from urllib.request import urlopen, Request
from zipfile import ZipFile
from io import TextIOWrapper, BytesIO
from tqdm.auto import tqdm

# Define function to verify data directory exists
def verify_directory():
    """
    This function verifies if the data directory exists in the root of the repo
    for this project and creates a folder in case it doesn't.

    Argument:
        None
    Output:
        ../output: a repository

    """
    # Verify if directory exists and create directory if not
    if not os.path.exists("../data/enem"):
        os.makedirs("../data/enem")

# Define function to download zipped file
def download_zip(url, save_name):
    """
    Downloads zip files from url and saves it under save_name in the data folder
    """
    # Download data and save in data with name in argument
    wget.download(url, out = "../data/enem/{}".format(save_name))

# Define function to unzip downloaded file
def unzip_file(zip_name, csv_name, new_name):
    """
    Unzips files extracted in download_zip function, extracts only relevant csvs and saves them
    """
    # Open zip files
    with ZipFile(zip_name) as zf:
        with zf.open("DADOS/{}.csv".format(csv_name.upper()), "r") as infile:
            file = csv.reader(TextIOWrapper(infile, encoding = "utf-8", errors = "ignore"))
            # Open as writer
            with open(new_name, "w") as new_file:
                writer = csv.writer(new_file)
                # Loop over to save
                for line in file:
                    writer.writerow(line)

# Define function to delete zip file
def delete_zip(ext):
    """
    Deletes files with the passed argument in current working directory
    """
    # Get files in directory in list
    files = os.listdir("../data/enem")
    # Loop to find files with extension and delete
    for file in files:
        if file.endswith(ext):
            os.remove(os.path.join("../data/enem/", file))

# Define main function to call script
def main():
    # Print message for download
    print("Initiating the download of ENEM data from Inep.\n")
    print("This might take a while, so grab a cup of coffee while this runs\n")
    print("""\
                 ( (
                  ) )
                (----)-)
                 \__/-'
                `----'      @gabrielsgaspar
        """)
    # Set links to download
    enem_links = {
                #"enem_2009":"http://download.inep.gov.br/microdados/microdados_enem2009.zip",
                #"enem_2010":"http://download.inep.gov.br/microdados/microdados_enem2010_2.zip",
                #"enem_2011":"http://download.inep.gov.br/microdados/microdados_enem2011.zip",
                #"enem_2012":"http://download.inep.gov.br/microdados/microdados_enem2012.zip",
                #"enem_2013":"http://download.inep.gov.br/microdados/microdados_enem2013.zip",
                #"enem_2014":"http://download.inep.gov.br/microdados/microdados_enem2014.zip",
                #"enem_2015":"http://download.inep.gov.br/microdados/microdados_enem2015.zip",
                #"enem_2016":"http://download.inep.gov.br/microdados/microdados_enem2016.zip",
                #"enem_2017":"http://download.inep.gov.br/microdados/microdados_enem2017.zip",
                #"enem_2018":"http://download.inep.gov.br/microdados/microdados_enem2018.zip",
                "enem_2019":"http://download.inep.gov.br/microdados/microdados_enem_2019.zip"
                }
    # Verify if data directory exists
    print("Verifying if data directory for ENEM exists ...")
    verify_directory()
    time.sleep(1)
    # Loop through available years to gather data
    for key in tqdm(enem_links.keys()):
        # Download the data as a zip file
        #download_zip(enem_links[key],str(key + ".zip"))
        time.sleep(1)
        # Unzip the zipper file
        unzip_file("../data/enem/{}.zip".format(key), enem_links[key].split("/")[-1].replace(".zip", ""), "../data/enem/{}.csv".format(key))
        time.sleep(1)
    # Delete old zip file
    delete_zip(".zip")
    # Complete output message
    print("Downloading of ENEM data complete!")


if __name__ == "__main__":
    main()
