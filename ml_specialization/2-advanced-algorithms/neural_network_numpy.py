# neural_network_numpy.py

import numpy as np

# Sigmoid and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Input and expected output
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])  # XOR

# Random weights
np.random.seed(1)
weights1 = 2 * np.random.rand(2, 4) - 1
weights2 = 2 * np.random.rand(4, 1) - 1

# Train
for j in range(60000):
    l1 = sigmoid(np.dot(X, weights1))
    l2 = sigmoid(np.dot(l1, weights2))
    l2_error = y - l2
    if j % 10000 == 0:
        print("Error:", np.mean(np.abs(l2_error)))
    l2_delta = l2_error * sigmoid_derivative(l2)
    l1_error = l2_delta.dot(weights2.T)
    l1_delta = l1_error * sigmoid_derivative(l1)
    weights2 += l1.T.dot(l2_delta)
    weights1 += X.T.dot(l1_delta)

print("Predictions after training:
", l2.round())
