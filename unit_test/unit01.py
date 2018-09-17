import unittest
from HTMLTestRunner import HTMLTestRunner


def add(a, b):
    return a + b


def minus(a, b):
    return a - b


def multi(a, b):
    return a * b


def divide(a, b):
    return a / b


class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    def setUp(self):
        print("每次执行之前准备环境")

    def tearDown(self):
        print("执行完成之后需要还原数据、断开连接")

    def test_add(self):
        """Test method add(a, b)"""
        print("add")
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        print("minus")
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        print("multi")
        self.assertEqual(6, multi(2, 3))

    @unittest.skip("I don't want to run this case.")
    def test_divide(self):
        """Test method divide(a, b)"""
        print("divide")
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathFunc))
    with open('HTMLReport.html', 'w', encoding='utf-8') as f:
        runner = HTMLTestRunner(stream=f,
                                title=u'My Resport',
                                description=u'Powered by xhongc.',
                                verbosity=2
                                )
        runner.run(suite)
