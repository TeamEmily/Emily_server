import tensorflow as tf
tf.reset_default_graph()
# Todo: make checkpoint for model
class Learning:
    def __init__(self, trainingSet):
        self.x_data = trainingSet.training
        self.y_data = trainingSet.output

    def train(self):
        n = len(self.x_data[0])
        global_step = tf.Variable(0, trainable=False, name='global_step')

        X = tf.placeholder(tf.float32, [None, n], name='x_data')
        Y = tf.placeholder(tf.float32, [None, 3])

        W1 = tf.Variable(tf.random_normal([n, 10]), name='weight1')
        b1 = tf.Variable(tf.random_normal([10]), name='bias1')
        layer1 = tf.sigmoid(tf.matmul(X, W1) + b1)

        W2 = tf.Variable(tf.random_normal([10, 3]), name='weight2')
        b2 = tf.Variable(tf.random_normal([3]), name='bias2')
        hypothesis = tf.sigmoid(tf.matmul(layer1, W2) + b2)

        cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))
        train = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost, global_step=global_step)

        predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32, name='predicted')
        accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

        with tf.Session() as sess:
            saver = tf.train.Saver(tf.global_variables())
            sess.run(tf.global_variables_initializer())

            for step in range(10001):
                sess.run(train, feed_dict={X: self.x_data, Y: self.y_data})
                if step % 100 == 0:
                    print(step, sess.run(cost, feed_dict={X: self.x_data, Y: self.y_data}))


            h, c, a = sess.run([hypothesis, predicted, accuracy], feed_dict={X: self.x_data, Y: self.y_data})
            print("\nHypotehsis: ", h, "\nCorrect: ", c, "\nAccuracy: ", a)
            saver.save(sess, './model/intent_model', global_step=1000)