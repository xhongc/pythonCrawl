import unittest
from pprint import pprint
from requests.sessions import Session

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class DemoApi(object):
    def __init__(self, base_url):
        self.base_url = base_url
        # 创建session实例
        self.session = Session()

    def login(self, username, password):
        """
        登录接口
        :param username: 用户名
        :param password: 密码
        """
        url = urljoin(self.base_url, 'login')
        data = {
            'username': username,
            'password': password
        }
        response = self.session.post(url, data=data).json()
        print('\n*****************************************')
        print(u'\n1、请求url: \n%s' % url)
        print(u'\n2、请求头信息:')
        pprint(self.session.headers)
        print(u'\n3、请求参数:')
        pprint(data)
        print(u'\n4、响应:')
        pprint(response)
        return response

    def info(self):
        """
        详情接口
        """
        url = urljoin(self.base_url, 'info')
        response = self.session.get(url).json()
        print('\n*****************************************')
        print(u'\n1、请求url: \n%s' % url)
        print(u'\n2、请求头信息:')
        pprint(self.session.headers)
        print(u'\n3、请求cookies:')
        pprint(dict(self.session.cookies))
        print(u'\n4、响应:')
        pprint(response)
        return response


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://127.0.0.1:5000'
        cls.username = 'admin'
        cls.password = '123456'
        cls.app = DemoApi(cls.base_url)

    def test_login(self):
        """
        测试登录
        """
        response = self.app.login(self.username, self.password)
        assert response['code'] == 200
        assert response['msg'] == 'success'

    def test_info(self):
        """
        测试获取详情信息
        """
        self.app.login(self.username, self.password)
        response = self.app.info()
        assert response['code'] == 200
        assert response['msg'] == 'success'
        assert response['data'] == 'info'
