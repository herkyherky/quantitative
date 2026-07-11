import requests as re
import pyhttpx,time
import pymysql



url='https://quotes.sina.cn/hq/api/openapi.php/US_CategoryV2Service.getList?sort=percent&asc=0&page='
header={'User-Agent': 'Mozilla/5.0 (Windows NT +10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
session = pyhttpx.HttpSession()
stock=[]
page=0

while len(stock)<5:
    page+=1
    r=re.get(url+str(page),headers=header).text
    r=eval(r)
    r=r['result']['data']['data']
    for name in r:
        urlin=str(name['symbol'])
        r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
        r=eval(r)
        if str(r['Result']) !='[]':
            stock.append(urlin)

# jkl=[]
# for gl in stock:
#     if gl[-1]=='u':
#         asd=gl[:-1]
#         r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+asd+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
#         r=eval(r)
#         if str(r['Result']) =='[]':
#             jkl.append(gl)
#     else:
#         jkl.append(gl)
# stock=jkl
print(stock)

urlin=stock[0]
r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
r=eval(r)
p=(float(r['Result']['priceinfo'][-1]['price']))


mo=25000


time_tuple = time.localtime(time.time())
timedata='d'+str(time_tuple[0])+str(time_tuple[1])+str(time_tuple[2])
tradingtime=str(time_tuple[3])+str(time_tuple[4])

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
    (tradingtime,stock[0],p, 'sell',str(mo))
]
with conn.cursor() as cursor:
    cursor.executemany(insert_query, data)

cursor = conn.cursor()
# 执行查询语句
query = "show tables;"
cursor.execute(query)
# 获取查询结果
results = cursor.fetchall()
# 遍历结果并打印成交额
# for result in results:
#     turnover = result[1]
#     print(turnover)
print(results)
cursor.close()

conn.commit()
conn.close()
print('running successfully')
