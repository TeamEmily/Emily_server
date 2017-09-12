import tensorflow as tf
tf.reset_default_graph()

class Model():
    def __init__(self):
        self.learning_late = 0.1
        self.saver = tf.train.import_meta_graph('./model/intent_model-1000.meta')

    def train(self, x_data, y_data):

        print(x_data)
        n = len(x_data[0])
        print(n)
#        global_step = tf.Variable(0, trainable=False, name='global_step')

        X = tf.placeholder(tf.float32, [None, n])
        Y = tf.placeholder(tf.float32, [None, 3])

        W1 = tf.Variable(tf.random_normal([n, 10]), name='weight1')
        b1 = tf.Variable(tf.random_normal([10]), name='bias1')
        layer1 = tf.sigmoid(tf.matmul(X, W1) + b1)

        W2 = tf.Variable(tf.random_normal([10, 3]), name='weight2')
        b2 = tf.Variable(tf.random_normal([3]), name='bias2')
        hypothesis = tf.sigmoid(tf.matmul(layer1, W2) + b2)

        cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))
        train = tf.train.GradientDescentOptimizer(learning_rate=self.learning_late).minimize(cost)

        predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32, name='predicted')
        accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

#        saver = tf.train.Saver(tf.global_variables())

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
#            saver.restore(sess, tf.train.latest_checkpoint('./model'))
            for step in range(10001):
                print(x_data)
                sess.run(train, feed_dict={X: x_data, Y: y_data})
                if step % 100 == 0:
                    print(step, sess.run(cost, feed_dict={X: x_data, Y: y_data}))


            h, c, a = sess.run([hypothesis, predicted, accuracy], feed_dict={X: x_data, Y: y_data})
            print("\nHypotehsis: ", h, "\nCorrect: ", c, "\nAccuracy: ", a)
    #        saver.save(sess, './model/intent_model', global_step=1000)

    def Predict(x_data, sess):
        # saver = tf.train.import_meta_graph('./model/intent_model-1000.meta')
        # saver.restore(sess, tf.train.latest_checkpoint('./model'))
        graph = tf.get_default_graph()
        X = graph.get_tensor_by_name('x_data:0')
        hypothesis = graph.get_tensor_by_name('predicted:0')
        predicted = sess.run(hypothesis, feed_dict={X: x_data})
        return predicted

