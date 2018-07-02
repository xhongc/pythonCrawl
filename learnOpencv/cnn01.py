import tensorflow as tf
import numpy as np

train_x = np.linspace(-1, 1, 100)
train_y = 2 * train_x + np.random.randn(*train_x.shape) * 0.33 + 10

X = tf.placeholder('float')
Y = tf.placeholder('float')

w = tf.Variable(0.0, name='weight')
b = tf.Variable(0.0, name='bias')
loss = tf.square(Y - tf.multiply(X, w) - b)
train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    epoch = 1
    for i in range(10):
        for (x, y) in zip(train_x, train_y):
            _, w_value, b_value = sess.run([train_op, w, b], feed_dict={X: x, Y: y})
            print('epoch: {},w:{},b:{}'.format(epoch, w_value, b_value))
            epoch += 1
