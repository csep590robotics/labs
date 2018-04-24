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
    #   Also for each speed, test with multiple time with the differnt of duration
    #   The total average is 88.03572726050415
    return 88


def rotate_front_wheel(robot, angle_deg):
    """Rotates the front wheel of the robot by a desired angle.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            angle_deg -- Desired rotation of the wheel in degrees
    """
    radians = math.radians(angle_deg)
    distance = radians * get_front_wheel_radius()
    cozmo_drive_straight(robot, distance, 50)


def my_drive_straight(robot, dist, speed, debug = False):
    """Drives the robot straight.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            dist -- Desired distance of the movement in millimeters
            speed -- Desired speed of the movement in millimeters per second
    """
    if speed < 0:
        robot.say_text('Cannot do that').wait_for_completed()
    if dist < 0 and speed > 0:
        speed = -speed
        dist = abs(dist)

    old_position = robot.pose.position.x
    new_position = old_position
    DRIVE_WHEELS_WARM_UP_SECOND = 0.2
    while dist - (new_position - old_position) > 0:
        rest = dist - abs(old_position - new_position)
        if debug:
            print(f'old_position {old_position}')
            print(f'new_position {new_position}')
            print(f'rest {rest}')
        if abs(rest) < 5:
            break
        if rest < speed:
            speed = speed / abs(speed) * rest
            if debug:
                print(f'lower speed to {speed}')
        elif rest - speed < 30:     # Cannot move when distance is small
            speed = speed / abs(speed) * rest + 10
            if debug:
                print(f'higher speed to {speed}')
        robot.drive_wheels(speed, speed, 0, 0, duration=DRIVE_WHEELS_WARM_UP_SECOND + 1)
        time.sleep(DRIVE_WHEELS_WARM_UP_SECOND + 1)
        new_position = robot.pose.position.x
        if debug:
            rest = dist - abs(new_position - old_position)
            print(f'rest {rest}')


def my_turn_in_place(robot, angle, speed, debug = False):
    """Rotates the robot in place.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            angle -- Desired distance of the movement in degrees
            speed -- Desired speed of the movement in degrees per second
    """
    if debug:
        print(f"Angle to {angle}, speed to {speed}")

    if speed < 0:
        robot.say_text('Cannot do that').wait_for_completed()
    while angle > 360:  # Reduce the turning angle
        angle -= 360
    while angle < -360: # Reduce the turning angle
        angle += 360
    if angle > 180:     # Reduce the turning angle
        angle = 360 - angle
        speed = -speed
    if angle < -180:    # Reduce the turning angle
        angle = 360 + angle
        speed = -speed
    if angle < 0 and speed > 0:
        speed = -speed
        angle = abs(angle)
    if debug:
        print(f"Adjust angle to {angle}, speed to {speed}")

    # If speed is positive turn left, otherwise, turn right
    old_angle = robot.pose.rotation.angle_z.degrees
    if old_angle < 0:
        old_angle += 360
    new_angle = old_angle
    DRIVE_WHEELS_WARM_UP_SECOND = 0.8
    while angle - (new_angle - old_angle) > 0:
        if speed > 0:
            delta = new_angle - old_angle
        else:
            delta = old_angle - new_angle
        if delta < 0:
            delta += 360
        rest = angle - delta
        if debug:
            print(f'rest {rest}')
        if abs(rest) < 5 or rest < 0:
            break
        if rest < abs(speed):
            speed = speed / abs(speed) * rest
            if debug:
                print(f'lower speed to {speed}')
        elif rest - speed < 20: # Cannot turn when degree is small
            speed = rest
            print(f'higher speed to {speed}')
        speed_mm = (get_distance_between_wheels() / 2) * math.radians(speed)
        robot.drive_wheels(-speed_mm, speed_mm, duration=DRIVE_WHEELS_WARM_UP_SECOND + 1)
        time.sleep(DRIVE_WHEELS_WARM_UP_SECOND + 1)
        new_angle = robot.pose.rotation.angle_z.degrees
        if new_angle < 0:
            new_angle += 360
        if debug:
            if speed > 0:
                delta = new_angle - old_angle
            else:
                delta = old_angle - new_angle
            if delta < 0:
                delta += 360
            rest = angle - delta
            print(f'rest {rest}')


def my_go_to_pose1(robot, x, y, angle_z, debug = False):
    """Moves the robot to a pose relative to its current pose.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            x,y -- Desired position of the robot in millimeters
            angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    distance = math.sqrt(x * x + y * y)
    angle = math.degrees(math.atan2(y, x))
    if debug:
        print(distance)
        print(angle)

    # Turn in place to point to new point
    my_turn_in_place(robot, angle, max(abs(angle / 2), 30), debug)
    # Move
    my_drive_straight(robot, distance, max(30, distance / 3), debug)
    # Turn in place to match angle_z
    angle = angle_z - angle
    my_turn_in_place(robot, angle, max(abs(angle / 2), 30), debug)


def my_go_to_pose2(robot, x, y, angle_z, debug = False):
    """Moves the robot to a pose relative to its current pose.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            x,y -- Desired position of the robot in millimeters
            angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    if y == 0:
        my_go_to_pose1(robot, x, y, angle_z, debug)
        return

    distance = math.sqrt(x * x + y * y)
    angle = math.atan2(abs(y), abs(x))
    if debug:
        print(f"distance: {distance}")
        print(f"angle: {angle}")
    # Circle Radius
    # theta = angle * 2
    # (distance / 2) : r = sin(theta / 2)
    # r = (distance / 2) / sin(theta / 2)
    r = (distance / 2) / math.sin(angle)
    # while turn left (y > 0):
    #   Arc length left = (r - b / 2) * (theta)
    #   Arc length right = (r + b / 2) * (theta)
    if y > 0:
        length_l = (r - get_distance_between_wheels() / 2) * (angle * 2)
        length_r = (r + get_distance_between_wheels() / 2) * (angle * 2)
        speed_l = max(30, length_l / 3)
        duration = length_l / speed_l
        speed_r = length_r / duration
    else:
        length_l = (r + get_distance_between_wheels() / 2) * (angle * 2)
        length_r = (r - get_distance_between_wheels() / 2) * (angle * 2)
        speed_r = max(30, length_r / 3)
        duration = length_r / speed_r
        speed_l = length_l / duration
    if debug:
        print(f"speed_l: {speed_l}")
        print(f"speed_r: {speed_r}")
    # Move
    robot.drive_wheels(speed_l, speed_r, duration = duration + DRIVE_WHEELS_WARM_UP_SECOND)
    time.sleep(duration + DRIVE_WHEELS_WARM_UP_SECOND)
    # Turn in place to match angle_z
    angle = angle_z - angle * 2
    my_turn_in_place(robot, angle, max(abs(angle / 2), 30), debug)


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
    for angle in range(15, 181, 15):
        old_position = robot.pose.position.x
        rotate_front_wheel(robot, angle)
        new_position = robot.pose.position.x
        distance = get_front_wheel_radius() * math.radians(angle)
        if (new_position - old_position > distance - 2) and (new_position - old_position < distance + 2):
            print(f'[rotate_front_wheel] Good in angle: {angle}')
        else:
            print(f'[rotate_front_wheel] Wrong in angle: {angle}, delta {abs(new_position - old_position - distance)}')

    # cozmo_drive_straight(robot, 62, 50)
    for distance in range(50, 100, 7):
        for speed in range(20, 50, 7):
            old_position = robot.pose.position.x
            my_drive_straight(robot, distance, speed)
            new_position = robot.pose.position.x
            if (new_position - old_position > distance - 10) and (new_position - old_position < distance + 10):
                print(f'[my_drive_straight] Good in distance: {distance}, speed: {speed}')
            else:
                print(f'[my_drive_straight] Wrong in distance: {distance}, speed: {speed}, delta {new_position - old_position - distance}')

    # cozmo_turn_in_place(robot, 60, 30)
    for angle in range(30, 181, 30):
        for speed in range(30, 61, 30):
            old_angle = robot.pose.rotation.angle_z.degrees
            if old_angle < 0:
                old_angle += 360
            print(f'start at {old_angle}')
            my_turn_in_place(robot, angle, speed)
            new_angle = robot.pose.rotation.angle_z.degrees
            if new_angle < 0:
                new_angle += 360
            print(f'end at {new_angle}')
            delta = new_angle - old_angle
            if delta < 0:
                delta += 360
            if (delta > angle - 10) and (delta < angle + 10):
                print(f'[my_turn_in_place] Good in angle: {angle}, speed: {speed}')
            else:
                print(f'[my_turn_in_place] Wrong in angle: {angle}, speed: {speed}, delta {abs(delta - angle)}')

    my_go_to_pose1(robot, 100, 0, 45, True)
    my_go_to_pose1(robot, -100, 0, -45, True)
    my_go_to_pose1(robot, 100, -100, -90, True)

    my_go_to_pose2(robot, 100, 0, 45, True)
    my_go_to_pose2(robot, 100, 100, 45, True)
    my_go_to_pose2(robot, 100, -100, 45, True)
    my_go_to_pose2(robot, -100, -100, 45, True)
    my_go_to_pose2(robot, 0, -150, 45, True)

    # cozmo_go_to_pose(robot, 100, 100, 45)
    # my_go_to_pose3(robot, 100, 100, 45)


if __name__ == '__main__':
    cozmo.run_program(run)
