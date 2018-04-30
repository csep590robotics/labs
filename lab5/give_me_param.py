#!/usr/bin/env python3

import cv2
import os
import math
import find_ball
import sys
import numpy as np

print("start.....")

for guessDP in range(100, 176, 5):
    for delta in range(64, 44, -2):
        score = 0

        for index in range(1, 11):
            file = f'{index}.png'

            # read in image as grayscale
            opencv_image = cv2.imread("./imgs/" + file, cv2.COLOR_GRAY2RGB)

            # try to find the ball in the image
            ball = find_ball.find_ball(opencv_image, False, delta=delta, guessDP=guessDP, minCircle=15, maxCircle=320)
            if (index < 5 and ball is None):
                score += 1
            elif (index > 4 and ball is not None):
                score += 1

        print(f"score = {score}, guessDP = {float(guessDP)/100}, delta = {delta}")
