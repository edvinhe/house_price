#!/usr/bin/emv python
# -*- coding: utf-8 -*-


########################################################################################################
#
# Shanghai location mappings to int for machine learning
#
#########################################################################################################
class LocationMappingToInt(object):
    def __init__(self):
        self.__locationMappingToInt = {
            'pudongxinqu': 1, 'minhang':2, 'baoshan':3, 'xuhui':4,
            'putuo':5, 'yangpu':6, 'changning':7, 'songjiang':8,
            'jiading':9, 'huangpu':10, 'jingan':11, 'zhabei':12,
            'hongkou':13, 'qingpu':14, 'fengxian':15, 'jinshan':16,
            'chongming':17, 'shanghaizhoubian':18
        }

    def getLocationMappingToInt(self):
        return self.__locationMappingToInt


