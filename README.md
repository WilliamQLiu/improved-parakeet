# improved-parakeet
Python Data ETL with scrapy, luigi, and pandas

# About

Building out a data extraction and transformation system using the following tools:

* Scrapy for data extraction (from an XML endpoint), code in **extract** dir
* Luigi for data transformation, code in **transform** dir
* Misc data exploration code in **explore** dir

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

In **transform** dir, run `python run_transform.py TransformListings --local-scheduler`

You should see an output file with the transformed data in `transform/listings.csv`.
