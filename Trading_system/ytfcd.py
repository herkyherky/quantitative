import pymysql
import time,pyhttpx
time_tuple = time.localtime(time.time())
date=str(time_tuple[0])+str(time_tuple[1])+str(time_tuple[2])
timedata='d'+date
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



urlin='vfs'




conn = pymysql.connect(
    host='localhost',
    user='root',
    password='kali',
    database='tradingdoce')
create_table_query = '''
CREATE TABLE IF NOT EXISTS '''+timedata+''' (
    id INT PRIMARY KEY AUTO_INCREMENT,
    start_time TIME,
    end_time TIME,
    name VARCHAR(255),
    price DECIMAL(10, 2),
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
    database='tradinghold')

create_table_query = '''
CREATE TABLE IF NOT EXISTS hold (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    price DECIMAL(10, 2),
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



def check(time,name,typ):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kali',
        database='tradingdoce')
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
        database='tradinghold')
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
        database='tradingdoce')

    cursor = conn.cursor()
    query = "select * from "+date+" where name='"+name+"';"
    cursor.execute(query)
    results = cursor.fetchall()
    volume=float(results[0][-1])+volume
    num=int(results[0][-2])+int(num)
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
        database='tradinghold')
    
    cursor = conn.cursor()
    query = "select * from hold where name='total';"
    cursor.execute(query)
    results = cursor.fetchall()
    total=float(results[0][-1])
    sql= "UPDATE hold SET volume = %s WHERE name ='total';"
    cursor.execute(sql, (total-volume))
    total=total-volume

    query = "select * from hold where name ='"+name+"';"
    cursor.execute(query)
    results = cursor.fetchall()
    volume=float(results[0][-1])+volume
    num=int(results[0][-2])+int(num)
    
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
        sql="delete from hold where id =2;"
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


def unhold(name,typ,timedata,tradingtime):
    
    total=0
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='kali',
        database='tradinghold')
    cursor = conn.cursor()
    query = "select * from hold where name='"+name+"';"
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
                time.sleep(5)
        time.sleep(2)
        a=int(r['Result']['detailinfos'][-1]['time'])

unhold(urlin,'buy',timedata,tradingtime)