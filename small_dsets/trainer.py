#!/usr/bin/env python3

import argparse
import tensorflow as tf
import pandas
import numpy
import helpers

def load_dataset(input_csv):
    data=pandas.read_csv(input_csv)
    target=data[data.columns[-1]].as_matrix().astype(numpy.float64)
    X=data.drop(data.columns[-1],axis=1).as_matrix().astype(numpy.float64)
    return X,target

def batch_generator(X,y,size=1000):
    i=0
    while True:
        if i > X.shape[0]:
            i=0
        batch_x=X[i:i+size]
        batch_y=y[i:i+size]
        if batch_x.shape[0]==size:
            yield batch_x,batch_y
        else:
            difference=size-batch_x.shape[0]
            batch_x=numpy.vstack((batch_x,X[:difference]))
            batch_y=numpy.hstack((batch_y,y[:difference]))
            yield batch_x,batch_y
        i+=size

def compute_mse_loss(predictions,samples):
    return tf.reduce_sum(tf.pow(predictions-model.y_,2))/(2.0*samples)

def train(generator,epochs,model,save_dir):
    estopper=helpers.EarlyStopper()
    predictions=model.compute_predictions(model.x)
    cost=compute_mse_loss(predictions,batch_size)
    optimizer=tf.train.AdagradOptimizer(1.0).minimize(cost)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver=tf.train.Saver()
        epoch=0
        loss=0
        while epoch <= epochs:
            x_train,y_train=next(generator)
            out,_cost=sess.run([optimizer,cost],feed_dict={model.x:x_train,model.y_:y_train})
            loss+=_cost
            if epoch%100 == 0 and epoch!=0:
                print("Epoch: %d Loss: %s "%(epoch,str(loss/100.0)))
                if estopper.early_stop(loss/100):
                    saver.save(sess,save_dir)
                    break
                loss=0
            epoch+=1
        print()

def main():
    global batch_size
    parser=argparse.ArgumentParser()
    parser.add_argument("-i",help="input csv path.")
    parser.add_argument("-e",help="number of epochs.")
    parser.add_argument("-b",help="batch size.")
    parser.add_argument("-m",help="model file.")
    parser.add_argument("-s",help="path to save trained model.")
    args=parser.parse_args()
    batch_size=int(args.b)
    X,y=load_dataset(args.i)
    global model
    model=__import__(args.m)
    generator=batch_generator(X,y,batch_size)
    train(generator,int(args.e),model,args.s)
    

main()
