from cStringIO import StringIO
from xml.etree import ElementTree as ET

import requests
from scrapy.selector import Selector, XmlXPathSelector
from scrapy.spider import Spider


def parse_single_element(element, name):
    """
    Helper function to parse a single XML element for name,
    returns dict of the key and text.
    """
    data = {}
    for key in element:
        if key.tag == name:
            data[name] = key.text
    return data


def parse_single_listing(listing):
    """
    Parse an individual listing for the following:
        Location - StreetAddress
        ListingDetails - Price, MlsId, MlsName, DateListed
        BasicDetails - Description, Bathrooms
        RichDetails - Appliances
    """
    location_results = listing.iter('Location')
    for item in location_results:
        loc_data = parse_single_element(item, 'StreetAddress')

    listing_results = listing.iter('ListingDetails')
    for item in listing_results:
        listing_data = parse_single_element(item, 'Price')

    print listing_data


def get_data_feed(url):
    """ Get a data feed from url, return dataframe """
    response = requests.get(url)
    tree = ElementTree.fromstring(response.content)

    tree.write('sample_data.xml')
    for listing in tree.getchildren():
        parse_single_listing(listing) 


def write_xml_to_file(url, location):
    """ GET XML from 'url', write to local file 'location' """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file = open(location, 'w')
            file.write(response.content)
            file.close()
            return "Successfully wrote to file"
        return ("Error %s with unexpected response status code" %
                response.status_code)
    except requests.exceptions.ConnectionError as e:
        return ("Error %e with connecting to url" % e)


def read_xml_schema(xml_schema):
    """ returns xml_schema (XSD) file as a string """
    with open(xml_schema, 'r') as schema_file:
        schema = schema_file.read()
    return schema


if __name__ == '__main__':
    print 'Running'
    local_file = 'sample_data.xml'
    schema_file = 'schema.xsd'

    # get our xml data from a url source
    write_xml_to_file(
        url='http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml',
        location=local_file)

    # verify data against a schema
    #schema = read_xml_schema(schema_file)
    #valid = StringIO(schema)

    #MrXMLParse.run()
