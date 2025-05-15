# logistic_regression_binary_classification.py

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report

# Generate a synthetic binary classification dataset
X, y = make_classification(n_samples=100, n_features=2, n_redundant=0,
                           n_informative=2, n_clusters_per_class=1)

# Train logistic regression model
model = LogisticRegression()
model.fit(X, y)

# Predict
y_pred = model.predict(X)

# Plot
plt.figure()
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='bwr', alpha=0.6, edgecolor='k')
plt.title("Logistic Regression - Binary Classification")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.savefig("logistic_classification_plot.png")
plt.show()

# Metrics
print(confusion_matrix(y, y_pred))
print(classification_report(y, y_pred))
