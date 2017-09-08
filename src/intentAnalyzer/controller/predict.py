import tensorflow as tf
tf.reset_default_graph()

def Predict(x_data):
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph('./model/intent_model-1000.meta')
        saver.restore(sess, tf.train.latest_checkpoint('./model'))
        graph = tf.get_default_graph()
        X = graph.get_tensor_by_name('x_data:0')
        hypothesis = graph.get_tensor_by_name('predicted:0')
        predicted = sess.run(hypothesis, feed_dict={X: x_data})
        return predicted
