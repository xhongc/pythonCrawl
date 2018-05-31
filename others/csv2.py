import csv
from pprint import pprint
import time


def insert_sort(array):
    for i in range(len(array)):
        for j in range(i):
            if array[i]['pay_type'] < array[j]['pay_type']:
                array.insert(j, array.pop(i))
                break
    return array


def sava_csv(array):
    headers = ['id', 'amount', 'body', 'business_id', 'code', 'create_time', 'notify_url', 'order_no', 'out_order_no'
        , 'pay_type', 'real_amount', 'status', 'up_order_no', 'user_id', 'amount_fee', 'pay_time', 'settlementd0',
               'settlementd1',
               'settlement_fee', 'settlementt0', 'settlementt1', 'remark', 'version', 'front_url', 'payer_ip',
               'code_id', 'amount_count', 'status_dict', 'status_rate', 'amount_sum6','nopay','pay_rate']
    with open(r'd:\test\test4.csv', 'a', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        # f_csv.writeheader()
        f_csv.writerows(array)


def get_all():
    with open(r'd:\test\test3.csv') as f:
        f_csv = csv.DictReader(f)
        t_dict = {}
        for row in f_csv:

            business_id = row['business_id']
            if business_id == '':
                business_id = 'null'
            # print(business_id)
            if business_id not in t_dict:

                t_dict[business_id] = []
                t_dict[business_id].append(row)
            else:

                t_dict[business_id].append(row)
    return t_dict


t_dict = get_all()
for k, v in t_dict.items():
    count6 = 0
    count = len(v)
    for row in v:
        status = row['status']
        if status == '6':
            count6 += 1
    v[-1]['status_rate'] = round(count6/count,6)

    nopay = float(v[-1]['amount_count']) - float(v[-1]['amount_sum6'])
    v[-1]['nopay'] = nopay

    pay_rate =round(float(v[-1]['amount_sum6'])/float(v[-1]['amount_count']),6)
    v[-1]['pay_rate'] = pay_rate
    sava_csv(v)

#################3
# for k, v in t_dict.items():
#     amount_sum = 0
#     li = []
#     amount_sum6 = 0
#     for row in v:
#         li.append(row)
#         status = row['status']
#         if status == '6':
#             amount = row['amount']
#             #print(amount)
#             try:
#                 amount_sum6 = amount_sum6 + int(amount)
#             except:
#                 amount_sum6 = amount_sum6 + float(amount)
#
#
#     li[-1]['amount_sum6'] = amount_sum6
#     # print(li[-1])
#     sava_csv(li)
############
# for k, v in t_dict.items():
#     # print(v)
#     li = []
#     amount_sum = 0
#     status_sum = 0
#     status_dict = {}
#     # print(k,v)
#     for row in v:
#         amount = row['amount']
#         status = row['status']
#         # print(business_id)
#
#         # 总计
#         try:
#             amount_sum = amount_sum + int(amount)
#         except:
#             amount_sum = amount_sum + float(amount)
#         # status
#         status_sum = status_sum + int(status)
#         # status 数
#         if status not in status_dict:
#             status_dict[status] = 1
#         else:
#             status_dict[status] += 1
#         # print('add',status)
#         li.append(row)
#         # print(li)
#     array = insert_sort(li)
#     try:
#         array[-1]['amount_count'] = amount_sum
#     except:
#         pass
#     try:
#         array[-1]['status_dict'] = status_dict
#     except:
#         pass
#     for each in array:
#         each['status_rate'] = round(int(each['status']) / status_sum, 2)
#     # print('add',row['id'])
#     print('save>>>%s'%row['business_id'])
#     sava_csv(array)
