import cx_Oracle
import json
import config.db as dbcfg


class oraconn():
    def __init__(self, condb="mis"):
        self.condb = condb

        cfg = dbcfg.dbconfig[condb]

        self.conn = cx_Oracle.connect('{0}/{1}@{2}'.format(cfg['username'], cfg['password'], cfg['host']), encoding = "UTF-8", nencoding = "UTF-8")
        self.res = []
        self.fields = {}
        # print ('Your database version..')
        # print (self.conn.version)

    def execute(self, sql):
        self.res = []
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.res = cursor

        self.fields = {}

        column = 0
        for d in cursor.description:
            self.fields[d[0]] = column
            column = column + 1

    def get_fields(self):
        return self.fields

    def result(self):
        return self.res

    def close(self):
        self.conn.close()