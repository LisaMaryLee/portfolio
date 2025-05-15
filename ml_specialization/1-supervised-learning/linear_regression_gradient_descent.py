# linear_regression_gradient_descent.py

import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic data
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# Add x0 = 1 to each instance
X_b = np.c_[np.ones((100, 1)), X]

# Gradient descent
eta = 0.1
n_iterations = 1000
m = 100
theta = np.random.randn(2, 1)

for iteration in range(n_iterations):
    gradients = 2/m * X_b.T.dot(X_b.dot(theta) - y)
    theta -= eta * gradients

print("Learned parameters:", theta)

# Plot
plt.scatter(X, y)
plt.plot(X, X_b.dot(theta), color="red")
plt.title("Linear Regression with Gradient Descent")
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("linear_regression_fit.png")
plt.show()
