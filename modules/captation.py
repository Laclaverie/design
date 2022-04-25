"""

    Class used to get user's hands movements.
    ROI := Region Of Interest

"""
# pylint: disable=E1101
# pylint: disable=R1702

import argparse
# organize imports
import time
from collections import deque
from screeninfo import get_monitors
import cv2
import imutils
import numpy as np
from imutils.video import VideoStream

from modules.variables import EAST, WEST, NORTH, SOUTH, SPEEDSCOPE


class Captation:
    """
    Class to get speed from user's hand movements.

    Attributes
    ----------
    posR and posR : arrays of int
        position of the hand on the Right and left box
    speedValues : arrays of dict
        array witch contains speed, speed on the X axis and on the Y axis.
    bgL and bgR : grayscale image
        background for the Left and Right ROI (used in the background substraction)
    threshold_min and threshold_max : integer between 0 and 255.
        parameter of the threshold.


    ...

    Methods
    -------
    get_speed, get_speed_values,set_speed_values,segment,run_avg

    ...

    """

    def __init__(self, queue):
        self.posR = [0, 0]  # position of the right hand
        self.posL = [0, 0]  # position of the left hand
        self.speedValues = []
        self.bgR = None
        self.bgL = None
        self.threshold_min = 25
        self.threshold_max = 255

        self.queue = queue

    # Get hand speed
    def get_speed(self, position, initialTime, direction, side=1):
        """
        Get speed from user's hands.

        Parameters
        ----------
        position : dim-2 array
            Position of hands at the beginning of while iteration.
        initialTime : time
            Time at the beginning of while iteration.
        direction : string
            Region where movements stops (East, West ...).
        side : int, optional
            Left hand or right hand. The default is 1.

        Returns
        -------
        None.

        """

        if side == 1:
            position_used = self.posR  # calculation : right rectangle
        else:
            position_used = self.posL  # calculation : left rectangle

        # Get time diff and pos diff from the beginning of iteration
        dist = np.sqrt(
            pow(position[0] - position_used[0], 2)
            + pow(position[1] - position_used[1], 2)
        )

        timeDiff = time.time() - initialTime

        if timeDiff != 0.0:
            speedX = (position[0] - position_used[0]) / timeDiff
            speedY = (position[1] - position_used[1]) / timeDiff
            # Instant speed
            speed = dist / timeDiff
        else:
            speed = 0.0

        if side == 1:
            self.posR = position
        else:
            self.posL = position

        # Add speed to speed array if speed is finite and positive.
        if speed > SPEEDSCOPE[0] and speed < SPEEDSCOPE[1]:
            self.speedValues.append(
                {
                    "speed": {
                        "speed": str(speed),
                        "speedX": str(speedX),
                        "speedY": str(speedY),
                    },
                    "side": side,
                    "direction": direction,
                }
            )
            self.queue.put(self.speedValues)

    def get_speed_values(self, idx=None):
        """
        Get speed values attribute of this class.

        Parameters
        ----------
        idx: int
            Specific value to return.

        Returns
        -------
        Array of dict / dict
            Array containing all values needed to print layers.

        """

        if idx is not None:
            return self.speedValues[idx]
        else:
            return self.speedValues

    def set_speed_values(self, values):
        """
        Set speedValues attributes.

        Paremeters
        ----------
        values: array of dict
            Values to set.

        Returns
        -------
        None.

        """

        self.speedValues = values

    def segment(self, image, choice=1):
        """
        Segment an image by using background substraction of a grayscale image.

        Parameters
        ----------
        image : grayscale image
        choice : integer
            choice = 1 : right ROI, choice = 2 : left ROI
        Returns
        --------
        thresholded : binary image
        segmented : position [[x y]]
            the center of the objet in the image.

        """
        # find the absolute difference between background and current frame
        if choice == 1:
            background_used = self.bgR
        else:
            background_used = self.bgL
        diff = cv2.absdiff(background_used.astype("uint8"), image)

        # threshold the diff image so that we get the foreground
        thresholded = cv2.threshold(
            diff, self.threshold_min, self.threshold_max, cv2.THRESH_BINARY
        )[1]

        # get the contours in the thresholded image
        contours, hierarchy = cv2.findContours(
            thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        # return None, if no contours detected
        if len(contours) == 0:
            return
        else:
            # based on contour area, get the maximum contour which is the hand
            segmented = max(contours, key=cv2.contourArea)
            return (thresholded, segmented)

    # --------------------------------------------------
    # To find the running average over the background
    # --------------------------------------------------
    def run_avg(self, imageRight, imageLeft, aWeight):
        """
        Make the background ( used in the segment function ).

        Parameters
        -----------
        imageRight : grayscale image
            right ROI
        imageLeft : grayscale image
            left ROI
        aWeight : float
             weight used to make the background

        Returns
        -------
        None
        But initialise the attribute bgR and bgL
        """
        # initialize the background
        if self.bgL is None or self.bgR is None:
            self.bgR = imageRight.copy().astype("float")
            self.bgL = imageLeft.copy().astype("float")
            return
        # compute weighted average, accumulate it and update the background
        cv2.accumulateWeighted(imageRight, self.bgR, aWeight)
        cv2.accumulateWeighted(imageLeft, self.bgL, aWeight)

    # -----------------
    # MAIN FUNCTION
    # -----------------
    def capture(self):
        """
        This is the "main" function of this part of the program
        """
        # initialize weight for running average
        aWeight = 1 / 200
        screen_size = (get_monitors()[0].width, get_monitors()[0].height)
        # argument (for speed part ) and parse it :
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=32, help="max buffer size")
        args = vars(ap.parse_args())
        # initialize the list of tracked points, the frame counter,
        # and the coordinate deltas
        ptsR = deque(maxlen=args["buffer"])
        ptsL = deque(maxlen=args["buffer"])
        counterR = 0
        counterL = 0
        (dXR, dYR) = (0, 0)
        (dXL, dYL) = (0, 0)
        direction = ""
        # get the reference to the webcam
        camera = VideoStream(src=0).start()
        time.sleep(2.0)

        # region of interest (ROI) coordinates
        topR, rightR, bottomR, leftR = int((screen_size[1])*7/ 500), int((screen_size[0])*75 / 500), int((screen_size[1]) *25/ 50), int(screen_size[0]*95/500)  # right ROI
        topL, rightL, bottomL, leftL = int((screen_size[1])*7/ 500), int((screen_size[0])*10/ 500), int(screen_size[1] *25/ 50), int(screen_size[0]*30/500)  # left ROI

        # initialize num of frames
        num_frames = 0

        # keep looping, until interrupted
        while True:
            initialTime = time.time()
            # get the current frame
            frame = camera.read()

            # resize the frame
            frame = imutils.resize(frame, width=700)

            # flip the frame so that it is not the mirror view
            frame = cv2.flip(frame, 1)

            # clone the frame
            clone = frame.copy()
            clone = imutils.resize(clone, int(screen_size[0] / 5), int(screen_size[1] / 5))

            # get the height and width of the frame
            frame.shape[:2]

            # get the ROI
            roiR = frame[topR:bottomR, rightR:leftR]  # ROI -> Right
            roiL = frame[topL:bottomL, rightL:leftL]  # ROI -> Left
            # convert the roi to grayscale and blur it
            # ---------------------------
            # the code HERE can be improved
            grayR = cv2.cvtColor(roiR, cv2.COLOR_BGR2GRAY)  # RGB -> grayscale
            grayR = cv2.GaussianBlur(grayR, (7, 7), 0)  # blur to reduce accuracy
            grayL = cv2.cvtColor(roiL, cv2.COLOR_BGR2GRAY)  # RGB -> grayscale
            grayL = cv2.GaussianBlur(grayL, (7, 7), 0)  # blur to reduce accuracy
            # -------------------------------------------
            # to get the background, keep looking till a threshold is reached
            # so that our running average model gets calibrated
            if num_frames < 200:
                self.run_avg(grayR, grayL, aWeight)

            else:
                # segment the hand region
                handR = self.segment(grayR, choice=1)  # segmentation of the right ROI
                handL = self.segment(grayL, choice=2)  # segementation of the left ROI

                # check whether hand region is segmented
                # -----------------------------------------------------------
                # We should improve this part because if handR and if handR
                # are VERY similar (only if time okok)
                # ----------------------------------------------------------
                if handR is not None:
                    # if yes, unpack the thresholded image and
                    # segmented region
                    (thresholdedR, segmentedR) = handR  # segmented frame --> binary !
                    cnts = cv2.findContours(
                        thresholdedR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                    )
                    cnts = imutils.grab_contours(cnts)

                    centerR = None
                    if len(cnts) > 0:
                        # find the largest contour in the mask, then use
                        # it to compute the minimum enclosing circle and
                        # centroid
                        c = max(cnts, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        if M["m00"] != 0:
                            centerR = (
                                int(M["m10"] / M["m00"]),
                                int(M["m01"] / M["m00"]),
                            )
                        # only proceed if the radius meets a minimum size
                        if radius > 10:
                            # draw the circle and centroid on the frame,
                            # then update the list of tracked points
                            cv2.circle(
                                roiR, (int(x), int(y)), int(radius), (0, 255, 255), 2
                            )
                            cv2.circle(roiR, centerR, 5, (0, 0, 255), -1)
                            ptsR.appendleft(centerR)
                            # loop over the set of tracked points
                    for i in np.arange(1, len(ptsR)):
                        # if either of the tracked points are None, ignore
                        # them
                        if ptsR[i - 1] is None or ptsR[i] is None:
                            continue
                        # check to see if enough points have been accumulated in
                        # the buffer
                        if (
                                counterR >= 10 and i == 1 and len(ptsR) == args["buffer"]
                        ):  # pts[-10] is not None:
                            # compute the difference between the x and y
                            # coordinates and re-initialize the direction
                            # text variables
                            dXR = ptsR[-10][0] - ptsR[i][0]
                            dYR = ptsR[-10][1] - ptsR[i][1]
                            (dirX, dirY) = ("", "")
                            # ensure there is significant movement in the
                            # x-direction
                            if np.abs(dXR) > 20:
                                dirX = EAST if np.sign(dXR) == 1 else WEST
                            # ensure there is significant movement in the
                            # y-direction
                            if np.abs(dYR) > 20:
                                dirY = NORTH if np.sign(dYR) == 1 else SOUTH
                            # handle when both directions are non-empty
                            if dirX != "" and dirY != "":
                                direction = "{}-{}".format(dirY, dirX)
                            # otherwise, only one direction is non-empty
                            else:
                                direction = dirX if dirX != "" else dirY
                        # otherwise, compute the thickness of the line and
                        # draw the connecting lines
                        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                        cv2.line(roiR, ptsR[i - 1], ptsR[i], (0, 0, 255), thickness)
                    cv2.putText(
                        roiR,
                        direction,
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (0, 0, 255),
                        3,
                    )

                    # Get current position and current time to determine speed in iteration
                    position = [dXR, dYR]
                    # speed = self.getSpeed(position, initialTime, direction);
                    self.get_speed(position, initialTime, direction, side=1)

                    counterR += 1
                    # Get current position and current time to determine speed in iteration
                    positionR = [dXR, dYR]
                    # speed = self.getSpeed(position, initialTime, direction);
                    self.get_speed(positionR, initialTime, direction, side=1)
                    # draw the segmented region and display the frame
                    cv2.drawContours(
                        clone, [segmentedR + (rightR, topR)], -1, (0, 0, 255)
                    )  # for the right ROI
                    # cv2.imshow("Thesholded -> right", thresholdedR)#(uncomment only when testing this class, not the entire algorithm (be aware of queue))
                    # cv2.imshow("ROI->Right", roiR)# (uncomment only when testing this class, not the entire algorithm (be aware of queue))

                # Now the left Hand !
                # -----------------------------------------
                # This "if" should be improved by creating a "big" function
                # -----------------------------------------
                if handL is not None:
                    # if yes, unpack the thresholded image and
                    # segmented region
                    (thresholded, segmented) = handL  # segmented frame --> binary !
                    cnts = cv2.findContours(
                        thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                    )
                    cnts = imutils.grab_contours(cnts)

                    centerL = None
                    if len(cnts) > 0:
                        # find the largest contour in the mask, then use
                        # it to compute the minimum enclosing circle and
                        # centroid
                        c = max(cnts, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        M = cv2.moments(c)
                        if M["m00"] != 0:
                            centerL = (
                                int(M["m10"] / M["m00"]),
                                int(M["m01"] / M["m00"]),
                            )
                        # only proceed if the radius meets a minimum size
                        if radius > 10:
                            # draw the circle and centroid on the frame,
                            # then update the list of tracked points
                            cv2.circle(
                                roiL, (int(x), int(y)), int(radius), (0, 255, 255), 2
                            )
                            cv2.circle(roiL, centerL, 5, (0, 0, 255), -1)
                            ptsL.appendleft(centerL)
                            # loop over the set of tracked points
                    for i in np.arange(1, len(ptsL)):
                        # if either of the tracked points are None, ignore
                        # them
                        if ptsL[i - 1] is None or ptsL[i] is None:
                            continue
                        # check to see if enough points have been accumulated in
                        # the buffer
                        if (
                                counterL >= 10 and i == 1 and len(ptsL) == args["buffer"]
                        ):  # pts[-10] is not None:
                            # compute the difference between the x and y
                            # coordinates and re-initialize the direction
                            # text variables
                            dXL = ptsL[-10][0] - ptsL[i][0]
                            dYL = ptsL[-10][1] - ptsL[i][1]
                            (dirX, dirY) = ("", "")
                            # ensure there is significant movement in the
                            # x-direction
                            if np.abs(dXL) > 20:
                                dirX = EAST if np.sign(dXL) == 1 else WEST
                            # ensure there is significant movement in the
                            # y-direction
                            if np.abs(dYL) > 20:
                                dirY = NORTH if np.sign(dYL) == 1 else SOUTH
                            # handle when both directions are non-empty
                            if dirX != "" and dirY != "":
                                direction = "{}-{}".format(dirY, dirX)
                            # otherwise, only one direction is non-empty
                            else:
                                direction = dirX if dirX != "" else dirY
                        # otherwise, compute the thickness of the line and
                        # draw the connecting lines
                        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                        cv2.line(roiL, ptsL[i - 1], ptsL[i], (0, 0, 255), thickness)
                    cv2.putText(
                        roiL,
                        direction,
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (0, 0, 255),
                        3,
                    )

                    # Get current position and current time to determine speed in iteration
                    positionL = [dXL, dYL]
                    self.get_speed(positionL, initialTime, direction, side=2)

                    counterL += 1
                    # draw the segmented region and display the frame
                    cv2.drawContours(
                        clone, [segmented + (rightL, topL)], -1, (0, 0, 255)
                    )  # for the right ROI
                    # cv2.imshow("Thesholded->Left", thresholded) #(uncomment only when testing this class, not the entire algorithm (be aware of queue))
                    # cv2.imshow("ROI->Left", roiL) #(uncomment only when testing this class, not the entire algorithm(be aware of queue))

            # draw the segmented hand
            cv2.rectangle(
                clone, (leftR, topR), (rightR, bottomR), (0, 255, 0), 2
            )  # for the right ROI
            cv2.rectangle(
                clone, (leftL, topL), (rightL, bottomL), (0, 255, 0), 2
            )  # for the left ROI

            # increment the number of frames
            num_frames += 1

            # display the frame with segmented hand
            cv2.moveWindow("Video Feed", int(screen_size[0] / 3), int(screen_size[1] / 25))
            cv2.imshow("Video Feed", clone)

            # observe the keypress by the user
            keypress = cv2.waitKey(1) & 0xFF

            if keypress == ord("+"):
                self.threshold_min += 5
                print("threshold_min = ", self.threshold_min)
            if keypress == ord("-"):
                self.threshold_min -= 5
                print("threshold_min= ", self.threshold_min)
            if keypress == ord("z"):
                self.threshold_max += 5
                print("threshold_max = ", self.threshold_max)
            if keypress == ord("s"):
                self.threshold_max -= 5
                print("threshold_max = ", self.threshold_max)

            # Quit app if user clicked on red cross.
            if cv2.getWindowProperty("Video Feed", cv2.WND_PROP_AUTOSIZE) == -1:
                break

        # free up memory
        camera.stop()
        cv2.destroyAllWindows()
