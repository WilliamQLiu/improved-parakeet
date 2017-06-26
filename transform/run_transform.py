""" Run with 'python run_transform.py TransformListings --local-scheduler' """
import subprocess
from datetime import datetime

import luigi
import pandas as pd


LISTINGS_INPUT_FILENAME = 'listings.json'
LISTINGS_OUTPUT_FILENAME = 'listings.csv'
MAX_DESC_LENGTH = 200

class GetListings(luigi.Task):
    """ Task to check that data extraction file exists """
    def output(self):
        return luigi.LocalTarget(LISTINGS_INPUT_FILENAME)


class TransformListings(luigi.Task):
    """ Task to Transform parsed listings from json to csv """

    def requires(self):
        """ List of previous tasks required """
        return [GetListings()]

    def run(self):
        df = pd.read_json(LISTINGS_INPUT_FILENAME)
        df = self._rename_columns(df)
        df = self._datetime_sort_filter(df)
        df = self._description_filter(df)
        return df.to_csv(LISTINGS_OUTPUT_FILENAME, index=False)

    def output(self):
        return luigi.LocalTarget(LISTINGS_OUTPUT_FILENAME)

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
        """ Must have 'and' in the description field and return first X chars only """
        df = df[df['Description'].str.contains("and")]
        df['Description'] = df['Description'].map(lambda x: x[:MAX_DESC_LENGTH])
        return df


class TestListingsCSV(luigi.Task):
    """ Test Transformations """

    def requires(self):
        return [TransformListings()]

    def run(self):
        df = pd.read_csv(LISTINGS_OUTPUT_FILENAME)
        print df.head()
        self._test_df_headers(df)
        self._test_df_datetime(df)
        self._test_df_description(df)

    def _test_df_headers(self, df):
        """ DataFrame headers are what we expect """
        assert list(df.columns.values) == [
            'Appliances', 'BathroomsFull', 'BathroomsHalf', 'Bedrooms',
            'DateListed', 'Description', 'MlsId', 'MlsName', 'Price',
            'Rooms', 'StreetAddress'
        ]

    def _test_df_datetime(self, df):
        """ DataFrame time is limited correctly """
        date_raw = df['DateListed'].iloc[0]  # e.g. '2016-01-07 00:00:00'
        first_date_time = datetime.strptime(date_raw, "%Y-%m-%d %H:%M:%S")
        assert first_date_time >= datetime(2016, 1, 1, 0, 0) and \
            first_date_time < datetime(2017, 1, 1, 0, 0)

    def _test_df_description(self, df):
        max_length = df['Description'].map(lambda x: len(x)).max()
        assert max_length <= MAX_DESC_LENGTH


if __name__ == '__main__':
    luigi.run()
