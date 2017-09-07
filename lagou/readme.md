## ladou_spider
&nbsp;
*使用scrapy、redis、mysq l实现的一个分布式网络爬虫,底层存储MySQL数据库,分布式使用redis实现。*
&nbsp;
- 分布式使用redis实现，redis中存储了工程的request，stats信息，能够对各个机器上的爬虫实现集中管理，这样可以 解决爬虫的性能瓶颈，利用redis的高效和易于扩展能够轻松实现高效率下载：当redis存储或者访问速度遇到瓶颈时，可以 通过增大redis集群数和爬虫集群数量改善。
- MySQL存储，将拉勾网Python相关的职位信息存入数据库。爬取内容包括职位信息、薪酬、公司名称、公司地点、发布时间等
- 反爬虫策略：
+创建cookie.py 实现模拟登录，并保存cookie，实现在download middleware 加载cookie 
+实现了一个download middleware，不停的变user-aget

- 调试策略的实现：
将系统log信息写到文件中

- 文件，信息存储
实现了FilePipeline可以将指定扩展名的文件下载到本地，保存为json或csv格式。
实现了Pipeline连接 mysql 保存数据库。

- 访问速度动态控制:
跟据网络延迟，分析出scrapy服务器和网站的响应速度，动态改变网站下载延迟

###运行redis
&nbsp;
- 想要加载自己的配置需要打开一个cmd窗口 使用cd命令切换目录到 D:\redis 运行 redis-server.exe redis.windows.conf 。
- 记得每一次运行程序时要记得清空redis缓存，不然爬虫不会进行
redis-cli flushdb
- 再另启一个cmd窗口，原来的不要关闭，不然就无法访问服务端了。
切换到redis目录下运行 redis-cli.exe -h 127.0.0.1 -p 6379 

&nbsp;
### scrapy-redis 配置
> settings.py配置redis（在scrapy-redis 自带的例子中已经配置好）
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
REDIS_URL = None							 # 一般情况可以省去
REDIS_HOST = '127.0.0.1' 				# 也可以根据情况改成 localhost
REDIS_PORT = 6379
spider 继承RedisSpider
class tempSpider(RedisSpider)  
name = "temp"
redis_key  = ''temp:start_url"


###Scrapy-Redis 全部配置
```
#启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
 
#确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
 
#默认请求序列化使用的是pickle 但是我们可以更改为其他类似的。PS：这玩意儿2.X的可以用。3.X的不能用
#SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"
 
#不清除Redis队列、这样可以暂停/恢复 爬取
#SCHEDULER_PERSIST = True
 
#使用优先级调度请求队列 （默认使用）
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
#可选用的其它队列
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'
 
#最大空闲时间防止分布式爬虫因为等待而关闭
#SCHEDULER_IDLE_BEFORE_CLOSE = 10
 
#将清除的项目在redis进行处理
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}
 
#序列化项目管道作为redis Key存储
#REDIS_ITEMS_KEY = '%(spider)s:items'
 
#默认使用ScrapyJSONEncoder进行项目序列化
#You can use any importable path to a callable object.
#REDIS_ITEMS_SERIALIZER = 'json.dumps'
 
#指定连接到redis时使用的端口和地址（可选）
#REDIS_HOST = 'localhost'
#REDIS_PORT = 6379
 
#指定用于连接redis的URL（可选）
#如果设置此项，则此项优先级高于设置的REDIS_HOST 和 REDIS_PORT
#REDIS_URL = 'redis://user:pass@hostname:9001'
 
#自定义的redis参数（连接超时之类的）
#REDIS_PARAMS  = {}
 
#自定义redis客户端类
#REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient'
 
#如果为True，则使用redis的'spop'进行操作。
#如果需要避免起始网址列表出现重复，这个选项非常有用。开启此选项urls必须通过sadd添加，否则会出现类型错误。
#REDIS_START_URLS_AS_SET = False
 
#RedisSpider和RedisCrawlSpider默认 start_usls 键
#REDIS_START_URLS_KEY = '%(name)s:start_urls'
 
#设置redis使用utf-8之外的编码
#REDIS_ENCODING = 'latin1'
```