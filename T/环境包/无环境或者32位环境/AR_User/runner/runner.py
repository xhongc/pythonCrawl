# coding=utf-8

"""
using method:
    input command in cmd linke "python runner.py case_2 case_1"
"""
import os
import sys
import importlib
import copy
from optparse import OptionParser

reload(sys)
sys.setdefaultencoding('utf8')
sys.path.insert(0, '..')

from pprint import pprint

import json
import socket

import HTMLTestRunner

import cof.file as CoFileM

import cof.conf as CoConfM

import cof.im as Sender

import cof.co_time as cofTime

import nose
from nose import suite
from nose import loader
from cof.conf import MyCfg

opt_parser = OptionParser()
opt_parser.add_option("-s", "--suite", dest="suite", help=u"指定运行的测试套件", metavar="SUITE")

(options, opt_args) = opt_parser.parse_args()

suite_opt = options.suite

app_loc = CoFileM.get_app_loc()
app_cfg = CoConfM.get_cfg_type()
app_gbl_cfg_file = CoConfM.get_cfg_type_path()

if not suite_opt:
    suite_config = "suites.json"
else:
    # 到指定的目录获取对应的测试集配置
    suite_config = app_loc + "config" + os.sep + app_cfg + os.sep + suite_opt + ".json"

# 获取当前时间
date = cofTime.get_date_ymd()       # 日期【20150213】
timestamp = str(cofTime.get_ts())   # 时间戳【1423813170】

# 当前路径
path = os.path.abspath(__file__)
path = os.path.dirname(path)

argvs = sys.argv
if len(argvs) <= 2:
    ip = '172.24.128.14'
else:
    ip = argvs[2]

if len(argvs) <= 3:
    port = '5816'
else:
    port = argvs[3]

if len(argvs) <= 4:
    test_type = 'test14'
else:
    test_type = argvs[4]

if len(argvs) <= 5:
    push_group = 'yes'
else:
    push_group = argvs[5]

if len(argvs) <= 6:
    execution_times = '1'
else:
    execution_times = argvs[6]

report_url = ""

def set_case_list():
    """
    从命令行读取需要运行的测试集，返回测试集列表
    """

    argvs = ['runner.py', 'case_test']

    if len(argvs) <= 1:         # 没有指定测试用例集，默认运行所有测试用例（nose自动识别）
        print "no specified cases, could run all cases"
        return None

    if argvs[1] == "--all":     # 运行配置文件中的所有用例集（待实现）
        print "run all cases specified in json file"
        return None

    # 读suites.json配置文件，获取所有划分的测试集
    file = open(suite_config)

    case_set = json.load(file)

    # 测试集
    suite_list = list()

    # for i in range(1, len(argvs)):
    case_set_name = argvs[1]
    case_tmp = case_set[case_set_name]
    suite_list.append(case_tmp)

    if len(suite_list) == 0:
        print "测试集为空，停止运行"
        exit(0)

    return suite_list


def generate_suites(root, test_sets):
    """
    生成测试套件
    """
    suites = suite.LazySuite()

    sys.path.append(root)
    #print "sys.path :"
    #for path_i in sys.path:
    #    print path_i

    for ts_name, ts in test_sets.iteritems():
        for tc in ts:
            print "tc xxxxxxx: ", tc
            tc_complete = ts_name + "." + tc    # 用例文件完整的路径
            print "tc_complete: ", tc_complete
            pprint(sys.path)
            module = importlib.import_module(tc_complete)
            print "module: ", module
            suites.addTest(loader.TestLoader().loadTestsFromModule(module))
    return suites


def run_test_cases(test_sets, report_dir, report_title):
    """
    运行测试用例
    test_sets：字典格式的测试集
    """
    # 判断报告文件夹是否存在，若不存在则创建
    is_exist = os.path.exists(report_dir)
    if is_exist is False:
        os.makedirs(report_dir)

    # 指定测试集
    root = os.path.dirname(os.path.abspath(__file__)) + "\\..\\testcases"
    test_suites = generate_suites(root, test_sets)      # 只运行指定测试用例集
    #test_suites = nose.collector()                     # 运行全部用例

    # 定义报告名称
    file_path = report_dir + '\\' + date + timestamp + '.html'
    fp = file(file_path, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=report_title      # 如：'共享平台接口测试[ApiTest for SDP]'
    )
    print "test_suites=============" + str(test_suites.__dict__)
    runner.run(test_suites)


def get_data_old(all_the_text):
    """
    获取结果报告中每一项的数值
    text:报告内容
    keyword：该项内容的关键字
    """
    # runtime
    start = all_the_text.find("<strong>Start Time:</strong>")
    end = all_the_text.find("</p>", start+29)
    runtime = str(all_the_text[start+29:end])
    # timeSpend
    start = all_the_text.find("<strong>Duration:</strong>")
    end = all_the_text.find("</p>", start+27)
    time_spend = str(all_the_text[start+27:end])

    hour_end = time_spend.find(":")
    hour = int(time_spend[0:hour_end])
    min_start = hour_end+1
    min_end = time_spend.find(":", min_start)
    min = int(time_spend[min_start:min_end])
    second_start = min_end+1
    second_end = time_spend.find(".", second_start)
    second = int(time_spend[second_start:second_end])
    mis = time_spend[second_end:]
    time_spend = float(str(3600*hour+60*min+second)+mis)

    # total
    start = all_the_text.find("<td>Total</td>")
    end = all_the_text.find("</td>", start+23)
    total_num = int(all_the_text[start+23:end])
    # pass
    start = end
    end = all_the_text.find("</td>", start+14)
    pass_num = int(all_the_text[start+14:end])
    # failed
    start = end
    end = all_the_text.find("</td>", start+14)
    failed_num = int(all_the_text[start+14:end])
    # error
    start = end
    end = all_the_text.find("</td>", start+14)
    error_num = int(all_the_text[start+14:end])
    # percent + avgTime
    percent = 0.0
    avg_time = 0.0
    if total_num != 0:
        percent = int((float(total_num-failed_num-error_num)/total_num)*10000)/100.0
        avg_time = int(float(time_spend/total_num)*100)/100.0

    return [runtime, time_spend, total_num, pass_num, failed_num, error_num, percent, avg_time]


def get_data(all_the_text):
    """
    获取结果报告中每一项的数值
    text:报告内容
    keyword：该项内容的关键字
    """
    # runtime
    start = all_the_text.find("<strong>该次测试执行于:</strong>")
    end = all_the_text.find("</p>", start+40)
    runtime = str(all_the_text[start+40:end])
    # timeSpend
    start = all_the_text.find("<strong>接口运行时间:</strong>")
    end = all_the_text.find("</p>", start+37)
    time_spend = str(all_the_text[start+37:end])

    hour_end = time_spend.find(":")
    hour = int(time_spend[0:hour_end])
    min_start = hour_end+1
    min_end = time_spend.find(":", min_start)
    min = int(time_spend[min_start:min_end])
    second_start = min_end+1
    second_end = time_spend.find(".", second_start)
    second = int(time_spend[second_start:second_end])
    mis = time_spend[second_end:]
    time_spend = float(str(3600*hour+60*min+second)+mis)

    # total
    start = all_the_text.find("<td>Total</td>")
    end = all_the_text.find("</td>", start+23)
    total_num = int(all_the_text[start+23:end])
    # pass
    start = end
    end = all_the_text.find("</td>", start+14)
    pass_num = int(all_the_text[start+14:end])
    # failed
    start = end
    end = all_the_text.find("</td>", start+14)
    failed_num = int(all_the_text[start+14:end])
    # error
    start = end
    end = all_the_text.find("</td>", start+14)
    error_num = int(all_the_text[start+14:end])
    # percent + avgTime
    percent = 0.0
    avg_time = 0.0
    if total_num != 0:
        percent = int((float(total_num-failed_num-error_num)/total_num)*10000)/100.0
        avg_time = int(float(time_spend/total_num)*100)/100.0

    return [runtime, time_spend, total_num, pass_num, failed_num, error_num, percent, avg_time]


def get_result(report_dir, report_title, iis_port=None):
    """
    获取测试报告结果内容，组成推送信息
    report_dir：报告所在的文件夹路径
    """
    # 打开文件
    file_path = report_dir + '\\' + date + timestamp + '.html'
    file_object = open(file_path)
    all_the_text = ""
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()

    data = get_data(all_the_text)

    # 获取本地ip
    local_ip = socket.gethostbyname(socket.gethostname())

    # 获取报告的相对目录，作为url目录
    index = len(path) + 3
    relative_directory = (report_dir[index:]).replace("\\", "/")
    global report_url
    if iis_port != "":
        report_url = "http://" + local_ip + ":" + iis_port + relative_directory + "/" + date + timestamp + '.html'
    else:
        report_url = "http://" + local_ip + relative_directory + "/" + date + timestamp + '.html'
    result = "[" + data[0] + "]" + report_title +"测试结果： " \
             + "\n所有测试： " + str(data[2]) + "个" \
             + ",  通过： " + str(data[3]) + "个" \
             + ",  错误： " + str(data[5]) + "个" \
             + ",  失败： " + str(data[4]) + "个" \
             + ",  通过率： " + str(data[6]) \
             + "%, 运行时间： " + str(data[1]) + "s"
    vag_time = data[7]
    threshold = 0.5
    #if vag_time > threshold:
        #result += ".\n平均用例运行时间为" + str(vag_time) +"s，超过" + str(threshold) + "s，请及时关注"
    result += ".\n具体测试结果请查看： " + report_url

    return result


def get_report_path(report_file):
    """
    根据配置的文件结构，生成文件路径
    path：当前路径
    """
    tmp = report_file.split('.')
    report_file_path = "\\..\\test_reports"
    for i in tmp:
        report_file_path += "\\"
        report_file_path += i
    report_dir = path + report_file_path

    return report_dir


def set_test_server():
    my_cfg = MyCfg('cfg.ini')
    my_cfg.set('ar_api', 'host', ip)
    my_cfg.set('ar_api', 'port', port)


def set_test_db():
    my_cfg = MyCfg('db.ini')
    # 测试数据库14配置
    print test_type
    if test_type == 'test14':
        print 'set test14 db info'
        my_cfg.set('db_info', 'host', '172.24.128.14')
        my_cfg.set('db_info', 'user', 'qa01')
        my_cfg.set('db_info', 'password', 'dIqaBOg5wO')
    # 开发数据库配置
    elif test_type == 'dev':
        print 'set dev db info'
        my_cfg.set('db_info', 'host', '192.168.251.22')
        my_cfg.set('db_info', 'user', 'ar_qa')
        my_cfg.set('db_info', 'password', '7EVA2eqiRA')
    # 测试数据库15配置
    elif test_type == 'test15':
        print 'set test15 db info'
        my_cfg.set('db_info', 'host', '172.24.128.15')
        my_cfg.set('db_info', 'user', 'qa01')
        my_cfg.set('db_info', 'password', 'dIqaBOg5wO')


if __name__ == "__main__":
    case_list = set_case_list()      # 获取划分的测试集信息列表

    if case_list is None:
        print "case_list is empty"
        exit()

    for case_info in case_list:
        # print "case_info: ", case_info

        report_file = case_info[u'report_file']
        iis_port = "801"

        test_sets = case_info[u'cases']
        a = copy.deepcopy(case_info[u'cases'])

        for keys in test_sets:
            for i in range(0, int(execution_times)-1):
                test_sets[keys].extend(a[keys])
                print test_sets
        title = case_info[u'title'] + "(服务器:" + ip + ",端口:" + port + ")"

        report_dir = get_report_path(report_file)
        set_test_server()
        set_test_db()

        run_test_cases(test_sets, report_dir, title)
        res = get_result(report_dir, title, iis_port=iis_port)

        print "report link:" + report_url

        if push_group == "yes":
            receivers = case_info[u'receivers']
            group = case_info[u'group']
            sender_o = Sender.SendNew99U()    # 新99u

            if len(receivers):
                if receivers is not None:
                    print "推送人："
                    print receivers
                    sender_o.send_to_receivers(res, receivers)
            if len(group):
                if group is not None:
                    print "推送群："
                    print group
                    # sender_o.send_to_groups(res, group)
