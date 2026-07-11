import pymysql
import time,pyhttpx
def hold(name,price, typ, num, volume):
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
    else:
        query = "select * from hold where name='total';"
        cursor.execute(query)
        results = cursor.fetchall()
        total=float(results[0][-1])
        updata = int(total//3)
        sql = "UPDATE hold SET volume = %s WHERE name ='total';"
        cursor.execute(sql, (total-updata))
    


        
    cursor = conn.cursor()
    query = "select * from hold where name ='"+name+"';"
    cursor.execute(query)
    results = cursor.fetchall()
    if str(results)=='()':
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
        insert_query = 'INSERT INTO hold (name, price, transaction_type, num, volume) VALUES (%s, %s, %s, %s, %s)'
        data = [(name, price, typ, num, volume)]
        with conn.cursor() as cursor:
            cursor.executemany(insert_query, data)

    else:

        sql = "UPDATE hold SET price = %s, volume = %s WHERE name ='"+name+"';"
        cursor.execute(sql, (price, volume))
    cursor.close()
    conn.commit()
    conn.close()
    
        
        
        
hold('ttoo','11.2','sell','100','1000')