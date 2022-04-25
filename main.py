"""

    Main.

"""

import sys
import os
from screeninfo import get_monitors

from modules.load_layers import load
from modules.start_algo import StartAlgo
from modules.variables import SPEEDSCOPE
from modules.window import start

if __name__ == "__main__":

    # Add current folder to pythonpath if it is not in environment
    # variable
    if not os.getcwd() in sys.path:
        sys.path.append(os.getcwd())

    # Load all layers in folder "calques"
    fileLayers = load()

    # Calcul step between each layer.
    step = (SPEEDSCOPE[1] - SPEEDSCOPE[0]) / (len(fileLayers))

    screen_size = (get_monitors()[0].width, get_monitors()[0].height)

    begin = False
    begin = StartAlgo(screen_size).start()

    if begin:
        start(fileLayers, step)
