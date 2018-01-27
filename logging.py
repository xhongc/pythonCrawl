import logging
# 使用一个名字为fib的logger
logger = logging.getLogger('fib')

# 设置logger的level为DEBUG
logger.setLevel(logging.DEBUG)

# 创建一个输出日志到控制台的StreamHandler
hdr = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
hdr.setFormatter(formatter)

# 给logger添加上handler
logger.addHandler(hdr)