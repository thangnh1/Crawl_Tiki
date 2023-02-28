from config import host, db_name, collection
import pymongo

myclient = pymongo.MongoClient(host)
mydb = myclient[db_name]
mycol = mydb[collection]

detail_document = mycol.find({})
cate = []
cate_path = []
for document in detail_document:
    if('TikiNGON' in document['productset_group_name']):
        document['productset_group_name']=document['productset_group_name'].replace('TikiNGON', 'NGON')
    elif('TIKINGON' in document['productset_group_name']):
        document['productset_group_name']=document['productset_group_name'].replace('TIKINGON', 'NGON')
    cate.append(document['productset_group_name'].split('/'))
    cate_path.append(document['productset_group_name'])

cate_0 = []
cate_1 = []
cate_2 = []
cate_3 = []
cate_4 = []
cate_5 = []
cate_6 = []


def get_category_by_rank(list_, rank):
    for i in range(len(cate)):
        try:
            if cate[i][rank] not in list_:
                list_.append(cate[i][rank])
        except:
            continue


get_category_by_rank(cate_0,0)
get_category_by_rank(cate_1,1)
get_category_by_rank(cate_2,2)
get_category_by_rank(cate_3,3)
get_category_by_rank(cate_4,4)
get_category_by_rank(cate_5,5)
get_category_by_rank(cate_6,6)

output = []
for x in cate:
    if '/'.join(x) not in output:
        output.append('/'.join(x))

result = []
for x in cate_0:
    count = 0
    for y in cate:
        if x == y[0]:
            count+=1
    result.append(x + ' : ' + '{}'.format(count))

temp_list = []
for a in cate_0:
    for b in cate_1:
        temp = 0
        for z in cate_path:
            if a+'/'+b in z:
                temp+=1
                if a+'/'+b not in temp_list:
                    temp_list.append(a+'/'+b)
        if temp != 0:
            result.append(a+'/'+b +' : '+'{}'.format(temp))
        else:
            continue

temp_list1 = []
for a in temp_list:
    for b in cate_2:
        temp = 0
        print(a+'/'+b)
        for z in cate_path:
            if a+'/'+b in z:
                temp+=1
                if a+'/'+b not in temp_list1:
                    temp_list1.append(a+'/'+b)
            if a+'/'+b == z:
                cate_path.remove(z)
        if temp != 0:
            result.append(a+'/'+b +' : '+'{}'.format(temp))
        else:
            continue

temp_list = []
for a in temp_list1:
    for b in cate_3:
        temp = 0
        print(a+'/'+b)
        for z in cate_path:
            if a+'/'+b in z:
                temp+=1
                if a+'/'+b not in temp_list:
                    temp_list.append(a+'/'+b)
            if a+'/'+b == z:
                cate_path.remove(z)
        if temp != 0:
            result.append(a+'/'+b +' : '+'{}'.format(temp))
        else:
            continue

temp_list1 = []
for a in temp_list:
    for b in cate_4:
        temp = 0
        print(a+'/'+b)
        for z in cate_path:
            if a+'/'+b in z:
                temp+=1
                if a+'/'+b not in temp_list1:
                    temp_list1.append(a+'/'+b)
            if a+'/'+b == z:
                cate_path.remove(z)
        if temp != 0:
            result.append(a+'/'+b +' : '+'{}'.format(temp))
        else:
            continue

temp_list = []
for a in temp_list1:
    for b in cate_4:
        temp = 0
        print(a+'/'+b)
        for z in cate_path:
            if a+'/'+b in z:
                temp+=1
                if a+'/'+b not in temp_list:
                    temp_list.append(a+'/'+b)
            if a+'/'+b == z:
                cate_path.remove(z)
        if temp != 0:
            result.append(a+'/'+b +' : '+'{}'.format(temp))
        else:
            continue

temp_list1 = []
for a in temp_list:
    for b in cate_5:
        temp = 0
        print(a+'/'+b)
        for z in cate_path:
            if a+'/'+b in z:
                temp+=1
                if a+'/'+b not in temp_list1:
                    temp_list1.append(a+'/'+b)
            if a+'/'+b == z:
                cate_path.remove(z)
        if temp != 0:
            result.append(a+'/'+b +' : '+'{}'.format(temp))
        else:
            continue

temp_list = []
for a in temp_list1:
    for b in cate_6:
        temp = 0
        print(a+'/'+b)
        for z in cate_path:
            if a+'/'+b in z:
                temp+=1
                if a+'/'+b not in temp_list:
                    temp_list.append(a+'/'+b)
            if a+'/'+b == z:
                cate_path.remove(z)
        if temp != 0:
            result.append(a+'/'+b +' : '+'{}'.format(temp))
        else:
            continue

result = sorted(result)

with open('result.txt', 'w', encoding='utf-8') as f:
    for line in result:
        print(line)
        # write each item on a new line
        f.write(line+'\n')
    print('Done')