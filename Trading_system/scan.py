import pymysql
import time
import os

def scan():
    os.system('I:')
    os.system("cd I:\project\trading system")
    os.system('start main.bat')
    os.system('start down.bat')

time_tuple = time.localtime(time.time())
timedata='d'+str(time_tuple[0])+str(time_tuple[1])+str(time_tuple[2])
tradingtime=int(time_tuple[3])*100+int(time_tuple[4])


# coon = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='kali',
#     database='tradingdoce')
# cursor = coon.cursor()
# query = "show tables"
# cursor.execute(query)
# results = cursor.fetchall()
# print(tradingtime)
# while True:
#     if tradingtime >=2131:
#         if results[-1][0]!=timedata:
#             scan()
#         while True:
#             if tradingtime >=2151:
#                 query = "SELECT * FROM "+str(timedata)
#                 cursor.execute(query)
#                 results = cursor.fetchall()
#                 for result in results:
#                     turnover = result[1]
#                     print(turnover)
#                     if result[1]!=tradingtime-1:
#                         scan()
#                     while True:
#                         if tradingtime >=1121:
#                             query = "SELECT * FROM "+str(timedata)
#                             cursor.execute(query)
#                             results = cursor.fetchall()
#                             for result in results:
#                                 turnover = result[1]
#                                 print(turnover)
#                                 if result[1]!=tradingtime-1:
#                                     scan()

while True:
    time_tuple = time.localtime(time.time())
    tradingtime=int(time_tuple[3])*100+int(time_tuple[4])
    print(tradingtime)
    if tradingtime >=1031:
        scan()
        while True:
                time_tuple = time.localtime(time.time())
                tradingtime=int(time_tuple[3])*100+int(time_tuple[4])
                if tradingtime >=1033:
                    os.system('shutdown -s -t 300')
        time.sleep(60)

#                         time.sleep(10)
#             time.sleep(10)
    time.sleep(10)
                            
# cursor.close()
# coon.close()