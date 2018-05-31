# import csv
#
#
# def insert_sort(array):
#     for i in range(len(array)):
#         for j in range(i):
#             if array[i]['pay_type'] < array[j]['pay_type']:
#                 array.insert(j, array.pop(i))
#                 break
#     return array
#
#
# def sava_csv(array):
#     headers = ['id', 'amount', 'body', 'business_id', 'code', 'create_time', 'notify_url', 'order_no', 'out_order_no'
#         , 'pay_type', 'real_amount', 'status', 'up_order_no', 'user_id', 'amount_fee', 'pay_time', 'settlementd0',
#                'settlementd1',
#                'settlement_fee', 'settlementt0', 'settlementt1', 'remark', 'version', 'front_url', 'payer_ip',
#                'code_id', 'amount_count', 'status_dict', 'status_rate']
#     with open(r'd:\test\test2.csv', 'w', newline='') as f:
#         f_csv = csv.DictWriter(f, headers)
#         f_csv.writeheader()
#         f_csv.writerows(array)
#
#
# with open(r'd:\test\test.csv') as f:
#     f_csv = csv.DictReader(f)
#
#     for i in range(1, 3):
#         li = []
#         amount_sum = 0
#         status_sum = 0
#         status_dict = {}
#         for row in f_csv:
#             business_id = row['business_id']
#             try:
#                 if business_id != str(i):
#                     continue
#             except BaseException as e:
#                 print('1',e)
#
#             amount = row['amount']
#             status = row['status']
#             # print(business_id)
#
#             # 总计
#             amount_sum = amount_sum + int(amount)
#             # status
#             status_sum = status_sum + int(status)
#             # status 数
#             if status not in status_dict:
#                 status_dict[status] = 1
#             else:
#                 status_dict[status] += 1
#             li.append(row)
#         print(li)
#         array = insert_sort(li)
#         try:
#             array[-1]['amount_count'] = amount_sum
#         except:
#             pass
#         try:
#             array[-1]['status_dict'] = status_dict
#         except:
#             pass
#         for each in array:
#             each['status_rate'] = round(int(each['status']) / status_sum, 2)
#
#         sava_csv(array)
print(float('0.1'))