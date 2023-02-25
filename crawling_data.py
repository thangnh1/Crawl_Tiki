# import pandas as pd
import random
import time
import pymongo
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import json
import re
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
            id_product.append(item.get('id'))
        time.sleep(random.randrange(1, 2))
        # for n_item in range (len(soup.find_all('a', class_='product-item'))):
        #     print('Product {}'.format(n_item))
        #     id = soup.find_all('a', class_='product-item')[n_item].attrs['data-view-content']
        #     e = json.loads(id)
        #     id_product.append(e.get('click_data').get('id'))
        num += 1

myclient = pymongo.MongoClient(host)
mydb = myclient[db_name]
mycol = mydb[collection]

data = []
data_err = []

for img in id_product:
    print('Add {} to db'.format(img))
    api = 'https://tiki.vn/api/v2/products/{}'.format(img)
    try:
        res = urlopen(api)
    except:
        continue
    soup = BeautifulSoup(res.read(), 'html.parser')
    data.append(json.loads(soup.text))
    mycol.insert_one(json.loads(soup.text))
    time.sleep(random.randrange(0, 3))

jsonString = json.dumps(data, ensure_ascii=False)
with open("data.json", "w", encoding='utf-8') as outfile:
    outfile.write(jsonString)

mycol.create_index('short_description')

# https://tiki.vn/do-choi-me-be/c2549
# https://tiki.vn/tikingon/ngon/c44792
# https://tiki.vn/dien-thoai-may-tinh-bang/c1789
# https://tiki.vn/lam-dep-suc-khoe/c1520
# https://tiki.vn/dien-gia-dung/c1882
# https://tiki.vn/thoi-trang-nu/c931
# https://tiki.vn/thoi-trang-nam/c915
# https://tiki.vn/giay-dep-nu/c1703
# https://tiki.vn/tui-vi-nu/c976
# https://tiki.vn/giay-dep-nam/c1686
# https://tiki.vn/tui-thoi-trang-nam/c27616
# https://tiki.vn/balo-va-vali/c6000
# https://tiki.vn/phu-kien-thoi-trang/c27498
# https://tiki.vn/dong-ho-va-trang-suc/c8371
# https://tiki.vn/laptop-may-vi-tinh-linh-kien/c1846
# https://tiki.vn/nha-cua-doi-song/c1883
# https://tiki.vn/cross-border-hang-quoc-te/c17166
# https://tiki.vn/bach-hoa-online/c4384
# https://tiki.vn/thiet-bi-kts-phu-kien-so/c1815
# https://tiki.vn/voucher-dich-vu/c11312
# https://tiki.vn/o-to-xe-may-xe-dap/c8594
# https://tiki.vn/nha-sach-tiki/c8322
# https://tiki.vn/dien-tu-dien-lanh/c4221
# https://tiki.vn/the-thao-da-ngoai/c1975
# https://tiki.vn/may-anh/c1801
# https://tiki.vn/san-pham-tai-chinh-bao-hiem/c54042

# id = soup.find_all('a', class_='product-item')[0].attrs['data-view-content']
# e = json.loads(id)
# e.get('click_data').get('id')

# with open("data.json", "w", encoding='utf-8') as outfile:
#     outfile.write(jsonString)

# f = open("data.json", "r", encoding='utf-8')
# print(f.read())

# jsonString = json.dumps(data_err, ensure_ascii=False)