# improved-parakeet
Python Data ETL with scrapy, luigi, and pandas

# Problem Description

Write a script to download and parse the given XML feed, manipulate some of the data, and deliver a CSV of the required fields. You may use any additional libraries that you wish, please include a requirements.txt if you do.

## CSV Requirements:

Contains only properties listed from 2016 [DateListed]
Contains only properties that contain `and' in the Description field
CSV ordered by DateListed
Required fields:
MlsId
MlsName
DateListed
StreetAddress
Price
Bedrooms
Bathrooms
Appliances (all sub-nodes comma joined)
Rooms (all sub-nodes comma joined)
Description (the first 200 characters)

## Technical Requirements

Interpreter version: python 2.7
Reasonable unit test coverage
All libraries used must be documented in requirements.txt
We will be using pip install -r requirements.txt prior to running your code
Raw information to parse / feed url
http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml
This feed must be downloaded from with in the script, raw data must not be downloaded manually

# About

Building out a data extraction and transformation system using the following tools:

* Scrapy for data extraction (from an XML endpoint).
    * The code is in the `extract` directory. This data extraction creates a JSON file, but the idea is that we store our data somewhere so we can later look at it.
* Luigi for data transformation.
    * The code is in the `transform` directory. This data transformation creates a CSV file, but the idea is that we can run transformations on our earlier data and can export it out in a new format.
* Misc data exploration code in in the `explore` directory

# Setup

Currently using:

* Python 2.7
* Install requirements with `pip install -r requirements.txt`

# Run

## Run Data Extraction with **scrapy**

In **extract** dir, run `scrapy crawl listing -o ../transform/listings.json` to
run the ListingSpider (which will crawl through an XML endpoint) and we will
save the output to a `./transform/listings.json`

## Run Data Transformation with **luigi** and **pandas**

In **transform** dir, run `python run_transform.py TestListingsCSV --local-scheduler`

You should see an output file with the transformed data in `transform/listings.csv`.
