#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import os, sys
class htmldemo():
      def __init__(self,testname):
            self.testname = str(testname)
            if not os.path.isdir("./LP/html"):
                  os.mkdir("./LP/html")
            self.testnamepath = "./LP/pvo/" + self.testname
            self.reporthtml()
      def readOpeartion(self, filename):
            fl = open(filename, 'r')
            thisdata = fl.readlines()
            return thisdata

      def result(self):
            thisresult =self.readOpeartion(self.testnamepath + ".result")
            thisresult = thisresult[0].split(";")
            thisresult[5] = thisresult[5].split(".")[0]
            return thisresult

      def match(self):
            thismatch = self.readOpeartion(self.testnamepath + ".match")
            return thismatch  # 匹配详情

      def performance(self):
            thiscpudata = []
            thisMdata = []
            num = 1
            numlist = []
            thistxt = self.readOpeartion(self.testnamepath + ".txt")
            for d in thistxt:
                  thisdata = d.split(",")
                  numlist.append(num)
                  thiscpudata.append(float(thisdata[1]))
                  thisMdata.append(int(thisdata[2]))
                  num = num + 1
            return thiscpudata, thisMdata, numlist




      def reporthtml(self):
            resultflag = False
            txtflag = False
            matchflag = False
            if os.path.isfile("./LP/html/"+self.testname+".html"):
                  os.remove("./LP/html/"+self.testname+".html")
            fh = open("./LP/html/"+self.testname+".html", 'w+')
            fh.write(str(self.htmldemo()))
            fh.close()
            if os.path.isfile(self.testnamepath + ".result"):
                  resultflag = True
                  fh = open("./LP/html/"+self.testname+".html", 'a ')
                  thisresult = self.result()
                  fh.write(self.resultshow(thisresult))
                  fh.close()
                  os.remove(self.testnamepath + ".result")
            if os.path.isfile(self.testnamepath + ".txt"):
                  txtflag = True
                  fh = open("./LP/html/"+self.testname+".html", 'a ')
                  fh.write(self.performanceshow())
                  fh.close()
            if os.path.isfile(self.testnamepath + ".match"):
                  matchflag = True
                  fh = open("./LP/html/"+self.testname+".html", 'a ')
                  matchdetails = self.match()
                  fh.write(self.matchshow(matchdetails))
                  fh.close()
                  os.remove(self.testnamepath + ".match")
            if os.path.isfile(self.testnamepath + ".txt"):
                  fh = open("./LP/html/"+self.testname+".html", 'a ')
                  cpudata, Mdata, num = self.performance()
                  fh.write(self.performancedata(cpudata, Mdata, num))
                  fh.close()
                  os.remove(self.testnamepath + ".txt")
            if not resultflag and not txtflag and not matchflag:
                  fh = open("./LP/html/"+self.testname+".html", 'a ')
                  fh.write(self.testresult())
                  fh.close()
            fh = open("./LP/html/"+self.testname+".html", 'a')
            fh.write(self.htmldemoend())
            fh.close()

      def htmldemo(self):
            htmldemo = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
      <html>
          <head>
              <meta charset="utf-8">
              <style>
                  #matchresult{
                      text-align: center;
                  }
                  #match{
                      text-align: center;
                  }
                  thead{
                      font-weight: 700;
                      font-size: 32px;
                  }
                  h1{
                      text-align: center;
                      font-weight: 700;
                  }
                  h3{
                      text-align: center;
                      font-weight: 700;
                  }
                  h2{
                      font-weight: 700;
                      font-size: 32px;
                  }
                   #matchbt td{
                      font-size: 20px;

                  }
                   img{
                      max-width: 660px;
                      }
              </style>
              <script src="https://img.hcharts.cn/jquery/jquery-1.8.3.min.js"></script>
              <script src="https://img.hcharts.cn/highcharts/highcharts.js"></script>
              <script src="https://img.hcharts.cn/highcharts/modules/exporting.js"></script>
              <script src="https://img.hcharts.cn/highcharts-plugins/highcharts-zh_CN.js"></script>
          </head><body>
          <h1>''' + str(self.testname).decode("GBK")+ '''任务报告</h1>'''
            return htmldemo

      def resultshow(self, result):
            resultshow = '''
               <div id="matchresult" style="margin-bottom: 60px">
                  <h2>录屏回放测试结果</h2>
                   <table style="max-width:400px" align="center">
                       <tr>
                          <td style="min-width:150px">
                                      回放开始时间
                                </td>
                               <td style="min-width:150px">
                                      回放结束时间
                                </td>
                               <td style="min-width:120px">
                                      匹配结果
                                </td>
                               <td style="min-width:120px">
                                      匹配概率为
                                </td>
                       </tr>
                       <tr>
                                <td>
                                     %s

                                </td><td>
                                     %s

                                </td><td style="color:%s">
                                     %s

                                </td><td style="color: %s">
                                     %s%%
                                </td>
                       </tr>
                   </table>
               </div>''' % (result[1], result[2], result[6], result[4], result[6], result[5])
            return resultshow

      def performanceshow(self):
            performanceshow = '''
               <div id="container" style="min-width:400px;height:400px" ></div>
               '''
            return performanceshow

      def matchdetail(self, i, testname, testpic, testmatch):
            matchdetail = '''
                               <tr >
                                     <td>
                                           ''' + str(i) + '''
                                     </td>
                                     <td>
                                           <img src=./capture/User/''' + str(testname) + '''.png >

                                     </td>
                                     <td>
                                         <a href=./capture/target/''' + str(
                  testpic) + '''.png target="_blank" ><span>''' + str(testpic) + '''</span></a>

                                     </td>
                                         <td>
                                           ''' + str(testmatch) + '''
                                     </td>
                               </tr>'''
            return matchdetail

      def matchshow(self, matchlist):
            matchshow = '''
      <div id="match" style="margin-top: 60px">
                    <table style="max-width:400px" align="center">
                          <thead ><tr><th colspan="8">关键位置测试详情</th></tr></thead>
                          <tr id="matchbt">
                                <td style="min-width:50px">
                                      序号
                                </td >
                                <td style="min-width:150px">
                                      需要验证
                                </td>
                                <td style="min-width:135px">
                                      验证图
                                </td >
                                <td style="min-width:120px">
                                      验证结果
                                </td>
                          </tr>'''

            matchdetails = ""
            matchnum = 1
            for i in matchlist:
                  matchone = i.split(",")
                  matchdetails = matchdetails + self.matchdetail(matchnum, matchone[1], matchone[2], matchone[3])
                  matchnum = matchnum + 1
            matchshowend = '''     
                    </table>
                           </div>
      '''
            return matchshow + matchdetails + matchshowend

      def performancedata(self, cpudata, Mdata, number):
            performancedata = '''
              <script>
                  $(function () {
          $('#container').highcharts({
              chart: {
                  zoomType: 'xy'
              },
              title: {
                  text: '性能数据展示'
              },
      //        subtitle: {
      //            text: '数据来源: WorldClimate.com'
      //        },
              xAxis: [{
                  categories: ''' + str(number) + '''
                               ,
                  crosshair: true
              }],
              yAxis: [{ // Primary yAxis
                  min:0,
                  labels: {
                      format: '{value}MB',
                      style: {
                          color: Highcharts.getOptions().colors[0]
                      }
                  },
                  title: {
                      text: '内存占用',
                      style: {
                          color: Highcharts.getOptions().colors[0]
                      }
                  }
              }, { // Secondary yAxis
                  title: {
                      text: 'CPU占用',
                      style: {
                          color: Highcharts.getOptions().colors[8]
                      }
                  },
                  labels: {
                      format: '{value}%',
                      style: {
                          color: Highcharts.getOptions().colors[8]
                      }
                  },
                  opposite: true
              }],
              tooltip: {
                  shared: true
              },
              legend: {
                  layout: 'vertical',
                  align: 'left',
                  x: 120,
                  verticalAlign: 'top',
                  y: 100,
                  floating: true,
                  backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
              },
              series: [{
                  name: 'CPU占用',
                  type: 'spline',
                  color:Highcharts.getOptions().colors[8],
                  yAxis: 1,
                  data:''' + str(cpudata) + ''',
                  tooltip: {
                      valueSuffix: '%'
                  }
              }, {
                  name: '内存占用',
                  type: 'line',
                  color:Highcharts.getOptions().colors[0],
                  data:''' + str(Mdata) + ''',
                  tooltip: {
                      valueSuffix: 'MB'
                  }
              }]
          });
      });
              </script>
      '''
            return performancedata

      def testresult(self):
            testresult = '''
               <h3>测试任务结束，操作人员没有进行关键位置匹配和性能数据获取操作</h3>
               '''
            return testresult

      def htmldemoend(self):
            htmldemoend = '''
      </body>
      </html>
      '''
            return htmldemoend
if "__main__"==__name__:
      htmldemo("z20171120112239")