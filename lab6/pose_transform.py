#!/usr/bin/env python3

'''
This is starter code for Lab 6 on Coordinate Frame transforms.

'''

import asyncio
import cozmo
import numpy
import math
import time
from cozmo.util import degrees


def get_relative_pose(object_pose, reference_frame_pose):
    # Point R as Robot, Point C as Cube, x as world X axis, x' as robot X axis
    # tan(RCx) = (cube_y - robot_y) / (cube_x - robot_x)
    # theta = RCx = atan((cube_y - robot_y) / (cube_x - robot_x))
    # RCx' = robot_angle - RCx
    #
    # ==>
    #
    # related_x = cos(RCx') * sqrt((cube_y - robot_y)^2 + (cube_x - robot_x)^2)
    # related_y = -sin(RCx') * sqrt((cube_y - robot_y)^2 + (cube_x - robot_x)^2)
    cube_x = object_pose.position.x
    cube_y = object_pose.position.y
    cube_angle_z = object_pose.rotation.angle_z

    robot_x = reference_frame_pose.position.x
    robot_y = reference_frame_pose.position.y
    robot_angle_z = reference_frame_pose.rotation.angle_z

    if (cube_x != robot_x):
        theta = math.atan((cube_y - robot_y) / (cube_x - robot_x))
    else:
        if (cube_y > robot_y):
            theta = math.pi / 2
        elif (cube_y < robot_y):
            theta = -math.pi / 2

    angle = robot_angle_z.radians - theta
    newX = math.cos(angle) * math.sqrt((cube_y - robot_y) *
                                       (cube_y - robot_y) + (cube_x - robot_x) * (cube_x - robot_x))
    newY = -math.sin(angle) * math.sqrt((cube_y - robot_y) *
                                        (cube_y - robot_y) + (cube_x - robot_x) * (cube_x - robot_x))
    newAngle = cube_angle_z - robot_angle_z

    return cozmo.util.pose_z_angle(newX, newY, 0, angle_z=newAngle, origin_id=object_pose._origin_id)


def find_relative_cube_pose(robot: cozmo.robot.Robot):
    '''Looks for a cube while sitting still, prints the pose of the detected cube
    in world coordinate frame and relative to the robot coordinate frame.'''

    robot.move_lift(-3)
    robot.set_head_angle(degrees(0)).wait_for_completed()
    cube = None

    while True:
        try:
            cube = robot.world.wait_for_observed_light_cube(timeout=30)
            if cube:
                print(f"Robot pose: {robot.pose}")
                print(f"Cube pose: {cube.pose}")
                print(
                    f"Cube pose in the robot coordinate frame: {get_relative_pose(cube.pose, robot.pose)}")
        except asyncio.TimeoutError:
            print("Didn't find a cube")
        time.sleep(10)


if __name__ == '__main__':
    cozmo.run_program(find_relative_cube_pose)
