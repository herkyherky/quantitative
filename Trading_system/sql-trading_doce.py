import pymysql
import time
time_tuple = time.localtime(time.time())
timedata='d'+str(time_tuple[0])+str(time_tuple[1])+str(time_tuple[2])
if len(str(time_tuple[3]))==1:
    h='0'+str(time_tuple[3])
else:
    h=str(time_tuple[3])
if len(str(time_tuple[4]))==1:
    m='0'+str(time_tuple[4])
else:
    m=str(time_tuple[4])
if len(str(time_tuple[5]))==1:
    s='0'+str(time_tuple[5])
else:
    s=str(time_tuple[5])
tradingtime=h+m+s


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='kali',
    database='tradingdoce'
)

create_table_query = '''
CREATE TABLE IF NOT EXISTS '''+timedata+''' (
    id INT PRIMARY KEY AUTO_INCREMENT,
    time TIME,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    transaction_type ENUM('buy', 'sell'),
    volume DECIMAL(12, 2)
)
'''
with conn.cursor() as cursor:
    cursor.execute(create_table_query)
  


insert_query = 'INSERT INTO '+timedata+' (time, name, price, transaction_type,volume) VALUES (%s, %s, %s, %s, %s)'
data = [
    (tradingtime, 'John', 10.99, 'buy','72000')
]
with conn.cursor() as cursor:
    cursor.executemany(insert_query, data)

conn.commit()

conn.close()