#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from dao import DAO
from location_mapping import LocationMapping
from string_to_int_mapping import LocationMappingToInt
from model_training import Model

def getLocationMenu():
    temp = {}
    locationMapping = LocationMapping().getLocationMapping()
    locationMappingToInt = LocationMappingToInt().getLocationMappingToInt()
    for k, v in locationMapping.iteritems():
        temp[locationMappingToInt[k]] = v

    for k, v in temp.iteritems():
        print k, '-> ', v

    return temp


def getCommunityCode(communityName):
    dao = DAO()

    querySQL = "SELECT * FROM community"
    results = dao.query(querySQL)
    for result in results:
        if result[1] == communityName:
            return result[2]

    return None


def main():
    reload(sys)
    sys.setdefaultencoding("utf-8")

    print '=' * 50
    print '=' + ' ' * 10 + '欢迎使用上海房屋预测机器人' + ' ' * 12 + '='
    print '=' + ' ' * 48 + '='

    print '= 1. 请选择房屋所在的区:'
    locationMapping = getLocationMenu()
    userInput = int(raw_input('请选择: '))
    # TODO validate user input
    locationCode = userInput
    print

    # 2. input community name
    userInput = raw_input('2. 请输入小区名： ')
    communityCode = getCommunityCode(userInput.strip())

    # 3. bedrooms
    userInput = int(raw_input('3. 请输入房间数: '))
    bedrooms = userInput

    # 4. houseSize
    userInput = int(raw_input('4. 请输入房间大小：'))
    houseSize = userInput

    # 5. houseFloor
    userInput = int(raw_input('5. 请输入房屋层数：'))
    houseFloor = userInput

    # 6. houseBuiltDate
    userInput = int(raw_input('4. 请输入房屋建造时间：'))
    houseBuiltDate = userInput

    # 7. houseAvgPrice 
    userInput = int(raw_input('5. 请输入房屋均价：'))
    houseAvgPrice = userInput

    print '=' * 50    

    model = Model()
    print '需要预测的数据为: ', locationCode, ', ', communityCode, ', ', bedrooms, ', ', houseSize, ', ', houseFloor, ', ', houseBuiltDate, ', ', houseAvgPrice
    print '=' * 50
    print '线性回归预测出来的价格为：', model.predictPrice([[locationCode, communityCode, bedrooms, houseSize, houseFloor, houseBuiltDate, houseAvgPrice]])

    print '-' * 50
    print '二阶多项式回归预测出来的价格为：', model.polyPredictPrice([[locationCode, communityCode, bedrooms, houseSize, houseFloor, houseBuiltDate, houseAvgPrice]], 2)

    print '-' * 50
    print '三阶多项式回归预测出来的价格为：', model.polyPredictPrice([[locationCode, communityCode, bedrooms, houseSize, houseFloor, houseBuiltDate, houseAvgPrice]], 3)

if __name__ == '__main__':
    main()
