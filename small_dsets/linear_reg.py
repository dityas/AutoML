import tensorflow as tf

x=tf.placeholder(tf.float64,[None,289],name="input")
y_=tf.placeholder(tf.float64,name="labels")

def compute_predictions(x):
    W=tf.Variable(tf.random_normal([289,1],mean=0.0,stddev=1.0,dtype=tf.float64))
    b=tf.Variable(tf.random_normal([1],dtype=tf.float64))
    return tf.add(tf.matmul(x,W),b,name="prediction")
