import requests
import json

baseUrl ='http://127.0.0.1:6800/'
daemUrl ='http://127.0.0.1:6800/daemonstatus.json'
listproUrl ='http://127.0.0.1:6800/listprojects.json'

schUrl = baseUrl + 'schedule.json'
dictdata ={ "project":'default',"spider":'spiders_5fc'}
# r= requests.post(schUrl, json= dictdata)
# print ('5.1.delversion : [%s]\n\n'  %r.text)
r = requests.post(schUrl,json=dictdata)
print(r.text)