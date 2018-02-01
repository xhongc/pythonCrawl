# coding=utf-8

__author__ = 'Administrator'

import socket
import logging

import AR_User.cof.co_time as CoTimeM


class ScribeHandler(logging.StreamHandler):
    """
    日志Scribe处理器

    将该handler加入日志记录设施
    """
    def __init__(self):
        #self.agent_ip = "192.168.205.8"
        self.agent_ip = "log.qa.huayu.nd"
        #self.agent_ip = "127.0.0.1"
        self.agent_port = 11215
        self.appid = "10010"
        self.filepath = "/LogTest/error.log"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.agent_ip, 11215))
        super(ScribeHandler, self).__init__(sock)
        self.sock = sock

    def set_appid(self, appid):
        self.appid = str(appid)

    def set_filepath(self, filepath):
        self.filepath = filepath

    def emit(self, record):
        """
        日志记录器日志发送函数

        record 日志记录

        MakeRecord()
        """
        # print "emit", record.levelname
        ts = CoTimeM.get_ts()

        try:
            # 根据格式字符串生成消息文本
            msg = self.format(record)
            msg = "[ts:\"" + str(ts) + "\"]" + \
                  "[level:\"" + record.levelname + "\"]" + \
                  "[filepath:\"" + self.filepath + "\"]" + \
                  "[msg:\"" + msg.replace('"', "\\\"") + "\"];"
            msg = self.appid + ":" + msg + "\n"
            #print msg

            # socket
            # stream = self.stream

            # 使用socket的发送方法来发送日志
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.agent_ip, self.agent_port))
            sock.send(msg)
            sock.close()

            self.flush()

        except (KeyboardInterrupt, SystemExit):
            raise

        except Exception, exc:
            self.handle_exc(Exception, exc)
            self.handleError(record)

    def handle_exc(self, arg1, arg2):
        """
        处理异常
        """
        pass

    def close(self):
        """
        Closes the stream.
        """
        self.acquire()
        try:
            if self.stream:
                self.flush()
                if hasattr(self.stream, "close"):
                    self.stream.close()
                self.stream = None
            # Issue #19523: call unconditionally to
            # 阻止句柄泄露
            # prevent a handler leak when delay is set
            logging.StreamHandler.close(self)
        finally:
            self.release()


if __name__ == "__main__":
    import datetime as DTM
    ts = str(DTM.datetime.now())

    logger = logging.getLogger('test01')
    scribe_handler = ScribeHandler()
    scribe_handler.set_appid("9996")
    scribe_handler.set_filepath('/LogTest/Test01/error.log')
    # scribe_handler.set_tag('');
    logger.addHandler(scribe_handler)
    logger.setLevel(logging.DEBUG)
    #logger.info("hello, world\t" + ts)
    #logger.debug("hello, linzh\t" + ts)
    s = """[ts:"1415618935"][case_id:"2"][filepath:"/UILog/CloudUI/TestCases/Advanced/Document/DocumentPreview/OfflineStatus/20141110192826.log"][level:"ERROR"][msg:"HyUi.UIException.TestCaseFailedException: Can't find webelement which text match '' and By:By.LinkText: auto-Offline
   在 HyUi.Browser.GetElements(IWebElement parentElement, By by, String textPattern) 位置 e:\Project\QA\工作文档\X 项目文档\华渔项目\Auto\Cloud\Cloud\Library\UI\Browser.cs:行号 311
   在 HyUi.Browser.GetElement(IWebElement parentElement, By by, String textPattern) 位置 e:\Project\QA\工作文档\X 项目文档\华渔项目\Auto\Cloud\Cloud\Library\UI\Browser.cs:行号 327
   在 HyUi.Browser.GetElement(IWebElement parentElement, By targetBy) 位置 e:\Project\QA\工作文档\X 项目文档\华渔项目\Auto\Cloud\Cloud\Library\UI\Browser.cs:行号 193
   在 HyUi.Browser.GetElement(By by) 位置 e:\Project\QA\工作文档\X 项目文档\华渔项目\Auto\Cloud\Cloud\Library\UI\Browser.cs:行号 158
   在 HyUi.Browser.ClickUrl(By by) 位置 e:\Project\QA\工作文档\X 项目文档\华渔项目\Auto\Cloud\Cloud\Library\UI\Browser.cs:行号 336
   在 HyUi.Browser.ClickUrl(String linkText) 位置 e:\Project\QA\工作文档\X 项目文档\华渔项目\Auto\Cloud\Cloud\Library\UI\Browser.cs:行号 440
   在 CloudUI.Test.WebPageClass.DocumentSearchPage.ClickDocumentName(String name) 位置 e:\Project\QA\工作文档\X 项目文档\华渔项目\Auto\Cloud\Cloud\CloudUI\WebPageClick"];
    """
    # s = "log test"
    for i in range(1):
        logger.debug(s)
    logger.removeHandler(scribe_handler)
