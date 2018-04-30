
import cv2
import find_ball

for index in range(1, 14):
    file = f'{index}.png'

    # read in image as grayscale
    opencv_image = cv2.imread("./imgs/" + file, cv2.COLOR_GRAY2RGB)

    # try to find the ball in the image
    ball = find_ball.find_ball(opencv_image, False, delta=50, minCircle=5, maxCircle=320)
    print(file, ' ball: ', ball)
