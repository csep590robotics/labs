
import cv2
import find_ball

file = '9.png'

# read in image as grayscale
opencv_image = cv2.imread("./imgs/" + file, cv2.COLOR_GRAY2RGB)

# try to find the ball in the image
ball = find_ball.find_ball(opencv_image, True, delta=50, minCircle=1, maxCircle=320)
print(file, ' ball: ', ball)
