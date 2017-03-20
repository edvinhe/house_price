#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from location_mapping import LocationMapping
from crawler import Crawler
from house_info_parser import HouseInfoParser


########################################################################################################
#
#
# Main Program starts from here
#
#########################################################################################################
if __name__ == '__main__':
    locationMapping = LocationMapping()
    crawler = Crawler(locationMapping)
    houseInfoParser = HouseInfoParser()

    # Crawl lianjia ershoufang
    lianjiaSiteName = 'http://sh.lianjia.com'
    lianjiaErShouFang = 'ershoufang'

    for k, v in locationMapping.getLocationMapping().iteritems():
        for i in xrange(100):
            crawUrl = lianjiaSiteName + '/' + lianjiaErShouFang + '/' + k + '/d' + repr(i+1)

            location, houseInfo = crawler.craw(crawUrl)

            if location and len(houseInfo):
                houseLocation, neighborhood, houseBedrooms, houseSize, houseFloor, houseBuiltDate, housePrice, houseAvgPrice = houseInfoParser.parseHttpResponse(location, houseInfo)
            if not len(neighborhood):
                break

            # Inser the data into database
            for i in xrange(len(neighborhood)):
                print houseLocation, '---', neighborhood[i], '---', houseBedrooms[i], '---', houseSize[i], '---', houseFloor[i], '---', houseBuiltDate[i], '---', housePrice[i], '---', houseAvgPrice[i]





