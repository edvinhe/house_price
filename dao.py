
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

########################################################################################################
#
# DAO
#
#########################################################################################################

class DAO(object):
    def __init__(self):
        self.__db = MySQLdb.connect("localhost","root","whalewatch1!","house_price" )
        self.__cursor = self.__db.cursor()
        self.__db.set_character_set('utf8')


    def insert(self, sql):
        if not sql:
            return

        try:
            self.__cursor.execute(sql)
            self.__db.commit()
        except MySQLdb.Error, e:
            self.__db.rollback()
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

    def queryForExistence(self, sql):
        if not sql:
            return False

        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()
            if results:
                return True
            else:
                return False

        except:
            pass

    def query(self, sql):
        if not sql:
            return None

        try:
            self.__cursor.execute(sql)
            results = self.__cursor.fetchall()

            return results
        except:
            pass




    def close(self):
        self.__db.close()


