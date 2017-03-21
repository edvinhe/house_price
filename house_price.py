#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import requests
from location_mapping import LocationMapping
from crawler import Crawler
from house_info_parser import HouseInfoParser
from string_to_int_mapping import LocationMappingToInt
from dao import DAO

def getHouseInfo():
    locationMapping = LocationMapping()
    locationMappingToInt = LocationMappingToInt()
    crawler = Crawler(locationMapping, locationMappingToInt)
    houseInfoParser = HouseInfoParser()
    dao = DAO()

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
                communityCode = queryCommunityCode(dao, neighborhood[i])
                houseBedroomsInt = extractDigitFromString(houseBedrooms[i])
                houseSizeInt = normalizeHouseSize(houseSize[i])
                houseFloorInt = normalizeHouseFloor(houseFloor[i])
                houseBuiltDateInt = normalizeHouseBuiltDate(houseBuiltDate[i])
                housePriceInt = normalizeHousePrice(housePrice[i])
                houseAvgPriceInt = normalizeHouseAvgPrice(houseAvgPrice[i])

                insertSQL = "INSERT INTO house_price(location, location_int, community_name, community_code, house_bedrooms, house_bedrooms_int, house_size, house_size_int, house_floor, house_floor_int, house_built_date, house_built_date_int, house_price, house_price_int, house_avg_price, house_avg_price_int) VALUES ('%s', %d, '%s', %d, '%s', %d, '%s', %d, '%s', %d, '%s', %d, '%s', %d, '%s', %d)" % (location, locationToInt, neighborhood[i], communityCode, houseBedrooms[i], houseBedroomsInt, houseSize[i], houseSizeInt, houseFloor[i], houseFloorInt, houseBuiltDate[i], houseBuiltDateInt, housePrice[i], housePriceInt, houseAvgPrice[i], houseAvgPriceInt)

                dao.insert(insertSQL)
                print 'Running...'

    dao.close()


def normalizeHouseAvgPrice(houseAvgPrice):
    return int(re.findall(ur'(\d+)', houseAvgPrice)[0])

def normalizeHousePrice(housePrice):
    if housePrice:
        return int(housePrice)
    return 300

def normalizeHouseBuiltDate(houseBuiltDate):
    if houseBuiltDate.strip():
        return int(re.findall(ur'(\d+)', houseBuiltDate)[0])
    return 2000

def normalizeHouseFloor(houseFloor):
    if len( houseFloor.split('/')) == 0 or len( houseFloor.split('/')) == 1:
        return 6

    temp = re.findall(ur'(\d+)', houseFloor.split('/')[1])
    return int(temp[0])

def normalizeHouseSize(houseSize):
    temp = re.findall(ur'(\d+)', houseSize)

    return int(temp[0])


def extractDigitFromString(targetString):
    temp = re.findall(ur'(\d+)', targetString)

    return reduce(lambda x, y: int(x) + int(y), temp)


def queryCommunityCode(dao, communityName):
    querySQL = "SELECT * from community WHERE community_name = '%s'" % communityName.strip()

    results = dao.query(querySQL)

    if results:
        return results[0][2]
    else:
        return 0


def main():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    getHouseInfo()

########################################################################################################
#
# Main Program starts from here
#
#########################################################################################################
if __name__ == '__main__':
    main()




