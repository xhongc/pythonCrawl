# coding=utf-8
'''
@author: 'wang'
'''

import os
import csv
import codecs
import sys
sys.path.insert(0, '..')

from api_call.flower_api.flower_api import FlowerApi  
from api_call.ar_api.v01.ar_api import ARControl
import json
from cof.rand import CoRand

reload(sys)
sys.setdefaultencoding('utf8')

for i in range(10):
    ar_con = ARControl()
    ar_con.connect_server()
    user_id = CoRand.get_rand_int()
    ar_con.login(user_id, "im")
    
    flower_web = FlowerApi()
    filepath = "D:\workspace\ARScoketTest\FlowerResource"
    pathDir =  os.listdir(filepath)
    result_list = []
    
    for jpg in pathDir:
        flower_url = "http://file1.ffpic.com/f/" + jpg
        web_data =  flower_web.get_flower(flower_url)
        socket_res = ar_con.match_flower(flower_url)
        socket_data = res_data = json.loads(socket_res)
    
        row = []
        row.append(jpg)
        if web_data["flower"]:
            for scores in web_data["results"]:            
                row.append(web_data["flower"])
                row.append(scores["class"])
                row.append(scores["score"])
        else:
            row.append(web_data["flower"])
            row.append(" ")
            row.append(" ")
        if socket_data.has_key("name"):
            row.append("True")
            row.append(socket_data["name"])
        else:
            row.append("False")
        
        result_list.append(row)
    
    print result_list
    ar_con.close()
    
    with open('result' + str(i) + '.csv', 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        spamwriter = csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(["jpg_name", "web_result", "web_name", "Rate", "socket_result", "socket_name"])
        for result in result_list:        
            spamwriter.writerow(result)