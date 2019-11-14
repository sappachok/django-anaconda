import cx_Oracle

class oraconn():
    def __init__(self):
        self.conn = cx_Oracle.connect('nstru_www/mis$password$mis@172.16.33.59/orcl')
        self.res = []
        print ('Your database version..')
        print (self.conn.version)

    def execute(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        self.res = c

    def result(self):
        return self.res

    def close(self):
        self.conn.close()