""" Run with 'python run_transform.py TransformListings --local-scheduler' """
import luigi
import pandas as pd
import subprocess


LISTINGS_INPUT_FILENAME = 'listings.json'
LISTINGS_OUTPUT_FILENAME = 'listings.csv'


class TransformListings(luigi.Task):
    """ Task to Transform parsed listings from json to csv """

    def requires(self):
        """ List of previous tasks required """
        return []

    def run(self):
        df = pd.read_json(LISTINGS_INPUT_FILENAME)
        print df.head()
        return df.head()

if __name__ == '__main__':
    luigi.run()
