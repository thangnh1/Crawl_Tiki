import random
import time
import urllib
import pymongo
from bs4 import BeautifulSoup
import requests
import json
import re
import os

from config import host, db_name, collection

headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
page = 'https://tiki.vn/'
res = requests.get(page, headers=headers)
src = res.text
soup = BeautifulSoup(src, 'html.parser')

categories = []
for i in range(len(soup.find_all('a', class_='styles__StyledItem-sc-oho8ay-0'))):
    link = soup.find_all('a', class_='styles__StyledItem-sc-oho8ay-0')[i].attrs['href']
    categories.append(link)

id_product = []
for p in categories:
    num = 1
    while (True):
        print('Process {} page {}'.format(p, num))
        page = 'https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&trackity_id=9f0706eb-cddc-44cf-3333-67df659d9c40&category={}&page={}'.format(re.sub(r'\D','',p), num)
        result = requests.get(page, headers=headers).text
        if (json.loads(result).get('data')==None or json.loads(result).get('data')==[]) :
            break
        for item in json.loads(result).get('data'):
            if item.get('id') not in id_product:
                id_product.append(item.get('id'))
            else:
                continue
        time.sleep(random.randrange(1, 2))
        num += 1

myclient = pymongo.MongoClient(host)
mydb = myclient[db_name]
mycol = mydb[collection]

data = []
data_err = []

for img in id_product:
    print('Process {}'.format(img))
    api = 'https://tiki.vn/api/v2/products/{}'.format(img)
    try:
        res = urllib.request.urlopen(api)
    except:
        continue
    soup = BeautifulSoup(res.read(), 'html.parser')
    data.append(json.loads(soup.text))
    mycol.insert_one(json.loads(soup.text))
    n_image = 0
    os.makedirs(os.path.join('images', str(img)))
    for n in range(len(json.loads(soup.text).get('images'))):
        urllib.request.urlretrieve(json.loads(soup.text).get('images')[n_image].get('base_url'),
                                   os.path.join('images', str(img), str(img) + '_' + str(n_image) + '.jpg'))
        n_image += 1
    time.sleep(random.randrange(0, 3))

jsonString = json.dumps(data, ensure_ascii=False)
with open("data.json", "w", encoding='utf-8') as outfile:
    outfile.write(jsonString)

mycol.create_index('short_description')