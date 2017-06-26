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
        df = self._rename_columns(df)
        df = self._datetime_sort_filter(df)
        df = self._description_filter(df)
        df.to_csv(LISTINGS_OUTPUT_FILENAME, index=False)

    def _rename_columns(self, df):
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

    def _datetime_sort_filter(self, df):
        """ Change column to datetime, filter by time, and sort """
        df['DateListed'] = pd.to_datetime(df['DateListed'])
        df = df[(df['DateListed'] >= '2016-01-01') & (df['DateListed'] < '2017-01-01')]
        df = df.sort_values(by='DateListed', ascending=True)
        return df

    def _description_filter(self, df):
        """ Must have 'and' in the description field and return first 200 chars only """
        MAX_DESC_LENGTH = 200
        df = df[df['Description'].str.contains("and")]
        df['Description'].map(lambda x: x[:MAX_DESC_LENGTH])
        return df


if __name__ == '__main__':
    luigi.run()
