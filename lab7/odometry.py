#!/usr/bin/env python3

'''
Stater code for Lab 7.

'''

import cozmo
from cozmo.util import degrees, Angle, Pose, distance_mm, speed_mmps
import math
import time

# Wrappers for existing Cozmo navigation functions

# Experiment warm up second for Cozmo Drive Wheels function,
# found by was determined by helper/understand_drive_wheels.py
# results is in helper/results/understand_drive_wheels.txt should be 0.8
# But for the length test, this should be 0.6
DRIVE_WHEELS_WARM_UP_SECOND = 0.6

def cozmo_drive_straight(robot, dist, speed):
    """Drives the robot straight.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            dist -- Desired distance of the movement in millimeters
            speed -- Desired speed of the movement in millimeters per second
    """
    robot.drive_straight(distance_mm(
        dist), speed_mmps(speed)).wait_for_completed()


def cozmo_turn_in_place(robot, angle, speed):
    """Rotates the robot in place.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            angle -- Desired distance of the movement in degrees
            speed -- Desired speed of the movement in degrees per second
    """
    robot.turn_in_place(degrees(angle), speed=degrees(
        speed)).wait_for_completed()


def cozmo_go_to_pose(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            x,y -- Desired position of the robot in millimeters
            angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    robot.go_to_pose(Pose(x, y, 0, angle_z=degrees(angle_z)),
                     relative_to_robot=True).wait_for_completed()

# Functions to be defined as part of the labs


def get_front_wheel_radius():
    """Returns the radius of the Cozmo robot's front wheel in millimeters."""
    # By watching the Cozmo to move straight and adjust the parameter,
    # found the length of circle is 86
    # The length was determined by helper/get_front_wheel_radium.py.
    # Results is in helper/results/get_front_wheel_radium.txt
    #   Radius is 13.687325105903
    return 13.69


def get_distance_between_wheels():
    """Returns the distance between the wheels of the Cozmo robot in millimeters."""

    # The distance was determined by helper/get_distance_between_wheel.py.
    # Results is in helper/results/get_distance_between_wheel.txt
    #   The test test with different speed and it's mutiplicatoin
    #   Also for each speed, test with multiple time with the differnt of duratoin
    #   The total average is 88.03572726050415
    return 88


def rotate_front_wheel(robot, angle_deg):
    """Rotates the front wheel of the robot by a desired angle.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            angle_deg -- Desired rotation of the wheel in degrees
    """
    # ####
    # TODO: Implement this function.
    # ####


def my_drive_straight(robot, dist, speed):
    """Drives the robot straight.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            dist -- Desired distance of the movement in millimeters
            speed -- Desired speed of the movement in millimeters per second
    """
    # ####
    # TODO: Implement your version of a driving straight function using the
    # robot.drive_wheels() function.
    # ####
    pass


def my_turn_in_place(robot, angle, speed):
    """Rotates the robot in place.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            angle -- Desired distance of the movement in degrees
            speed -- Desired speed of the movement in degrees per second
    """
    # ####
    # TODO: Implement your version of a rotating in place function using the
    # robot.drive_wheels() function.
    # ####
    pass


def my_go_to_pose1(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            x,y -- Desired position of the robot in millimeters
            angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    # ####
    # TODO: Implement a function that makes the robot move to a desired pose
    # using the my_drive_straight and my_turn_in_place functions. This should
    # include a sequence of turning in place, moving straight, and then turning
    # again at the target to get to the desired rotation (Approach 1).
    # ####
    pass


def my_go_to_pose2(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            x,y -- Desired position of the robot in millimeters
            angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    # ####
    # TODO: Implement a function that makes the robot move to a desired pose
    # using the robot.drive_wheels() function to jointly move and rotate the
    # robot to reduce distance between current and desired pose (Approach 2).
    # ####
    pass


def my_go_to_pose3(robot, x, y, angle_z):
    """Moves the robot to a pose relative to its current pose.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            x,y -- Desired position of the robot in millimeters
            angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    # ####
    # TODO: Implement a function that makes the robot move to a desired pose
    # as fast as possible. You can experiment with the built-in Cozmo function
    # (cozmo_go_to_pose() above) to understand its strategy and do the same.
    # ####
    pass


def run(robot: cozmo.robot.Robot):
    print(f"***** Front wheel radius     : {get_front_wheel_radius()}")
    print(f"***** Distance between wheels: {get_distance_between_wheels()}")

    # Example tests of the functions

    # cozmo_drive_straight(robot, 62, 50)

    # cozmo_turn_in_place(robot, 60, 30)

    # my_go_to_pose1(robot, 100, 100, 45)
    # my_go_to_pose2(robot, 100, 100, 45)

    # cozmo_go_to_pose(robot, 100, 100, 45)
    # my_go_to_pose3(robot, 100, 100, 45)


if __name__ == '__main__':
    cozmo.run_program(run)
