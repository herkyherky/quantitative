import requests as re
from lxml import etree

header={
'User-Agent': 'Mozilla/5.0 (Windows NT +10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
'Cookie' : '__bid_n=18698508f045b24b254207; FPTOKEN=zLdW3pqVRX/7cWpctTLNdiPh0jFEHJUeRTr6iJ3Y4h652HhPtF7EJk87f4NuKYxGBVceTWieg+OT5I/cEd2nza0n5aVw2Eh4bm1T6vbY+QWk6cz2ldQhd4v3GbbXF8U7ojLzS1kr4WoNXz/9K0LAHM+hkG4Me3sqE0klDNITTMYOQ6BuOTy3F2YUZSTpWd04pP27nhirUOUOkK42dUT+DA2s883HJe+Cgqg86aTbVRnoxQLjqJxuyAlBJLAbG9aFIw2DozvRKLGzjr36fhNs6sX5u1Plgr91yP2zzU1NkSFAwqJ5vJNN3G00VwoVbAH42RjcOay9fP4ak/0wl93d3Wy6cfRpEPeHE86QmIGA4RsGzKHTKIb0lrvnMGwsOPR2BqWyWK7hGgom+NBYw1+HCA==|aPkoHn+hVvHjCt438ESU6cIcsdWfkxwa0OECjWYaVRY=|10|a9e1a998ebf35fdd4dbdc22d9d9e1f4e; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1689424197; user=MDptb182MzI5OTI2NjY6Ok5vbmU6NTAwOjY0Mjk5MjY2Njo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNDo6OjYzMjk5MjY2NjoxNjg5NDI2MTUyOjo6MTY1MjE4NjgyMDo2MDQ4MDA6MDoxNzFkZDBmZWQ0ZjE3ZmQ5MDFkNjYxYTAzYjUzYTVmZjE6ZGVmYXVsdF80OjE%3D; userid=632992666; u_name=mo_632992666; escapename=mo_632992666; ticket=0cfef2eeb2e9789f9cb46e85fc5a760a; user_status=0; utk=3a87665dd0a8d3d4b2842cd332ea1cba; historystock=FREQ%7C*%7CEDTX; v=A2p14cy8-pAvFnZ8ZXacnml9u9sJ2-414F9i2fQjFr1IJwRF3Gs-RbDvsuzH'}

r=re.get('http://q.10jqka.com.cn/usa/detailDefer',headers=header).text
html = etree.HTML(r)
for a in range(1,4):
    
    data_name = html.xpath('//*[@id="maincont"]/table/tbody/tr['+str(a)+']/td[2]/a/text()')
    data_increase = html.xpath('//*[@id="maincont"]/table/tbody/tr['+str(a)+']/td[5]/text()')
    data_price = html.xpath('//*[@id="maincont"]/table/tbody/tr['+str(a)+']/td[6]/text()')
    data_volume = html.xpath('//*[@id="maincont"]/table/tbody/tr['+str(a)+']/td[8]/text()')
    print(data_name,data_increase,data_price,data_volume)
