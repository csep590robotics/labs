#!/usr/bin/env python3

'''
Stater code for Lab 8.

'''

import cozmo
from cozmo.util import degrees, Angle, Pose, distance_mm, speed_mmps
import math
import time

def run(robot: cozmo.robot.Robot):

	try:
		while True:
			
			#angular_velocity
			print("Gyro" + str(robot.gyro.x) + "," + str(robot.gyro.y) + "," + str(robot.gyro.z))

			#linear_acceleration
			print("Accelerometer" + str(robot.accelerometer.x*0.001) + "," + str(robot.accelerometer.y*0.001) + "," + str(robot.accelerometer.z*0.001))

			time.sleep(.2)

	except KeyboardInterrupt:
		print("")
		print("Exit requested by user")
	except cozmo.RobotBusy as e:
		print(e)


if __name__ == '__main__':

	cozmo.run_program(run)
