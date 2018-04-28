#!/usr/bin/env python3

'''
Stater code for Lab 7.

'''

import cozmo
from cozmo.util import degrees, Angle, Pose, distance_mm, speed_mmps
import math
import time
import sys

sys.path.insert(0, '../lab6')
from pose_transform import get_relative_pose

# Wrappers for existing Cozmo navigation functions

# Experiment warm up second for Cozmo Drive Wheels function,
# found by was determined by helper/understand_drive_wheels.py
# results is in helper/results/understand_drive_wheels.txt should be 0.9
# But for the length test, this should be 0.5
DRIVE_WHEELS_WARM_UP_SECOND = 0.9

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
    #   The total average is: 80.84659110426436
    return 80.85


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
    debug_print(f"[Drive Straight] Dist to {dist}, speed to {speed}", debug)
    if speed < 0:
        robot.say_text('Cannot do that').wait_for_completed()
        return
    if dist < 0 and speed > 0:
        speed = -speed
        dist = abs(dist)

    old_position = robot.pose
    new_position = old_position
    related_pose = get_relative_pose(new_position, old_position)
    rest = dist - abs(math.sqrt(related_pose.position.x**2 + related_pose.position.y**2))
    while rest > 0:
        debug_print(f"[Drive Straight] old_position {old_position}", debug)
        debug_print(f"[Drive Straight] new_position {new_position}", debug)
        debug_print(f"[Drive Straight] rest {rest}", debug)
        if abs(rest) < 5:
            break
        if rest < abs(speed):
            speed = get_number_signal(speed) * rest
            debug_print(f"[Drive Straight] lower speed to {speed}", debug)
        elif rest - abs(speed) < 10:     # Cannot move when distance is small
            speed = get_number_signal(speed) * (rest + 10)
            debug_print(f"[Drive Straight] higher speed to {speed}", debug)
        elif rest - abs(speed) < 30:     # Cannot move when distance is small
            speed = get_number_signal(speed) * rest
            debug_print(f"[Drive Straight] higher speed to {speed}", debug)
        robot.drive_wheels(speed, speed, 0, 0, duration=max(rest / abs(speed), 1))
        time.sleep(0.2)
        new_position = robot.pose
        related_pose = get_relative_pose(new_position, old_position)
        rest = dist - abs(math.sqrt(related_pose.position.x**2 + related_pose.position.y**2))
        if debug:
            debug_print(f"[Drive Straight] rest {rest}", debug)


def my_turn_in_place(robot, angle, speed, debug = False):
    """Rotates the robot in place.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            angle -- Desired distance of the movement in degrees
            speed -- Desired speed of the movement in degrees per second
    """
    debug_print(f"[Turn in Place] Angle to {angle}, speed to {speed}", debug)

    if speed <= 0:
        robot.say_text('Cannot do that').wait_for_completed()
    if abs(angle) <= 5:
        return

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
    debug_print(f"[Turn in Place] Adjust angle to {angle}, speed to {speed}", debug)

    # If speed is positive turn left, otherwise, turn right
    old_angle = robot.pose.rotation.angle_z.degrees
    if old_angle < 0:
        old_angle += 360
    new_angle = old_angle
    while angle - (new_angle - old_angle) > 0:
        if speed > 0:
            delta = new_angle - old_angle
        else:
            delta = old_angle - new_angle
        if delta < 0:
            delta += 360
        rest = angle - delta
        debug_print(f'[Turn in Place] rest {rest}', debug)
        if abs(rest) < 7 or rest < 0:
            break
        if rest < abs(speed) - 1:
            speed = get_number_signal(speed) * rest
            debug_print(f'[Turn in Place] lower speed to {speed}', debug)
        if rest < 31 and rest - abs(speed) < 20: # Cannot turn when degree is small
            speed = get_number_signal(speed) * (rest + 15)
            debug_print(f'[Turn in Place] higher speed to {speed}', debug)
        if abs(speed) < 35: # Cannot turn when degree is small
            speed = get_number_signal(speed) * (35)
            debug_print(f'[Turn in Place] higher speed 2 to {speed}', debug)
        speed_mm = (get_distance_between_wheels() / 2) * math.radians(speed)
        robot.drive_wheels(-speed_mm, speed_mm, duration=DRIVE_WHEELS_WARM_UP_SECOND + max(rest / abs(speed), 1))
        time.sleep(0.2)
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
            debug_print(f'[Turn in Place] rest {rest}', debug)


def my_go_to_pose1(robot, x, y, angle_z, debug = False):
    """Moves the robot to a pose relative to its current pose.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            x,y -- Desired position of the robot in millimeters
            angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    distance = math.sqrt(x * x + y * y)
    angle = math.degrees(math.atan2(y, x))
    debug_print(distance, debug)
    debug_print(angle, debug)

    # Turn in place to point to new point
    my_turn_in_place(robot, angle, max(abs(angle / 2), 50), debug)
    # Move
    my_drive_straight(robot, distance, max(50, distance / 3), debug)
    # Turn in place to match angle_z
    angle = angle_z - angle
    my_turn_in_place(robot, angle, max(abs(angle / 2), 50), debug)


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
    angle = math.atan2(abs(y), x)
    debug_print(f"distance: {distance}", debug)
    debug_print(f"angle: {math.degrees(angle)}", debug)
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
        speed_l = max(75, length_l / 2)
        duration = length_l / speed_l
        speed_r = length_r / duration
    else:
        length_l = (r + get_distance_between_wheels() / 2) * (angle * 2)
        length_r = (r - get_distance_between_wheels() / 2) * (angle * 2)
        speed_r = max(75, length_r / 2)
        duration = length_r / speed_r
        speed_l = length_l / duration
    debug_print(f"r: {r}", debug)
    debug_print(f"duration: {duration}", debug)
    debug_print(f"speed_l: {speed_l}", debug)
    debug_print(f"speed_r: {speed_r}", debug)
    # Move
    robot.drive_wheels(speed_l, speed_r, duration = DRIVE_WHEELS_WARM_UP_SECOND + duration)
    time.sleep(DRIVE_WHEELS_WARM_UP_SECOND)
    # Turn in place to match angle_z
    debug_print(f"angle_z: {angle_z}", debug)
    debug_print(f"angle: {math.degrees(angle)}", debug)
    angle_z = angle_z - get_number_signal(y) * math.degrees(angle * 2)
    debug_print(f"new_angle_z: {angle_z}", debug)
    my_turn_in_place(robot, angle_z, max(abs(angle_z / 2), 50), debug)


def my_go_to_pose3(robot, x, y, angle_z, debug = False):
    """Moves the robot to a pose relative to its current pose.
            Arguments:
            robot -- the Cozmo robot instance passed to the function
            x,y -- Desired position of the robot in millimeters
            angle_z -- Desired rotation of the robot around the vertical axis in degrees
    """
    # ####
    # Find out when the angle is larger than 90 degree,
    # cozmo_go_to_pose() function will turn first
    # ####
    if y == 0:
        my_go_to_pose1(robot, x, y, angle_z, debug)
        return

    distance = math.sqrt(x * x + y * y)
    theta = get_number_signal(y) * math.degrees(math.atan2(abs(y), x))
    debug_print(f"angle {theta}", debug)
    if abs(theta) > 90:
        turn_angle = theta - get_number_signal(theta) * 90
        debug_print(f"Turn {turn_angle} first to have less movement", debug)
        my_turn_in_place(robot, turn_angle, max(abs(turn_angle / 2), 50), debug)
        x = 0
        y = get_number_signal(y) * distance
        angle_z = angle_z - turn_angle
        debug_print(f"After turn adjust x: {x}, y: {y}, angle: {angle_z}", debug)

    my_go_to_pose2(robot, x, y, angle_z, debug)


def get_number_signal(number: float):
    return number / abs(number)


def debug_print(message: str, debug = False):
    if debug:
        print(message)


def run(robot: cozmo.robot.Robot):
    print(f"***** Front wheel radius     : {get_front_wheel_radius()}")
    print(f"***** Distance between wheels: {get_distance_between_wheels()}")

    # Example tests of the functions
    for angle in range(15, 181, 15):
        old_position = robot.pose
        rotate_front_wheel(robot, angle)
        new_position = robot.pose
        related_pose = get_relative_pose(new_position, old_position)
        moved = abs(math.sqrt(related_pose.position.x**2 + related_pose.position.y**2))
        distance = get_front_wheel_radius() * math.radians(angle)
        if abs(moved - distance) < 3:
            print(f'[rotate_front_wheel_test] Good in angle: {angle}')
        else:
            print(f'[rotate_front_wheel_test] Wrong in angle: {angle}, delta {abs(moved - distance)}')

    cozmo_drive_straight(robot, 62, 50)
    for distance in range(50, 100, 15):
        for speed in range(20, 50, 10):
            for signal in range(-1, 2, 2):
                dist = signal * distance
                old_position = robot.pose
                my_drive_straight(robot, dist, speed)
                new_position = robot.pose
                related_pose = get_relative_pose(new_position, old_position)
                moved = abs(math.sqrt(related_pose.position.x**2 + related_pose.position.y**2))
                if abs(moved - distance) < 10:
                    print(f'[my_drive_straight_test] Good in distance: {dist}, speed: {speed}')
                else:
                    print(f'[my_drive_straight_test] Wrong in distance: {dist}, speed: {speed}, delta {moved - distance}')

    cozmo_turn_in_place(robot, 60, 30)
    for orignal_angle in range(30, 181, 30):
        for speed in range(30, 61, 15):
            for signal in range(-1, 2, 2):
                angle = signal * orignal_angle
                old_angle = robot.pose.rotation.angle_z.degrees
                if old_angle < 0:
                    old_angle += 360
                my_turn_in_place(robot, angle, speed)
                new_angle = robot.pose.rotation.angle_z.degrees
                if new_angle < 0:
                    new_angle += 360
                if (new_angle > old_angle):
                    delta = new_angle - old_angle
                else:
                    delta = old_angle - new_angle
                if delta > 180:
                    delta -= 360
                if abs(abs(delta) - abs(angle)) < 10:
                    print(f'[my_turn_in_place_test] Good in angle: {angle}, speed: {speed}')
                else:
                    print(f'[my_turn_in_place_test] Wrong in angle: {angle}, speed: {speed}, delta {abs(delta) - abs(angle)}')

    my_go_to_pose1(robot, 100, 0, 45, True)
    my_go_to_pose1(robot, -100, 0, -45, True)
    my_go_to_pose1(robot, 100, -100, -90, True)

    my_go_to_pose2(robot, 100, 0, 45, True)
    my_go_to_pose2(robot, 100, 100, 45, True)
    my_go_to_pose2(robot, 100, -100, 45, True)
    my_go_to_pose2(robot, -100, -100, 45, True)
    my_go_to_pose2(robot, 0, -150, 45, True)

    cozmo_go_to_pose(robot, 100, 0, 45)
    cozmo_go_to_pose(robot, 100, 100, 45)
    cozmo_go_to_pose(robot, 100, -100, 45)
    cozmo_go_to_pose(robot, -100, -100, 45)
    cozmo_go_to_pose(robot, 0, -150, 45)

    my_go_to_pose3(robot, 100, 0, 45, True)
    my_go_to_pose3(robot, 100, 100, 45, True)
    my_go_to_pose3(robot, 100, -100, 45, True)
    my_go_to_pose3(robot, -100, -100, 45, True)
    my_go_to_pose3(robot, 0, -150, 45, True)


if __name__ == '__main__':
    cozmo.run_program(run)
