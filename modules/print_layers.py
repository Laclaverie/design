"""

    Module containing class PrintLayers to print layers in a separated window
    from window captation.

"""
# pylint: disable=E1101

from math import cos, sin
from os import kill, getpid, listdir

import pygame

from modules.layer import Layers, Layer
from modules.variables import MAX_LAYERS, LOCAL_FOLDER, PICTURES_EXTENSION


def count_local_pictures():
    """
    Return the number of local pictures.

    Returns
    -------
    integer
        Number of local pictures.

    """

    return len(listdir(LOCAL_FOLDER))


class PrintLayers:
    """
    Class to print layers in window.

    Attributes
    ----------
    queue: Queue
        Queue used to transfer data between two processes in window.py
    layers: Layers
        Layers class to manage layer affectation.
    step: int
        Step used to sample speed.
    layer_files: array of string
        Array containing all layer filenames.
    size: array of int
        Window dimensions.
    screen: Screen
        Pygame object to stamp items such as layers.

    Methods
    -------
    reset_queue():
        Reset queue value.
    position(speed):
        Set position following speed data.
    from_speed_to_layers(values):
        Set a specific layer from speed values.
    launch(number):
        Start layers printing.

    """

    def __init__(self, files, step, queue):
        """
        Initialize window.

        Parameters
        ----------
        files : list of string
            List containing all files names in folder 'calques_individuels'.
        step : int
                Step used to implement layers and print layers. Step is used
                to sample speed and affect layer to speed sub-range.
        queue : Queue
            Same queue as in class to get movement. This queue allow to
            transfer data from two processes. Get data is this class.

        Returns
        -------
        None.

        """

        self.queue = queue
        self.layers = Layers()
        self.step = step
        self.layer_files = files
        self.size = None
        self.screen = None

    def position(self, speed):
        """
        Use data send by captation to return a specific position to print layer.

        Parameters
        ----------
        speed : dict
            Dictionnary containing speed data sent by captation class.

        Returns
        -------
        pos : array of int
            Position of layer in window.

        """

        speed_x = float(speed["speedX"])
        speed_y = float(speed["speedY"])
        pos = (
            (cos(speed_x) + sin(speed_y)) / 4 * self.size[0],
            (cos(speed_y) + sin(speed_x)) / 4 * self.size[1],
        )
        return pos

    def from_speed_to_layers(self, values):
        """
        Link layers generation to hand speed.

        Parameters
        ----------
        values : dict
            Dict in queue sent by cptation class.

        Returns
        -------
        None.

        """

        # Get last speed only or there will have to much layers.
        last_speed = values[len(values) - 1]
        # Sample speed
        for i in range(1, len(self.layer_files) + 1):
            # Get the highest sample value as possible
            if float(last_speed["speed"]["speed"]) < i * self.step:
                # Add layer to layer array
                self.layers.add(
                    Layer(
                        self.screen,
                        self.layer_files[i - 1],
                        self.position(last_speed["speed"]),
                        last_speed["direction"],
                    )
                )
                break

    def launch(self, number):
        """
        Start layers printing.

        Parameters
        ----------
        number: integer
            Shared variable with main process in window.py

        Returns
        -------
        None.

        """

        pygame.init()

        # Get screen size to maximize window
        info = pygame.display.Info()
        self.size = (info.current_w - 10, info.current_h - 50)
        self.screen = pygame.display.set_mode(self.size)

        try:
            while True:

                # Convert speed and directions to layers
                values = self.queue.get()
                if len(values) > 0:
                    self.from_speed_to_layers(values)
                    # Blit all layers
                    self.layers.blit()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        break

                if len(self.layers.layers) >= MAX_LAYERS:
                    break

                pygame.display.flip()

            # Affect image number to shared variable. This information is now
            # enable for window.py program.
            number.value = count_local_pictures()

            # Save picture on local folder
            pygame.image.save(self.screen, LOCAL_FOLDER + str(number.value).zfill(6) + PICTURES_EXTENSION)

            # Quit pygame
            pygame.quit()

            # Kill process to release resources
            kill(getpid(), 9)

        finally:
            pygame.quit()
            # Reset queue
            # self.reset_queue()
            kill(getpid(), 9)
