## 多线程抓取今日头条图片
<br />


> AJAX即“Asynchronous Javascript And XML”（异步JavaScript和XML），是指一种创建交互式网页应用的网页开发技术。
> AJAX 是一种用于创建快速动态网页的技术。 
> 通过在后台与服务器进行少量数据交换，AJAX 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。 
> 传统的网页（不使用 AJAX）如果需要更新内容，必须重载整个网页页面（html页面）。


<br />
1. 分析今日头条ajax 网页
我们查看网页审查，分析Ajax加载的秘密。 
首先动态加载肯定不是Doc目录下的，所以应该在XHR下查找。 
![](http://img.blog.csdn.net/20170620072635684?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvZ3g4NjQxMDIyNTI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
2. 分析街头美拍详细页面的网页组成
3. 分析索引页内容
4. 下载图片及保存数据库
5. 开启循环和多进程
