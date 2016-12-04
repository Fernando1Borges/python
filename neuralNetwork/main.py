#neural net from scratch: two layers;
#build an ai composer
# andreson horowitz team follow all on twitter- study machine learning on internet!
# Internet is the way!!! makes eveyrhting obsoleate!
# have a lot of data inputs

# build a two layer neural network, that will predict the xor output

import numpy as np
#times how long training is going to be
import time

#variables
n_hidden = 10
n_in = 10
#outputs
n_out = 10
#sample data
n_sample = 300


#hyper parameters
learning_rate = 0.01
momentum = 0.9
#non deterministic seeding
np.random.seed(0)

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

#sigmoid functions turns numbers into probablilities
#this is the activation function

def tanh_prime(x):
    return 1 - np.tanh(x)**2

#input data, transpose, layer 1, layer 2, biases
def train(x, t, V, W, bv, bw):

    #forward -- matrix multiply + biases
    A = np.dot(x, V) + bv
    Z = np.tanh(A)

    B = np.dot(Z, W) + bw
    Y = sigmoid(B)

    #backward propagation
    Ew = Y - t
    Ev = tanh_prime(A) * np.dot(W, Ew)

    #predict our loss
    dW = np.outer(Z, Ew)
    dV = np.outer(x, Ev)

    #cross
    loss = -np.mean(t * np.log(Y) + (1 - t) * np.log(1-Y))

    return loss, (dV, dW, Ev, Ew)


def predict(x, V, W, bv, bw):
    A = np.dot(x, V) + bv
    B = np.dot(np.tanh(A), W) + bw
    return (sigmoid(B) > 0.5).astype(int)

#create layers
V = np.random.normal(scale = 0.1, size = (n_in, n_hidden))
W = np.random.normal(scale=0.1, size=(n_hidden, n_out))


bv = np.zeros(n_hidden)
bw = np.zeros(n_out)

params= [V, W, bv, bw]

#generate our data
X = np.random.binomial(1, 0.5, (n_sample, n_in))
T = X ^ 1

#training time

#training time
for epoch in range(100):
    err = []
    upd = [0]*len(params)

    t0 = time.clock()
    #for each data point, update our weights
    for i in range(X.shape[0]):
        loss,grad = train(X[i], T[i], *params)
        #update loss
        for j in range(len(params)):
            params[j] -= upd[j]

        for j in range(len(params)):
            upd[j] = learning_rate * grad[j] * momentum * upd[j]

        err.append(loss)

    print('Epoch: %d, Loss: %.8f, Time: %.4fs' %(
        epoch, np.mean(err), time.clock()-t0))

#try to predict something
x = np.random.binomial(1, 0.5, n_in)
print('XOR prediction')
print(x)
print(predict(x, *params))
