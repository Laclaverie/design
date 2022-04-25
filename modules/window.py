# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:08:45 2021

@author: Julien
"""

from multiprocessing import Queue, Process, Value

import cv2

from modules.captation import Captation
from modules.post_bdd import upload_on_firebase
from modules.print_layers import PrintLayers
from modules.variables import PICTURES_EXTENSION


def print_number(nb: int):
    """
    Open QR code image and add number corresponding to the current image.

    Parameters
    ----------
    nb : int
        Image number.

    Returns
    -------
    None.

    """

    # Load static QRCode image
    nb_img = cv2.imread("qrcode.png")

    # Add image number to make it dynamic.
    cv2.putText(
        nb_img,
        str(nb).zfill(6),
        (205, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        3
    )
    cv2.imshow("QR code", nb_img)

    # Set 15 sec timeout
    cv2.waitKey(15000)
    cv2.destroyAllWindows()


def start(files, step):
    """
    Start window to get user's movements and window to print layers.

    Parameters
    ----------
    files : array of strings
        Array containing all layers filenames.
    step : int
        Step used to sample speed.

    Returns
    -------
    None.

    """

    # Create queue to tranfer data between two processes.
    queue = Queue()

    # Initialize class to print layers.
    print_layers = PrintLayers(files, step, queue)

    # Initialize class to get user's hands movements.
    captation = Captation(queue)

    number = Value("i", 0, lock=False)

    # Start processes to print layers and to get user's hands movements from
    # a competitive way.
    captation_process = Process(target=captation.capture)
    print_layers_process = Process(target=print_layers.launch, args=[number])

    captation_process.start()
    print_layers_process.start()

    # Wait print layers process to terminate
    print_layers_process.join()

    # Terminate second process
    captation_process.terminate()

    # Upload on firebase DB
    upload_on_firebase(str(number.value).zfill(6) + PICTURES_EXTENSION)

    # Open picture to say picture number to user
    print_number(number.value)
