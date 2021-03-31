# -*- coding: utf-8 -*-
"""linear regression module.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LKZMsRuWx9P5ceDi3BXMIXyrt5FLOy36
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class LinearRegression:
    # Initalizing some useful variables
    def __init__(self, alpha=0.05, lam=0.0001, num_iters=500):
        ''' '__init__' method takes arguments as Learning Rate(alpha), Regularization Constant(lam), Number of iterations(num_iters).
        All of these values have been initialized by default values, but can be changed when required'''
        self.alpha = alpha
        self.lam = lam
        self.num_iters = num_iters

    def normalize(self, X):
        ''' 'normalize' method takes X as argument.
    Applies Feature Scalling by standardizing the data, adds biasing layer and returns X'''
        # X = (X - np.mean(X, axis=0))/(np.std(X, axis=0) + np.exp(-9))  "NOT WORKING"
        for i in range(X.shape[1]):
            X[:, i] = (X[:, i] - np.mean(X[:, i])) / (np.std(X[:, i]) + np.exp(-9))
        m = len(X)
        X0 = np.ones((m, 1))
        X = np.hstack((X0, X))
        return X

    def cost_function(self):
        ''' 'cost_function' method takes no arguments, returns cost value with regularization'''
        h = self.X @ self.theta  # h stands for hypothesis
        J = (1 / (2 * self.m)) * np.sum((h - self.y) ** 2) + (self.lam / (self.m * 2)) * np.sum(
            self.theta[1:, :] ** 2)  # j stands for cost value
        return J

    def fit(self, X, y):
        ''' 'fit' method takes X, y as arguments.
    Applies Gradient Descent algorithm and updates parameters theta '''

        # Normalization
        X = self.normalize(X)
        self.X = X
        self.y = y
        self.m, self.n = X.shape

        # Initializing parameter vector theta
        self.theta = np.zeros((self.n, 1))

        # Initializing some useful variables
        # 'J.history' and 'iters' keeps track of cost with each iteration.
        self.J_history = []
        self.iters = []

        # Applying Gradient Descent algorithm
        for i in range(self.num_iters):
            # Parameter update
            self.theta = self.theta * (1 - (self.alpha * self.lam / self.m)) - (self.alpha / self.m) * (
                        self.X.T @ (self.X @ self.theta - self.y))
            # Saving cost J in every iteration
            self.J_history.append(self.cost_function())
            self.iters.append([i])

    def plot(self):
        ''' 'plot' method takes no arguments.
     Plots the learning curve (Cost vs Number of Iteration) '''
        plt.plot(self.iters, self.J_history)
        plt.xlabel('Number of iterations')
        plt.ylabel('Cost Function')
        plt.title('Cost Function vs Iterations')

    def score(self, y, y_pred):
        ''' 'score' method takes y, y_pred as arguments.
    Calculates the y_mean and R2 score(Coefficient of determination), and returns R2 score'''
        score = 1 - ((y - y_pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        return score

    def predict(self, X):
        ''' 'predict' method takes X as argument,
    Calculates and returns the predicted values given by the trained model.'''
        X = self.normalize(X)
        y_pred = X @ self.theta
        return y_pred

    def accuracy(self, y, y_pred):
        ''' 'accuracy' method takes y(True values), y_pred(Predicted values) and returns the accuracy of the of trained model.'''
        m = len(y)
        accuracy = (np.mean(y==y_pred))*100
        return accuracy

    def y_pred_thresh(self, y_pred, threshold):
        ''' y_pred_thresh' function takes y_pred( Values predicted by trained model), and threshold value.
        Calculates and returns y_pred_thresh(Final predicted values with respect to given threshold value)'''
        y_pred_thresh = np.ceil(y_pred - threshold)
        return y_pred_thresh

    def threshold(self, y, y_pred):
        ''' threshold takes y_pred(Predicted values without threshold).
        Returns the threshold which gives maximum training accuracy.
        Prints Maximum accuracy and Threshold value '''
        thresh = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
                  0.9]
        acc_values = []  # Stores accuracy values for each threshold

        for i in thresh:
            y_pred_new = self.y_pred_thresh(y_pred, i)
            acc_values.append(self.accuracy(y, y_pred_new))

        index = np.argmax(acc_values)
        max_acc = acc_values[index]
        threshold_value = thresh[index]

        print("Maximum accuracy for traing data:", max_acc)
        print("Threshold value:", threshold_value)
        return threshold_value