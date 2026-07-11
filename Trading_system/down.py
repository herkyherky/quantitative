import time
import os,pyhttpx
import requests as re

time_tuple = time.localtime(time.time())
timedata=str(time_tuple[1])



path='./data/'+str(time_tuple[0])
if not os.path.exists(path):
    os.mkdir(path)






url='https://quotes.sina.cn/hq/api/openapi.php/US_CategoryV2Service.getList?sort=percent&asc=0&page='
header={'User-Agent': 'Mozilla/5.0 (Windows NT +10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
session = pyhttpx.HttpSession()
stock=[]
page=0



while len(stock)<4:
    page+=1
    r=re.get(url+str(page),headers=header).text
    r=eval(r)
    r=r['result']['data']['data']
    for name in r:
        urlin=str(name['symbol'])
        u = session.get(url='https://finance.pae.baidu.com/selfselect/getstockquotation?all=1&isIndex=false&isBk=false&isBlock=false&isStock=true&isFutures=false&isForeign=false&code='+urlin+'&stockType=us&newFormat=1&group=quotation_minute_us&finClientType=pc',headers=header).text
        u=eval(u)
        if str(u['Result']) !='[]':
            
            stock.append(urlin)
            if len(stock)>3:
                break

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

file = open('./data/'+str(time_tuple[0])+'/'+timedata+'.txt','a+')
file.write(str(time_tuple[2])+':')

for a in stock:
    

    
    file.write(str(a)+'  ')
file.write('''

''')
file.close()

