""" Run with 'python run_transform.py TransformListings --local-scheduler' """
import subprocess

import luigi
import pandas as pd


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
        import pdb
        pdb.set_trace()
        df = self._rename_columns(df)
        return df.head()

    def _rename_columns(self.df):
        """ Rename columns """
        return df.rename(columns={
            'mls_id': 'MlsId',
            'mls_name': 'MlsName',
            'date_listed': 'DateListed',
            'street_address': 'StreetAddress',
            'price': 'Price',
            'bedrooms': 'Bedrooms',
            'bathrooms_full': 'BathroomsFull',
            'bathrooms_half': 'BathroomsHalf',
            'appliances': 'Appliances',
            'rooms': 'Rooms',
            'description': 'Description'
        })

if __name__ == '__main__':
    luigi.run()
