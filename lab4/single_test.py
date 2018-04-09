
import cv2
import find_ball
import math
import numpy as np

# file = 'test91.bmp'
# answer = [160, 56, 13]
file = 'test65.bmp'
answer = [278, 118, 84]
# file = 'test73.bmp'
# answer = [0, 0, 0]

# read in image as grayscale
opencv_image = cv2.imread("./imgs/" + file, cv2.COLOR_GRAY2RGB)

# try to find the ball in the image
ball = find_ball.find_ball(opencv_image, True, answer)
print(file, ' result: ', ball)
print(file, ' answer: ', answer)

center_err_thresh = 20.0
radius_err_thresh = 10.0

# get center err
center_err = math.sqrt((ball[0] - float(answer[0]))**2 + (
    ball[1] - float(answer[1]))**2)

# get radius err
r_err = math.fabs(ball[2] - float(answer[2]))

print("circle center err =", center_err, "pixel")
print("circle radius err =", r_err, "pixel")
if center_err <= center_err_thresh and r_err <= radius_err_thresh:
    print("correct")
else:
    print("wrong")
