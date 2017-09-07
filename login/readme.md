## 基于scrapy的模拟登陆
<br>
1. 重写 start_requests方法，
```python
    def start_requests(self):
        return [Request('https://accounts.douban.com/login',meta={'cookiejar':1},callback=self.login)]
```
<br>
2. 回调到login函数实现登陆。
- 获取验证码<br>
`capt = response.xpath('//div[@class="item item-captcha"]/div/img/@src').extract_first()`
- 手动输入并传入参数
`captcha = input('请手动输入captcha:\n')
            data = {
                'source': 'None',
                'redir': 'https://www.douban.com',
                'form_email': '408737515@qq.com',
                'form_password': 'chao123456789..',
                'remember': 'on',
                'login': '登录',
                'captcha-solution': captcha,
                'captcha-id': capt_id
                `
- 如简单的验证码可tesseract 识别自动登陆：
[方法链接](https://github.com/xhongc/pythonCrawl/blob/master/tesseract.py)
<br>
3. Formrequest 返回表单信息
`return [Request(self.start_urls,
                       meta={'cookiejar':response.meta['cookiejar']},
                       callback=self.parse
                       )]`
4. 测试成功返回登入后信息。 
