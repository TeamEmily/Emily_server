import tensorflow as tf
import numpy as np
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
tf.reset_default_graph()
num_intent = 4

class Model():
    def __init__(self):
        self.learning_late = 0.1

    def train(self, x_data, y_data):

        print(x_data)
        n = len(x_data[0])
        print(n)
#        global_step = tf.Variable(0, trainable=False, name='global_step')

        X = tf.placeholder(tf.float32, [None, n], name='x_data')
        Y = tf.placeholder(tf.float32, [None, num_intent])

        W1 = tf.Variable(tf.random_normal([n, 100]), name='weight1')
        b1 = tf.Variable(tf.random_normal([100]), name='bias1')
        layer1 = tf.nn.relu(tf.matmul(X, W1) + b1)

        W2 = tf.Variable(tf.random_normal([100, num_intent]), name='weight2')
        b2 = tf.Variable(tf.random_normal([num_intent]), name='bias2')
        hypothesis = tf.sigmoid(tf.matmul(layer1, W2) + b2, name='hypothesis')

        cost = -tf.reduce_mean(Y * tf.log(tf.clip_by_value(hypothesis, 1e-10, 1.0)) + (1 - Y) * tf.log(tf.clip_by_value(1-hypothesis, 1e-10, 1.0)))
        train = tf.train.GradientDescentOptimizer(learning_rate=self.learning_late).minimize(cost)

        predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32, name='predicted')
        accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

        saver = tf.train.Saver()

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
#            saver.restore(sess, tf.train.latest_checkpoint('./model'))
            for step in range(100001):
                sess.run(train, feed_dict={X: x_data, Y: y_data})
                if step % 100 == 0:
                    print(step, sess.run(cost, feed_dict={X: x_data, Y: y_data}))


            h, c, a = sess.run([hypothesis, predicted, accuracy], feed_dict={X: x_data, Y: y_data})
            print("\nHypotehsis: ", h, "\nCorrect: ", c, "\nAccuracy: ", a)
            saver.save(sess, './model/intent_model', global_step=1000)

    def predict(self, x_data):
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(os.path.join(BASE_DIR, './model/intent_model-1000.meta'))
            saver.restore(sess, tf.train.latest_checkpoint(os.path.join(BASE_DIR, './model')))
            graph = tf.get_default_graph()
            X = graph.get_tensor_by_name('x_data:0')
            predicted = graph.get_tensor_by_name('predicted:0')
            hypothesis = graph.get_tensor_by_name('hypothesis:0')
            print(sess.run(hypothesis, feed_dict={X: x_data}))
            result = sess.run(predicted, feed_dict={X: x_data})
            print(result)
            intent_index = np.argmax(result)
            if result[0][intent_index] < 1:
                intent_index = -1
            return intent_index