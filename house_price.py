#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from location_mapping import LocationMapping
from crawler import Crawler
from house_info_parser import HouseInfoParser
from string_to_int_mapping import LocationMappingToInt


def getHouseInfo():
    locationMapping = LocationMapping()
    locationMappingToInt = LocationMappingToInt()
    crawler = Crawler(locationMapping, locationMappingToInt)
    houseInfoParser = HouseInfoParser()

    # Crawl lianjia ershoufang
    lianjiaSiteName = 'http://sh.lianjia.com'
    lianjiaErShouFang = 'ershoufang'

    for k, v in locationMapping.getLocationMapping().iteritems():
        for i in xrange(100):
            crawUrl = lianjiaSiteName + '/' + lianjiaErShouFang + '/' + k + '/d' + repr(i+1)

            location, locationToInt, houseInfo = crawler.craw(crawUrl)

            if len(houseInfo):
                neighborhood, houseBedrooms, houseSize, houseFloor, houseBuiltDate, housePrice, houseAvgPrice = houseInfoParser.parseHttpResponse(houseInfo)
            if not len(neighborhood):
                break

            # Inser the data into database
            for i in xrange(len(neighborhood)):
                print location, '---', locationToInt, '---', neighborhood[i], '---', houseBedrooms[i], '---', houseSize[i], '---', houseFloor[i], '---', houseBuiltDate[i], '---', housePrice[i], '---', houseAvgPrice[i]



def getCommunityInfo():
    locationMapping = LocationMapping()
    locationMappingToInt = LocationMappingToInt()
    crawler = Crawler(locationMapping, locationMappingToInt)
    houseInfoParser = HouseInfoParser()

    lianjiaSiteName = 'http://sh.lianjia.com'
    lianjiaXiaoqu = 'xiaoqu'

    # 100 communities
    for i in xrange(100):
        crawUrl = lianjiaSiteName + '/' + lianjiaXiaoqu + '/d' + repr(i+1) + 'rs'

        communityResp = crawler.crawCommunity(crawUrl)
        if len(communityResp):
            communityInfo = houseInfoParser.parseCommunityHttpResponse(communityResp)

        if not len(communityInfo):
            break

        for i in xrange(len(communityInfo)):
            print communityInfo[i]




def main():
    getCommunityInfo()

########################################################################################################
#
# Main Program starts from here
#
#########################################################################################################
if __name__ == '__main__':
    main()




