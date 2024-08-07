import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Load and preprocess data
data = pd.read_csv('./digit-recognizer/train.csv')
data = np.array(data)

m, n = data.shape
np.random.shuffle(data)

data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n] / 255.0  # Normalize input features

data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n] / 255.0  # Normalize input features

# Initialize parameters
def init_params():
    W1 = np.random.randn(10, 784) * np.sqrt(2./784)  # He initialization
    b1 = np.zeros((10, 1))
    W2 = np.random.randn(10, 10) * np.sqrt(2./10)   # He initialization
    b2 = np.zeros((10, 1))
    return W1, b1, W2, b2

# Activation functions
def ReLU(Z):
    return np.maximum(0, Z)

def softmax(Z):  
    expZ = np.exp(Z - np.max(Z, axis=0))
    return expZ / expZ.sum(axis=0)

# Forward propagation
def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2

# One-hot encoding of labels
def matrix_flip(Y):
    mat_Y = np.zeros((Y.size, Y.max() + 1))
    mat_Y[np.arange(Y.size), Y] = 1
    mat_Y = mat_Y.T
    return mat_Y

# Derivative of ReLU
def deriv_ReLu(X):
    return X > 0

# Backpropagation
def back_prop(Z1, A1, Z2, A2, W2, X, Y):
    m = Y.size
    mat_Y = matrix_flip(Y)
    dZ2 = A2 - mat_Y
    dW2 = 1/m * dZ2.dot(A1.T)
    db2 = 1/m * np.sum(dZ2, axis=1, keepdims=True)
    dZ1 = W2.T.dot(dZ2) * deriv_ReLu(Z1)
    dW1 = 1/m * dZ1.dot(X.T)
    db1 = 1/m * np.sum(dZ1, axis=1, keepdims=True)
    return dW1, db1, dW2, db2

# Update parameters
def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1
    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    return W1, b1, W2, b2

# Utility functions
def get_predictions(A2):
    return np.argmax(A2, axis=0)

def get_accuracy(predictions, Y):
    return np.sum(predictions == Y) / Y.size

# Gradient descent loop
def gradient_descent(X, Y, iterations, alpha):
    W1, b1, W2, b2 = init_params()
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = back_prop(Z1, A1, Z2, A2, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
        if i % 50 == 0:
            print("Iteration: ", i)
            print("Accuracy: ", get_accuracy(get_predictions(A2), Y))
    return W1, b1, W2, b2

# Train the model
W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 500, 0.1)

    
    
