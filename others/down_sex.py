import requests
from scrapy.selector import Selector
import time
import random
def get_video_html(page):
    try:
        url = 'http://www.sexx2020.com/'
        header={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }

        data ={
            'mode': 'async',
            'function': 'get_block',
            'block_id': 'list_videos_most_recent_videos',
            'sort_by': 'post_date',
            'from': page
        }
        html = requests.post(url,headers=header)
        selector = Selector(html)

        sex_item = selector.xpath("//div[@class='margin-fix']/div/a/@href").extract()
        return sex_item
    except:
        print('sleep3s')
        time.sleep(3)
        get_video_html(page)
    # print(sex_item)
def save_txt(each):
    with open('video.txt','a') as f:
        f.write(each)
        f.write('\n')

def main():
    for page in range(1,10):
        print('loading page%s'%page)
        lists = get_video_html(page)
        for each in lists:
            save_txt(each)

        time.sleep(random.uniform(0.3,1.2))

main()