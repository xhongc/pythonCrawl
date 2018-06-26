import tensorflow as tf

state = tf.Variable(0, name='counter')
one = tf.constant(1)

new_value = tf.add(state, one)
update = tf.assign(state, new_value)

init = tf.initialize_all_variables()  # 初始化 变量常量

with tf.Session() as sess:
    sess.run(init)  # run 初始化
    for _ in range(9):
        sess.run(update)
        print(sess.run(state))
