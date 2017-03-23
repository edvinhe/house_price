#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn import linear_model

class Model(object):
    def __init__(self):
        pass

    def trainModel(self, X_train, Y_train):
        regression = linear_model.LinearRegression()

        regression.fit(X_train, Y_train)

        return regression


    def splitDataSet(self, dataset):
        X = dataset.values[:,0:7]
        Y = dataset.values[:,7]

        validation_size = 0.20
        seed = 7

        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

        return X_train, X_validation, Y_train, Y_validation



    def loadDataSet(self, fileName):
        names = ['Location', 'Community', 'Bedrooms', 'Size', 'Floor', 'Built Date', 'Avg Price', 'Price(10K)']
        dataset = pd.read_csv(fileName, names=names, header=None, delim_whitespace=True)

        return dataset

    def printDataSetDetail(self, dataset):
        print '=' * 30
        print(dataset.describe())
        print '=' * 30


    def getModel(self):
        model = Model()
        dataset = model.loadDataSet('./data/shuffled_house_price.csv')

        # model.printDataSetDetail(dataset)

        X_train, X_validation, Y_train, Y_validation = model.splitDataSet(dataset)

        regression = model.trainModel(X_train, Y_train)

        return regression


    def predictPrice(self, data):
        return self.getModel().predict(data)

if __name__ == '__main__':
    model = Model()
    dataset = model.loadDataSet('./data/shuffled_house_price.csv')

    model.printDataSetDetail(dataset)
    print

    X_train, X_validation, Y_train, Y_validation = model.splitDataSet(dataset)

    regression = model.trainModel(X_train, Y_train)
    meanSquaredError = np.mean((regression.predict(X_validation) - Y_validation) ** 2)
    print ("Mean squared error after prediction is: %.2f" %meanSquaredError)


