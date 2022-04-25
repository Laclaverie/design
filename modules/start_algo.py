"""

    Module to create a user friendly menu, to facilitate app using.

"""
import os.path
import time
import cv2
import imutils
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class StartAlgo:
    def __init__(self, size):
        self.seuil = 100
        self.TIMER = int(5)
        self.size = size

    def initImages(self):
        """
        This manage the instructions witch are shown at the screen.

        Parameters
        -------
        None

        Returns
        --------
        None
        """
        if not (os.path.isfile('../demarrage/Blank.png') and os.path.isfile(
                '../demarrage/acceuil.png') and os.path.isfile(
            '../demarrage/attention.png')):
            print("if ok")
            # if one of theses files is missing, create all
            wallpaper = 255 * np.ones((self.size[1], self.size[0], 3), np.uint8)
            cv2.imwrite("../demarrage/Blank.png", wallpaper)
            im = Image.open("../demarrage/Blank.png")
            print("open ok")
            im2 = Image.open("../demarrage/Blank.png")
            draw = ImageDraw.Draw(im)
            draw2 = ImageDraw.Draw(im2)
            font_acceuil = ImageFont.truetype("../demarrage/White On Black.ttf", 150)
            font_attention = ImageFont.truetype("../demarrage/MADE Evolve.otf", 100)
            print("font ok")
            draw.text((int(self.size[1] / 6), int(self.size[0] / 5)),
                      "Pour commencer, \n Veuillez Obstruer \n la camera", (225, 99, 29), font=font_acceuil,
                      align='center')
            draw2.text((int(self.size[1] / 3), int(self.size[0] / 8)),
                       "Maintenant reculez vous \n et placez vous\n entre les rectangles\n\n Attention! \n Ne rentrez pas \n dans les rectangles",
                       (225, 99, 29), font=font_attention, align='center')
            im.save("../demarrage/acceuil.png", "PNG")
            im2.save("../demarrage/attention.png")

    def start(self):
        """
        This manage the transition between the standby mode and the "active" mode of the program
        To start the active mode, the user should put his/her hand very close to the camera WITHOUT touching it.

        Parameters
        -----------
        None

        Returns
        ---------
        None
        """
        self.initImages()
        # initialisation
        cap = cv2.VideoCapture(0)
        print(cap)
        acceuil = mpimg.imread("../demarrage/acceuil.png")
        attention = mpimg.imread("../demarrage/attention.png")
        quitter = 0

        topR, rightR, bottomR, leftR = 50, 450, 500, 600  # right ROI
        topL, rightL, bottomL, leftL = 50, 70, 500, 200  # left ROI
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            print(frame)
            if ret:
                frame = cv2.flip(frame, 1)
                frame = imutils.resize(frame, int(self.size[0] / 5), int(self.size[1] / 5))
                # Our operations on the frame come here
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                moyenne = gray.mean()
                # print (moyenne)
                # Display the resulting frame
                cv2.namedWindow("acceuil", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("acceuil", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow("acceuil", acceuil)  # standby
                cv2.moveWindow("frame", int(self.size[0] / 3), int(self.size[1] / 25))
                cv2.imshow("frame", gray)

                if moyenne < self.seuil:
                    cv2.destroyWindow("acceuil")
                    cv2.imshow("attention", attention)  # instructions
                    quitter = 1
                if cv2.waitKey(1) & 0xFF == ord("q") or quitter == 1:
                    time.sleep(5)  # x seconds to not press the user
                    break
            prev = time.time()
            cv2.destroyWindow("attention")
            cv2.destroyWindow("frame")
            while self.TIMER >= 0:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                cv2.rectangle(
                    frame, (leftR, topR), (rightR, bottomR), (0, 255, 0), 2
                )  # for the right ROI
                cv2.rectangle(
                    frame, (leftL, topL), (rightL, bottomL), (0, 255, 0), 2
                )  # for the left ROI
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(
                    frame,
                    str(self.TIMER),  # show the timer in the screen
                    (250, 250),
                    font,
                    7,
                    (0, 255, 255),
                    4,
                    cv2.LINE_AA,
                )
                cv2.namedWindow("RGB", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("RGB", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow("RGB", frame)

                cv2.waitKey(125)
                cur = time.time()
                if cur - prev >= 1:
                    prev = cur
                    self.TIMER = self.TIMER - 1
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
        else:
            print("erreur ouverture")
        return True


if __name__ == "__main__":
    print("otto")
    StartAlgo([1920, 1080]).start()
