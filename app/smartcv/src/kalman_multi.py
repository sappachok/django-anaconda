import os
import argparse
import numpy as np
import cv2
from smartcv.src.util import get_midpoint, get_distance, bb_intersection_over_union, displacement

class KalmanFilter_cv(object):
    def __init__(self):
        self.kalman = cv2.KalmanFilter(4, 4, 0)
        self.state = np.array([0, 0, 0, 0], np.float32)
        self.LR = 0
        self.UD = 0
        self.prediction = None
        self.kalman.transitionMatrix = np.array([[1., 0., self.LR, 0.], # left right
                                            [0., 1., 0., self.UD], # up down
                                            [0., 0., 1., 0.],
                                            [0., 0., 0., 1.]], np.float32)
        self.kalman.measurementMatrix = np.array((1. * np.eye(4, 4)), np.float32)
        # self.kalman.processNoiseCov = np.array((1. * np.eye(4, 4)), np.float32)
        # self.kalman.measurementNoiseCov = np.array((1. * np.eye(4, 4)), np.float32)
        # self.kalman.errorCovPost = np.array((1. * np.eye(4, 4)), np.float32)     
        self.kalman.processNoiseCov = np.array((1e-5 * np.eye(4, 4)), np.float32)
        self.kalman.measurementNoiseCov = np.array((1e-3 * np.eye(4, 4)), np.float32)
        self.kalman.errorCovPost = np.array((1e-1 * np.eye(4, 4)), np.float32)
        self.kalman.statePost = self.state
    
    def predict(self):
        # x, y, w, h = p_scalar
        # print("state", self.state)
        # self.state = np.array([x, y, w, h], np.float32)
        self.kalman.statePost = self.state
        self.prediction = self.kalman.predict()
        self.prediction = [int(self.prediction[i]) for i in range(len(self.prediction))]
        return self.prediction
    
    def update(self, p_scalar):
        x, y, w, h = p_scalar
        self.state = np.array([x, y, w, h], dtype='float32')
        measurement = (np.dot(self.kalman.measurementNoiseCov, np.random.randn(4, 1))).reshape(-1)
        measurement = np.dot(self.kalman.measurementMatrix, self.state) + measurement
        posterior = self.kalman.correct(np.array(measurement, np.float32))
        pos = (posterior[0], posterior[1], posterior[2], posterior[3])
        pos = [int(pos[i]) for i in range(len(pos))]
        if self.prediction:
            dist, direction, LR, UD = displacement(self.prediction, pos)
            # print(self.prediction, pos)
            # print(dist, direction, LR, UD)
            self.LR = LR
            self.UD = UD
        self.prediction = pos
        process_noise = np.sqrt(self.kalman.processNoiseCov[0, 0]) * np.random.randn(4, 1)
        self.state = np.array((np.dot(self.kalman.transitionMatrix, self.state) + process_noise.reshape(-1)), np.float32)
        self.kalman.transitionMatrix = np.array([[1., 0., self.LR, 0.],
                                            [0., 1., 0., self.UD],
                                            [0., 0., 1., 0.],
                                            [0., 0., 0., 1.]], np.float32)
        return pos