import requests as re
import pyhttpx,time
import pymysql
import random


url='https://quotes.sina.cn/hq/api/openapi.php/US_CategoryV2Service.getList?sort=percent&asc=0&page='
header={'User-Agent': 'Mozilla/5.0 (Windows NT +10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
session = pyhttpx.HttpSession()
stock=[]
page=0
ratio=1


user = 'test'

while len(stock)<3 and ratio==1:
    page+=1
    r=re.get(url+str(page),headers=header).text
    r=eval(r)
    r=r['result']['data']['data']
    for name in r:
        urlin=str(name['symbol'])
        u = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
        u=eval(u)
        if str(u['Result']) !='[]':
            if float(u['Result']['priceinfo'][-1]['ratio'][1:-1])<=80:
                stock.append(urlin)
                ratio=0
                break
            elif float(u['Result']['priceinfo'][-1]['ratio'][1:-1])>=80:
                stock.append(urlin)


jkl=[]
for gl in stock:
    if gl[-1]=='u':
        asd=gl[:-1]
        r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+asd+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
        r=eval(r)
        if str(r['Result']) =='[]':
            jkl.append(gl)
    else:
        jkl.append(gl)

stock=jkl
print(stock)

urlin=stock[0]
r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
r=eval(r)
p=(float(r['Result']['priceinfo'][-1]['price']))



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
    database=user+'_tradingdoce')
create_table_query = '''
CREATE TABLE IF NOT EXISTS '''+timedata+''' (
    id INT PRIMARY KEY AUTO_INCREMENT,
    start_time TIME,
    end_time TIME,
    name VARCHAR(255),
    price DECIMAL(10, 3),
    transaction_type ENUM('buy', 'sell'),
    num MEDIUMINT (12),
    volume DECIMAL(12, 2)
)
'''
with conn.cursor() as cursor:
    cursor.execute(create_table_query)
cursor.close()
conn.commit()
conn.close()

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='kali',
    database=user+'_tradinghold')

create_table_query = '''
CREATE TABLE IF NOT EXISTS hold (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    price DECIMAL(10, 3),
    transaction_type ENUM('buy', 'sell'),
    num MEDIUMINT (12),
    volume DECIMAL(12, 2)
)
'''
with conn.cursor() as cursor:
    cursor.execute(create_table_query)
    

cursor = conn.cursor()
search = "select * from hold where name ='total';"
cursor.execute(search)
results = cursor.fetchall()
if str(results)=='()':
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    insert_query = 'INSERT INTO hold (name,volume) VALUES (%s, %s)'
    data = [('total', '3000')]
    with conn.cursor() as cursor:
        cursor.executemany(insert_query, data)
cursor.close()
conn.commit()
conn.close()



def check(typ,time,name):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kali',
        database=user+'_tradingdoce')
    cursor = conn.cursor()
    search = "select * from "+timedata+" where name ='"+name+"';"
    cursor.execute(search)
    results = cursor.fetchall()
    if str(results)=='()':
        insert_query = 'INSERT INTO '+timedata+' (start_time,end_time, name, price, transaction_type, num, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        data = [(time,'', name, '0', typ, '0', '0')]
        with conn.cursor() as cursor:
            cursor.executemany(insert_query, data)

    cursor.close()
    conn.commit()
    conn.close()
    
    
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kali',
        database=user+'_tradinghold')
    cursor = conn.cursor()
    search = "select * from hold where name ='"+name+"';"
    cursor.execute(search)
    results = cursor.fetchall()
    if str(results)=='()':
        insert_query = 'INSERT INTO hold (name, price, transaction_type, num, volume) VALUES (%s, %s, %s, %s, %s)'
        data = [(name, '0', typ, '0', '0')]
        with conn.cursor() as cursor:
            cursor.executemany(insert_query, data)
        
    cursor.close()
    conn.commit()
    conn.close()



def acc(time,date, name, price, typ, num, volume):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kali',
        database=user+'_tradingdoce')
    cursor = conn.cursor()
    search = "select * from "+timedata+" where name ='"+name+"';"
    cursor.execute(search)
    results = cursor.fetchall()
    volume=float(results[0][-1])+volume
    num=int(results[0][-2])+int(num)
    price=volume/num
    print(volume,num,price)
    sql = "UPDATE "+date+" SET end_time=%s,price = %s,num= %s,volume = %s WHERE name ='"+name+"';"
    cursor.execute(sql, (time,str(price),num ,str(volume)))

    cursor.close()
    conn.commit()
    conn.close()
    

def hold(name,price,num,volume,typ):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kali',
        database=user+'_tradinghold')
    
    cursor = conn.cursor()
    query = "select * from hold where name='total';"
    cursor.execute(query)
    results = cursor.fetchall()
    total=float(results[0][-1])
    sql= "UPDATE hold SET volume = %s WHERE name ='total';"
    cursor.execute(sql, (total-volume))
    total=total-volume

    query = "select * from hold where name ='"+str(name)+"';"
    cursor.execute(query)
    results = cursor.fetchall()
    volume=float(results[0][-1])+volume
    num=int(results[0][-2])+int(num)
    if int(num)!=0:
        price=volume/num
    sql = "UPDATE hold SET price = %s,num= %s,volume = %s WHERE name ='"+name+"';"
    cursor.execute(sql, (price,num ,volume))
    print(num)
    if int(num)==0:
        query = "select * from hold where name ='"+name+"';"
        cursor.execute(query)
        results = cursor.fetchall()
        volume=float(results[0][-1])
        print(volume,num)
        sql="delete from hold where name ='"+name+"';"
        cursor.execute(sql)
        sql = "UPDATE hold SET volume = %s WHERE name ='total';"
        if typ=='buy':
            cursor.execute(sql, (volume+total))
            print(volume+total)
        elif typ=='sell':
            cursor.execute(sql, (volume-total))
    cursor.close()
    conn.commit()
    conn.close()


def trading(name,typ,timedata,tradingtime):
    check(typ,tradingtime,name)
    total=0
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kali',
        database=user+'_tradinghold')
    cursor = conn.cursor()
    search = "select * from hold;"
    cursor.execute(search)
    results = cursor.fetchall()
    for result in results:
        total+=float(result[-1])
    v_updata1 = int(total/2)

    cursor.close()
    conn.commit()
    conn.close()
    
    r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
    r=eval(r)
    vol=1
    a=int(r['Result']['detailinfos'][-1]['time'])
    print(a)
    time.sleep(2)
    while vol==1:
        r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
        r=eval(r)
        for rar in r['Result']['detailinfos']:
            if a<int(rar['time']):
                if vol==2:
                    break
                p=rar['price']
                n=rar['volume']
                v=float(int(n)*float(p))
                if v_updata1 >= v:
                    v_updata1=v_updata1-v
                    acc(tradingtime,timedata,name,p,typ,n,v)
                    hold(name,p,n,v,typ)
                elif v_updata1 < v:
                    v=v_updata1
                    up_v=v%float(p)
                    v-=up_v
                    n=v/float(p)
                    v=float(int(n)*float(p))
                    vol=2
                    acc(tradingtime,timedata,name,p,typ,n,v)
                    hold(name,p,n,v,typ)
                    break
                
        time.sleep(2)
        a=int(r['Result']['detailinfos'][-1]['time'])
        
        






def unhold(name,typ,timedata,tradingtime):
    
    total=0
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kali',
        database=user+'_tradinghold')
    cursor = conn.cursor()
    query = "select * from hold where name ='"+name+"';"
    cursor.execute(query)
    results = cursor.fetchall()
    n1=results[0][-2]
    print(n1)
    cursor.close()
    conn.commit()
    conn.close()


    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",}
    session = pyhttpx.HttpSession()
    r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=headers).text
    r=eval(r)
    vol=1

    a=int(r['Result']['detailinfos'][-1]['time'])
    time.sleep(2)
    while vol==1:
        r = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=headers).text
        r=eval(r)
        for rar in r['Result']['detailinfos']:
            if a<int(rar['time']):
                p=rar['price']
                n=int(rar['volume'])
                v=float(int(n)*float(p))
                if n1 > n:
                    n1-=n
                    acc(tradingtime,timedata,urlin,p,typ,n,v)
                    hold(name,p,-n,-v,typ)
                elif n1 <= n:
                    n=n1
                    v=float(int(n)*float(p))
                    vol=2
                    acc(tradingtime,timedata,urlin,p,typ,n,v)
                    hold(name,p,-n,-v,typ)
                    break

        time.sleep(2)
        a=int(r['Result']['detailinfos'][-1]['time'])

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='kali',
    database=user+'_tradinghold')
cursor = conn.cursor()
query = "select * from hold;"
cursor.execute(query)
results = cursor.fetchall()
cursor.close()
conn.commit()
conn.close()
if len(results)>1:
    n1=results[1][1]
    print(n1)
    
    unhold(n1,'buy',timedata,tradingtime)

trading(urlin,'sell',timedata,tradingtime)
# unhold(urlin,'buy',timedata,tradingtime)

print('running successfully')

