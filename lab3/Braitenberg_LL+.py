#!/usr/bin/env python3

'''Make Cozmo behave like a Braitenberg machine with virtual light sensors and wheels as actuators.

The following is the starter code for lab.
'''

import asyncio
import time
import cozmo
import cv2
import numpy as np
import sys


def sense_brightness(image, columns):
    '''Maps a sensor reading to a wheel motor command'''

    h = image.shape[0]
    w = image.shape[1]
    avg_brightness = 0

    for y in range(0, h):
        for x in columns:
            avg_brightness += image[y, x]

    avg_brightness /= (h * len(columns))

    return avg_brightness


def mapping_funtion(sensor_value):
    '''Maps a sensor reading to a wheel motor command'''
    motor_value = 0.3 * sensor_value
    return motor_value


async def braitenberg_machine(robot: cozmo.robot.Robot):
    '''The core of the braitenberg machine program'''
    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
    print("Press CTRL-C to quit")

    camera = robot.camera
    fixed_gain = (camera.config.min_gain + camera.config.max_gain) * 0.5
    fixed_exposure_ms = 10
    camera.set_manual_exposure(fixed_exposure_ms, fixed_gain)

    while True:
        # get camera image
        event = await robot.world.wait_for(cozmo.camera.EvtNewRawCameraImage, timeout = 30)

        # convert camera image to opencv format
        opencv_image = cv2.cvtColor(np.asarray(event.image), cv2.COLOR_RGB2GRAY)
        # Determine the w/h of the new image
        h = opencv_image.shape[0]
        w = opencv_image.shape[1]
        sensor_n_columns = int(w / 2)

        # Sense the current brightness values on the right and left of the image.
        sensor_left = sense_brightness(
            opencv_image, columns = np.arange(sensor_n_columns))
        sensor_right = sense_brightness(
            opencv_image, columns = np.arange(w - sensor_n_columns, w))

        if (sensor_right > sensor_left):
            print(f"More light on RIGHT. ({sensor_left}, {sensor_right})")
        else:
            print(f"More light on LEFT. ({sensor_left}, {sensor_right})")

        # Map the sensors to actuators
        # TODO: You might want to switch which sensor is mapped to which motor.
        motor_right = mapping_funtion(sensor_right)
        motor_left = mapping_funtion(sensor_left)

        if (motor_right > motor_left):
            print(f"Should go LEFT. ({motor_left}, {motor_right})")
        else:
            print(f"Should go RIGHT. ({motor_left}, {motor_right})")

        # Send commands to the robot
        await robot.drive_wheels(motor_left, motor_right)

        time.sleep(.1)


cozmo.run_program(braitenberg_machine, use_viewer = True, force_viewer_on_top = True)
