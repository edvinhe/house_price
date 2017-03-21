#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

########################################################################################################
#
# Parse the data crawled from the Web
#
#########################################################################################################
class HouseInfoParser(object):
    def __init__(self):
        pass

    def parseCommunityHttpResponse(self, communityResp):
        if not communityResp:
            print('communityResp = ' + communityResp + ' is empty')

        communityInfo = re.findall(ur'<div class="info-panel".*?<a name="selectDetail".*?>(.*?)</a>', communityResp, re.S)

        return communityInfo


    def parseHttpResponse(self, houseInfo):
        if not houseInfo:
            print('HouseInfo = '+ houseInfo + 'is  not correct!')

        # 1. Get neighborhood
        neighborhood = re.findall(ur'<span class="nameEllipsis".*?>(.*?)</span>', houseInfo)
        neighborhood = [self.__normalizeStr(s) for s in neighborhood]

        # 2. Get house bedrooms
        houseBedrooms = re.findall(ur'<div class="where".*?<span>(.*?)</span>', houseInfo, re.S)
        houseBedrooms = [self.__normalizeStr(s) for s in houseBedrooms]

        # 3. Get house size
        houseSize = re.findall(ur'<div class="where".*?<span>.*?</span>.*?<span>(.*?)</span>', houseInfo, re.S)
        houseSize = [self.__normalizeStr(s) for s in houseSize]

        # 4. Get house floor
        houseFloor = re.findall(ur'<div class="con".*?</span>(.*?)<', houseInfo, re.S)
        houseFloor = [self.__normalizeStr(s) for s in houseFloor]

        # To check if there will be built date tag
        houseFloorBuiltDateTag = re.findall(ur'<div class="con".*?</div>', houseInfo, re.S)
        notCompleteIndexFlag = self.__checkIfHouseFloorBUiltDateTagComplete(houseFloorBuiltDateTag)
        # 5. Get house built date
        houseBuiltDate = re.findall(ur'<div class="con".*?</span>.*?</span>.*?</span>(.*?)</div>', houseInfo, re.S)
        houseBuiltDate = self.__preProcess(houseBuiltDate, notCompleteIndexFlag)
        houseBuiltDate = [self.__normalizeStr(s) for s in houseBuiltDate]

        # 6. Get house price
        housePrice = re.findall(ur'<div class="price">.*?>(.*?)</span>', houseInfo, re.S)
        housePrice = [self.__normalizeStr(s) for s in housePrice]

        # 7. Get house average price
        houseAvgPrice = re.findall(ur'<div class="price-pre".*?>(.*?)</div>', houseInfo, re.S)
        houseAvgPrice = [self.__normalizeStr(s) for s in houseAvgPrice]

        return neighborhood, houseBedrooms, houseSize, houseFloor, houseBuiltDate, housePrice, houseAvgPrice

    def __preProcess(self, houseBuiltDate, notCompleteIndexFlag):
        temp = houseBuiltDate[:]
        for i in xrange(len(houseBuiltDate)):
            if i in notCompleteIndexFlag:
                temp[i] = ' '
            else:
                temp[i] = houseBuiltDate[i]

        return temp

    def __checkIfHouseFloorBUiltDateTagComplete(self, houseFloorBuiltDateTag):
        notCompleteIndexFlag = []
        for i in xrange(len(houseFloorBuiltDateTag)):
            if len(re.findall(r'<span>', houseFloorBuiltDateTag[i], re.S)) < 3:
                notCompleteIndexFlag.append(i)

        return notCompleteIndexFlag

    def __normalizeStr(self, rawStr):
        if '&nbsp;' in rawStr:
            return rawStr[:rawStr.index('&nbsp;')].strip()
        elif  'div' in rawStr or 'span' in rawStr or '<a' in rawStr or len(rawStr.strip()) == 0:
            return ''
        else:
            return rawStr.strip()



