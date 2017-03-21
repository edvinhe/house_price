#!/usr/bin/env python
# -*- coding: utf-8 -*-

from location_mapping import LocationMapping
from crawler import Crawler
from house_info_parser import HouseInfoParser
from string_to_int_mapping import LocationMappingToInt
from dao import DAO

def getCommunityInfo():
    locationMapping = LocationMapping()
    locationMappingToInt = LocationMappingToInt()
    crawler = Crawler(locationMapping, locationMappingToInt)
    houseInfoParser = HouseInfoParser()
    dao = DAO()

    lianjiaSiteName = 'http://sh.lianjia.com'
    lianjiaXiaoqu = 'xiaoqu'

    count = 0
    # 100 pages
    for i in xrange(100):
        crawUrl = lianjiaSiteName + '/' + lianjiaXiaoqu + '/d' + repr(i+1) + 'rs'

        communityResp = crawler.crawCommunity(crawUrl)
        if len(communityResp):
            communityInfo = houseInfoParser.parseCommunityHttpResponse(communityResp)

        if not len(communityInfo):
            break

        for i in xrange(len(communityInfo)):
            # If it already exists
            querySQL = "SELECT * FROM community where community_name='%s'" % communityInfo[i].strip()
            if dao.queryForExistence(querySQL):
                continue

            count = count + 1
            insertSQL = "INSERT INTO community(community_name, community_code) VALUES ('%s', %d)" % (communityInfo[i].strip(), count)
            dao.insert(insertSQL)

    dao.close()


def main():
    getCommunityInfo()

########################################################################################################
#
# Main Program starts from here
#
#########################################################################################################
if __name__ == '__main__':
    main()




