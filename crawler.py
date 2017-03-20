
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

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

