from conn_oracle import oraconn

ora = oraconn()
ora.execute('select * from s_user')
res = ora.result()

for r in res:
    print(r[0])

ora.close()