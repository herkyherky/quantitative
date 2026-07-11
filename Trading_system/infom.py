import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = 'https://finance.yahoo.com/gainers'
response = requests.get(url, headers=headers)
html = response.text

tree = etree.HTML(html)

for i in range(1,11):
    data_name = tree.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr['+str(i)+']/td[1]//text()')
    data_price = tree.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr['+str(i)+']/td[3]/fin-streamer//text()')
    data_increase = tree.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr['+str(i)+']/td[5]/fin-streamer/span//text()')
    data_volume = tree.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr['+str(i)+']/td[6]/fin-streamer//text()')
    print(data_name[0],data_increase,data_price,data_volume)
