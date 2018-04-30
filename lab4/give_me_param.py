#!/usr/bin/env python3

import cv2
import os
import math
import find_ball
import sys
import numpy as np

# load ground truth
with open('./imgs/ground_truth.txt') as f:
    grid_data = [i.split() for i in f.readlines()]

# thresh hold to accept circle and give credit per circle
center_err_thresh = 20.0
radius_err_thresh = 10.0
score = 0

print("start.....")

for guessDP in range(140, 176, 5):
    for delta in range(62, 44, -2):
        score = 0

        for filedata in grid_data:
            file = filedata[0]
            opencv_image = cv2.imread("./imgs/" + file, cv2.COLOR_GRAY2RGB)

            ball = find_ball.find_ball(opencv_image, False, [int(filedata[1]), int(filedata[2]), int(filedata[3])], delta=delta, guessDP=float(guessDP)/100)
            if ball is None:
                ball = np.array([0, 0, 0])

            center_err = math.sqrt((ball[0] - float(filedata[1]))**2 + (
                ball[1] - float(filedata[2]))**2)
            r_err = math.fabs(ball[2] - float(filedata[3]))
            if center_err <= center_err_thresh and r_err <= radius_err_thresh:
                score += 1

        print(f"score = {score}, guessDP = {float(guessDP)/100}, delta = {delta}")
