#!/usr/bin/env python3

import asyncio
import sys

import cv2
import numpy as np

sys.path.insert(0, '../lab4')
import find_ball

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
try:
    from PIL import ImageDraw, ImageFont
except ImportError:
    sys.exit('run `pip3 install --user Pillow numpy` to run this example')

from enum import Enum

class BotState(Enum):
	SEARCHING = 1
	HUNTING = 2
	HITTING = 3

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

            #double size of bounding box to match size of rendered image
            BallAnnotator.ball = np.multiply(BallAnnotator.ball,2)

            #define and display bounding box with params:
            #msg.img_topLeft_x, msg.img_topLeft_y, msg.img_width, msg.img_height
            box = cozmo.util.ImageBox(BallAnnotator.ball[0]-BallAnnotator.ball[2],
                                      BallAnnotator.ball[1]-BallAnnotator.ball[2],
                                      BallAnnotator.ball[2]*2, BallAnnotator.ball[2]*2)
            cozmo.annotate.add_img_box_to_image(image, box, "green", text=None)

            BallAnnotator.ball = None


async def run(robot: cozmo.robot.Robot):
    '''The run method runs once the Cozmo SDK is connected.'''

    #add annotators for battery level and ball bounding box
    robot.world.image_annotator.add_annotator('battery', BatteryAnnotator)
    robot.world.image_annotator.add_annotator('ball', BallAnnotator)

    currentState = BotState.SEARCHING
    cameraFOV = [60,60];
    Kp = [0.25, 0.01]
    baseTranslationSpeed = 13
    radiusThreshold = 125
    try:
        while True:
            #get camera image
            event = await robot.world.wait_for(cozmo.camera.EvtNewRawCameraImage, timeout=30)

            #convert camera image to opencv format
            opencv_image = cv2.cvtColor(np.asarray(event.image), cv2.COLOR_RGB2GRAY)

            #find the ball
            ball = find_ball.find_ball(opencv_image)

            #set annotator ball
            BallAnnotator.ball = ball

            
            if(currentState is BotState.SEARCHING):
                if(ball is not None):
                    currentState = BotState.HUNTING
                else:
                    await robot.set_lift_height(1.0).wait_for_completed()
                    await robot.set_head_angle(cozmo.util.Angle(degrees=0.0)).wait_for_completed()
                    await robot.drive_wheels(int(baseTranslationSpeed), int(-1.0 * baseTranslationSpeed))
            elif(currentState is BotState.HUNTING):
                if(ball is not None):
                    imageSizePixels = [320, 240]
                    errorPixels = [(imageSizePixels[0] / 2) - ball[0], (imageSizePixels[1] / 2) - ball[1]]
                    errorNormalizedLinearDegrees = [(errorPixels[0] / (imageSizePixels[0] / 2)) * cameraFOV[0], (errorPixels[1] / (imageSizePixels[1] / 2)) * cameraFOV[1]]
                    proportionalComponent = [errorNormalizedLinearDegrees[0] * Kp[0], errorNormalizedLinearDegrees[1] * Kp[1]]
                    
                    robot.move_head(proportionalComponent[1])
                    await robot.drive_wheels(int(baseTranslationSpeed - proportionalComponent[0]), int(baseTranslationSpeed + proportionalComponent[0]))
                    print('cur radius:' + str(ball[2]))
                    if(ball[2] > radiusThreshold):
                        robot.stop_all_motors()
                        currentState = BotState.HITTING
                else:
                    robot.stop_all_motors()
                    currentState = BotState.SEARCHING
            elif(currentState is BotState.HITTING):
                await robot.set_lift_height(0.0).wait_for_completed()
                await robot.set_lift_height(1.0).wait_for_completed()
                currentState = BotState.SEARCHING
            print(str(currentState))

            ## TODO: ENTER YOUR SOLUTION HEREx


    except KeyboardInterrupt:
        print("")
        print("Exit requested by user")
    except cozmo.RobotBusy as e:
        print(e)



if __name__ == '__main__':
    cozmo.run_program(run, use_viewer = True, force_viewer_on_top = True)

