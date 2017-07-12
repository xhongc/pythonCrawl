'''将爬取的表格存为csv文件'''
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://en.wikipedia.org/wiki/Comparison_of_text_editors')
bs = BeautifulSoup(html,'html.parser')
table = bs.findAll('table',{'class':'wikitable'})[0]
rows = table.findAll('tr')

with open('table.csv','wt',newline='',encoding='utf-8') as d:
    writer = csv.writer(d)

    for row in rows:
        csvrows=[]
    
        
        for cell in row.findAll(['td','th']):
                
            csvrows.append(cell.get_text())
        writer.writerow(csvrows)
        
            
    
