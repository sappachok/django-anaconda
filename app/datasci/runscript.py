import sys
import io
import urllib, base64
import psycopg2
import json

class OutputBuffer:
    def __init__(self):
        self.output_list = []

    def setval(self, content_type, val):
        output = {'type': content_type, 'val': val}
        self.output_list.append(output)

    def setfigure(self, plt):
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        output = 'data:image/png;base64,' + urllib.parse.quote(string)
        self.setval("image", output)

    def val(self):
        print(json.dumps(self.output_list))

class loader:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(user="postgres",
                                          password="postgres",
                                          host="db",
                                          port="5432",
                                          database="postgres")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL : {0}" + format(error))

    def dbversion(self):
        try:
            cursor = self.connection.cursor()
            # Print PostgreSQL Connection properties
            print(self.connection.get_dsn_parameters())
            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - {0}".format(record))
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL : {0}" + format(error))

    def get_script(self, pid):
        try:
            cursor = self.connection.cursor()
            select = """SELECT script FROM editor_pythonlab WHERE name='{0}'""".format(pid)
            cursor.execute(select)
            record = cursor.fetchone()
            #print(record[0])
            self.script = record[0]
            return self.script
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL : {0}" + format(error))

pid = sys.argv[1]
python = loader()
tmp = python.get_script(pid)
op = OutputBuffer()
exec(tmp)
op.val()
#script.dbversion()
#res = connectdb()
#print(res)

