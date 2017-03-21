
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

########################################################################################################
#
# Web Crawler
#
#########################################################################################################

class Crawler(object):
    def __init__(self, locationMapping, locationMappingToInt):
        self.__locationMapping = locationMapping.getLocationMapping()
        self.__locationMappingToInt = locationMappingToInt.getLocationMappingToInt()


    def craw(self, url):
        if not url.strip():
            print('url is empty')

        resp = requests.get(url.strip())

        if resp.status_code != 200:
            print('=====>Error: failed to craw << ' + url + ' >>, status_code = ' + str(resp.status_code))
            return


        return self.__locationMapping[url.split('/')[-2].strip()], self.__locationMappingToInt[url.split('/')[-2].strip()], resp.text

    def crawCommunity(self, url):
        if not url.strip():
            print('url is empty')

        resp = requests.get(url.strip())

        if resp.status_code != 200:
            print('=====>Error: failed to craw << ' + url + ' >>, status_code = ' + str(resp.status_code))

        return resp.text

