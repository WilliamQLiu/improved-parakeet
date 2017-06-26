# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from scrapy.selector import Selector

from ..items import ListingsItem


class ListingSpider(XMLFeedSpider):
    """ Run with `scrapy crawl listing` """
    name = 'listing'
    allowed_domains = ['http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml']
    start_urls = ['http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml']
    iterator = 'iternodes'
    itertag = 'Listing'

    def parse_node(self, response, node):
        """ Parse a node for a specific Item """
        #self.logger.info('Hi this is <%s> node!: %s', self.itertag, ''.join(node.extract()))
        try:
            item = ListingsItem()
            item['mls_id'] = node.xpath('ListingDetails/MlsId/text()').extract_first()
            item['mls_name'] = node.xpath('ListingDetails/MlsName/text()').extract_first()
            item['mls_date_listed'] = node.xpath('ListingDetails/DateListed/text()').extract_first()
            item['street_address'] = node.xpath('Location/StreetAddress/text()').extract_first()
            item['price'] = node.xpath('ListingDetails/Price/text()').extract_first()
            item['bedrooms'] = node.xpath('BasicDetails/Bedrooms/text()').extract_first()
            item['bathrooms_full'] = node.xpath('BasicDetails/Bathrooms/FullBathrooms/text()').extract_first([])
            item['bathrooms_half'] = node.xpath('BasicDetails/Bathrooms/HalfBathrooms/text()').extract_first([])
            item['appliances'] = self._get_sub_nodes(node, './/RichDetails/Appliances/Appliance/text()')
            item['rooms'] = self._get_sub_nodes(node, './/RichDetails/Rooms/Room/text()')
            item['description'] = self._get_short_description(node, 'BasicDetails/Description/text()')
            return item
        except Exception as e:
            self.logger.error("A response from %s arrived with exception %s" % (response.url, e))

    def _get_sub_nodes(self, node, xpath):
        """ Return list of node's sub-nodes values joined by commas """
        list_items = []
        for item in node.xpath(xpath).extract():
            list_items.append(item)
        return list_items

    def _get_short_description(self, node, xpath):
        """ Return a shortened description """
        MAX_DESC_LENGTH = 200
        description = node.xpath(xpath).extract_first()
        return str(description)[:MAX_DESC_LENGTH]
