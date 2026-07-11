import pymysql


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='kali',
    database='tradinghold')


cursor = conn.cursor()
query = "select * from hold where id =2;"
cursor.execute(query)
results = cursor.fetchall()
if results!='()':
    name=results[0][1]
    v=results[0][-1]
    n=results[0][-3]
    print(name,v,n)