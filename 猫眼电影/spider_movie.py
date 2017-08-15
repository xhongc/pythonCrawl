import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        responese = requests.get(url)
        if responese.status_code ==200:
            return responese.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>.*?<img data-src="(.*?)".*?alt="(.*?)".*?<p class="star">(.*?)</p>'
                         +'.*?class="releasetime">(.*?)</p>.*?<p class="score"><i class="integer">(.*?)</i>'
                         +'<i class="fraction">(.*?)</i></p>',re.S)
    result = re.findall(pattern,html)
    for item in result:
        yield {
            'index':item[0],
            'image':item[1],
            'titile':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4][5:],
            'score':item[5]+item[6]
        }

def write_to_file(content):
    with open ('result.json','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
def main(offset):
    url =  'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    groups = [x*10 for x in range(0,11)]
    pool =Pool(4)
    pool.map(main,groups)