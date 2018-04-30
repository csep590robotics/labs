#!/usr/bin/env python3

import asyncio
import sys
import copy

import cv2
import numpy as np

import find_ball
import cozmo
from cozmo.util import degrees, speed_mmps, distance_mm

try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')


# Define a decorator as a subclass of Annotator; displays battery voltage
class BatteryAnnotator(cozmo.annotate.Annotator):
    def apply(self, image, scale):
        d = ImageDraw.Draw(image)
        bounds = (0, 0, image.width, image.height)
        batt = self.world.robot.battery_voltage
        text = cozmo.annotate.ImageText('BATT %.1fv' % batt, color='green')
        text.render(d, bounds)

# Define a decorator as a subclass of Annotator; displays the ball


class BallAnnotator(cozmo.annotate.Annotator):
    ball = None

    def apply(self, image, scale):
        d = ImageDraw.Draw(image)
        bounds = (0, 0, image.width, image.height)

        if BallAnnotator.ball is not None:
            # double size of bounding box to match size of rendered image
            BallAnnotator.ball = np.multiply(BallAnnotator.ball, 2)

            # define and display bounding box with params:
            #msg.img_topLeft_x, msg.img_topLeft_y, msg.img_width, msg.img_height
            box = cozmo.util.ImageBox(BallAnnotator.ball[0] - BallAnnotator.ball[2],
                                      BallAnnotator.ball[1] - BallAnnotator.ball[2],
                                      BallAnnotator.ball[2] * 2, BallAnnotator.ball[2] * 2)
            cozmo.annotate.add_img_box_to_image(image, box, "yellow", text=None)


async def run(robot: cozmo.robot.Robot):
    '''The run method runs once the Cozmo SDK is connected.'''

    # add annotators for battery level and ball bounding box
    robot.world.image_annotator.add_annotator('battery', BatteryAnnotator)
    # robot.world.image_annotator.add_annotator('ball', BallAnnotator)

    if robot.is_on_charger:
        await robot.drive_off_charger_contacts().wait_for_completed()
        await robot.drive_straight(distance_mm(300), speed_mmps(50)).wait_for_completed()
    await robot.set_head_angle(degrees(10)).wait_for_completed()
    await robot.set_lift_height(0.0).wait_for_completed()
    await robot.say_text('game is on').wait_for_completed()

    ball_found = False

    try:
        while True:
            event = await robot.world.wait_for(cozmo.camera.EvtNewRawCameraImage, timeout=30)
            opencv_image = cv2.cvtColor(np.asarray(event.image), cv2.COLOR_RGB2GRAY)

            ball = find_ball.find_ball(opencv_image, delta=50, minCircle=1, maxCircle=320)
            # BallAnnotator.ball = copy.copy(ball)
            print('ball: ', ball)

            if ball is None:
                if not ball_found:
                    await robot.turn_in_place(degrees(30)).wait_for_completed()
                    await robot.say_text('searching').wait_for_completed()
                elif ball_found:
                    print('hit the ball: ', ball)
                    await robot.say_text('Hit it').wait_for_completed()
                    await robot.drive_straight(distance_mm(150), speed_mmps(50), should_play_anim=False).wait_for_completed()
                    await robot.set_head_angle(degrees(180)).wait_for_completed()
                    await robot.play_anim_trigger(cozmo.anim.Triggers.FistBumpSuccess).wait_for_completed()
                    break
            else:
                robot.stop_all_motors()
                if not ball_found:
                    await robot.say_text('Found it').wait_for_completed()
                    ball_found = True

                h = opencv_image.shape[0]
                w = opencv_image.shape[1]
                if (ball[2] > 70):          #  Hit
                    await robot.say_text('Hit it').wait_for_completed()
                    await robot.drive_straight(distance_mm(150), speed_mmps(50), should_play_anim=False).wait_for_completed()
                    await robot.set_head_angle(degrees(180)).wait_for_completed()
                    await robot.play_anim_trigger(cozmo.anim.Triggers.FistBumpSuccess).wait_for_completed()
                    break
                elif (ball[0] > w / 5 * 3): #  Right
                    await robot.turn_in_place(degrees(-5)).wait_for_completed()
                elif (ball[0] < w / 5 * 2): #  Left
                    await robot.turn_in_place(degrees(5)).wait_for_completed()
                elif (ball[1] > h / 5 * 3): #  High
                    await robot.set_head_angle(degrees(robot.head_angle.degrees - 5)).wait_for_completed()
                elif (ball[1] < h / 5 * 2): #  Low
                    await robot.set_head_angle(degrees(robot.head_angle.degrees + 5)).wait_for_completed()
                else:
                    await robot.drive_straight(distance_mm(50), speed_mmps(50), should_play_anim=False).wait_for_completed()

    except KeyboardInterrupt:
        print("")
        print("Exit requested by user")
    except cozmo.RobotBusy as e:
        print("too many action for cozmo")
        print(e)


if __name__ == '__main__':
    cozmo.run_program(run, use_viewer=True, force_viewer_on_top=True)
