#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests

########################################################################################################
########################################################################################################
class LocationMapping(object):
    def __init__(self):
        self.__locationMapping = {
            'pudongxinqu': '浦东新区', 'minhang':'闵行区', 'baoshan':'宝山区', 'xuhui':'徐汇区',
            'putuo':'普陀区', 'yangpu':'杨浦区', 'changning':'长宁区', 'songjiang':'松江区',
            'jiading':'嘉定区', 'huangpu':'黄浦区', 'jingan':'静安区', 'zhabei':'闸北区',
            'hongkou':'虹口区', 'qingpu':'青浦区', 'fengxian':'奉贤区', 'jinshan':'金山区',
            'chongming':'崇明区', 'shanghaizhoubian':'上海周边'
        }

    def getLocationMapping(self):
        return self.__locationMapping


########################################################################################################
########################################################################################################
class Crawler(object):
    def __init__(self, locationMapping):
        self.__locationMapping = locationMapping.getLocationMapping()
        

    def craw(self, url):
        if not url.strip():
            print('url is empty')

        resp = requests.get(url.strip())

        if resp.status_code != 200:
            print('=====>Error: failed to craw << ' + url + ' >>, status_code = ' + str(resp.status_code))
            return


        return self.__locationMapping[url.split('/')[-2].strip()], resp.text


########################################################################################################
########################################################################################################
class HouseInfoParser(object):
    def __init__(self):
        pass

    def parseHttpResponse(self, houseLocation, houseInfo):
        if not houseLocation or not houseInfo:
            print('Either houseLocation = ' + houseLocation + ' or houseInfo = '+ houseInfo + 'are  not correct!')

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

        return houseLocation, neighborhood, houseBedrooms, houseSize, houseFloor, houseBuiltDate, housePrice, houseAvgPrice

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


########################################################################################################
########################################################################################################
class DAO(object):
    def __init__(self):
        pass


########################################################################################################
########################################################################################################
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





