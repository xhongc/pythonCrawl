import logging_t
# 使用一个名字为fib的logger
logger = logging_t.getLogger('fib')

# 设置logger的level为DEBUG
logger.setLevel(logging_t.DEBUG)

# 创建一个输出日志到控制台的StreamHandler
hdr = logging_t.StreamHandler()
formatter = logging_t.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
hdr.setFormatter(formatter)

# 给logger添加上handler
logger.addHandler(hdr)