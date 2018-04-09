#!/usr/bin/env python3

import cv2
import sys
import copy

import numpy as np

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit('install Pillow to run this code')


def find_ball(opencv_image, debug=False, best=None, threshold=100, delta=54, guessDP=1.55, minCircle=10, maxCircle=120, minDist=40):
    """Find the ball in an image.

            Arguments:
            opencv_image -- the image
            debug -- an optional argument which can be used to control whether
                            debugging information is displayed.

            Returns [x, y, radius] of the ball, and [0,0,0] or None if no ball is found.
    """

    ball = None

    gray_image = get_gray_image(opencv_image)
    circles = try_find_ball(gray_image, debug, threshold,
                            delta, guessDP, minCircle, maxCircle, minDist)

    if circles is None:
        ball = np.array([0, 0, 0])
        debugLog("Result - Didn't find any ball", debug)
    else:
        ball = np.round(circles[0, :]).astype("int")
        debugLog(f"Result - Find the ball: {ball}", debug)

    if (debug):
        display_circles(opencv_image, [ball], best)

    return ball


def get_gray_image(image):
    try:
        return cv2.cvtColor(opencv_image, cv2.COLOR_RGB2GRAY)
    except:
        return image


def debugLog(message, debug=False):
    if (debug):
        print(message)


def try_find_ball(gray_image, debug=False, threshold=100, delta=54, guessDP=1.55, minCircle=10, maxCircle=90, minDist=40):
    number_of_circles_expected = 1

    minimum_circle_size = minCircle
    maximum_circle_size = maxCircle
    guess_dp = guessDP
    guess_accumulator_array_threshold = threshold

    circles = None

    debugLog("Start find the ball in image with these parameters:", debug)
    debugLog(f"minimum circle size: {minimum_circle_size}", debug)
    debugLog(f"maximum circle size: {maximum_circle_size}", debug)
    debugLog(f"guess dp:            {guess_dp}", debug)
    debugLog(f"maximum threshold:   {guess_accumulator_array_threshold}", debug)
    debugLog(f"minimum threshold:   {threshold - delta}", debug)

    while guess_accumulator_array_threshold > threshold - delta:
        guess_radius = maximum_circle_size
        debugLog(f"adjust the threshold, and resetting guess_radius", debug)

        while guess_radius >= minimum_circle_size:
            circles = cv2.HoughCircles(
                gray_image, cv2.cv2.HOUGH_GRADIENT,
                dp=guess_dp,
                minDist=minDist,
                param1=50,
                param2=guess_accumulator_array_threshold,
                minRadius=(guess_radius - 3),
                maxRadius=(guess_radius + 3)
            )

            if circles is not None:
                if len(circles[0]) == number_of_circles_expected:
                    debugLog(f"Find one circle with guessing radius: {guess_radius} and dp: {guess_dp} vote threshold: {guess_accumulator_array_threshold}")
                    return copy.copy(circles[0])
                else:
                    debugLog(f"Find {len(circles[0])} circles with guessing radius: {guess_radius} and dp: {guess_dp} vote threshold: {guess_accumulator_array_threshold}, skip it", debug)

                circles = None
            else:
                debugLog(f"Didn't find circles with guessing radius: {guess_radius} and dp: {guess_dp} vote threshold: {guess_accumulator_array_threshold}", debug)

            guess_radius -= 3

        guess_accumulator_array_threshold -= 2
    return None


def display_circles(opencv_image, circles, best=None):
    """Display a copy of the image with superimposed circles.

       Provided for debugging purposes, feel free to edit as needed.

       Arguments:
            opencv_image -- the image
            circles -- list of circles, each specified as [x,y,radius]
            best -- an optional argument which may specify a single circle that will
                            be drawn in a different color.  Meant to be used to help show which
                            circle is ranked as best if there are multiple candidates.

    """
    # make a copy of the image to draw on
    circle_image = copy.deepcopy(opencv_image)
    circle_image = cv2.cvtColor(circle_image, cv2.COLOR_GRAY2RGB, circle_image)

    for c in circles:
        # draw the outer circle
        cv2.circle(circle_image, (c[0], c[1]), c[2], (255, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(circle_image, (c[0], c[1]), 2, (0, 255, 255), 3)
        # write coords
        cv2.putText(circle_image, str(c), (c[0], c[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (255, 255, 255), 2, cv2.LINE_AA)

    # highlight the best circle in a different color
    if best is not None:
        # draw the outer circle
        cv2.circle(circle_image, (best[0], best[1]), best[2], (0, 0, 255), 2)
        # draw the center of the circle
        cv2.circle(circle_image, (best[0], best[1]), 2, (0, 0, 255), 3)
        # write coords
        cv2.putText(circle_image, str(best), (best[0], best[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (255, 255, 255), 2, cv2.LINE_AA)

    # display the image
    pil_image = Image.fromarray(circle_image)
    pil_image.show()


if __name__ == "__main__":
    pass
