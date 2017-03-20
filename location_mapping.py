#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
