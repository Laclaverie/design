# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 10:13:04 2020

@author: Julien
"""

import numpy as np
import pygame

from modules.variables import FOLDER, EAST, WEST, NORTH, SOUTH


class Layers:
    """
    Class to manage many layers.

    Attributes
    ----------
    layers: array of Layer
        A set of layers.

    Methods
    -------
    add(layer):
        Add layer to layer array.
    blit(layers_):
        Blit all layers on window. If arg is not none, blit specific layers.

    """

    def __init__(self):
        """
        Contructor.

        Parameters
        ----------

        """
        self.layers = np.array([]).tolist()

    def add(self, layer):
        """
        Add a unique layer to the layer array.

        Parameters
        ----------
        layer : Layer
            Layer to add.

        Returns
        -------
        bool
            Information if layer is added or not. Layer is not added if it
            is not unique.

        """

        if not layer in self.layers:
            self.layers.append(layer)
            return True
        return False

    def blit(self, layers_=None):
        """
        Blit all layers in layers array in pygame window.

        Parameters
        ----------
        layers_ : Array of Layer, optional
            Blit all layers in array. The default is None.

        Returns
        -------
        None.

        """

        if layers_ is None:
            layers_ = self.layers
        for i in layers_:
            if i in self.layers:
                i.blit()


class Layer:
    """
    Class to create a layer object.

    Attributes
    ----------
    screen: Screen
        Screen to attach layer (from pygame).
    file: string
        Layer name that corresponds to layer filename.
    image: Image
        Image loaded by pygame.
    position: Array of int
        Position of the layer on pygame window.

    Methods
    -------
    blit():
        Blit layer on screen.
    __eq__(o):
        Overload of == operator to know if layer is unique or not.

    """

    # Constructor
    def __init__(self, screen_, file_, position_, rotate_=""):
        """
        Constructor.

        Parameters
        ----------
        screen_ : Screen
            Screen to attach layer (from pygame).
        file_ : string
            Filenameof the layer file. It is layer's name too.
        position_ : Array of int
            Position of the layer on pygame window.
        rotate_ : string, optional
            Rotate layer following region of hand (South, West ...). The default is "".

        """

        self.screen = screen_
        self.file = file_
        self.image = pygame.image.load(FOLDER + self.file).convert_alpha()
        rotation = 0
        if rotate_ != "":
            if NORTH in rotate_:
                rotation += 90
            if SOUTH in rotate_:
                rotation -= 90
            if WEST in rotate_:
                rotation += 90
            if EAST in rotate_:
                rotation -= 90
            self.image = pygame.transform.rotate(self.image, rotation)
        self.position = position_

    def blit(self):
        """
        Blit layer on screen.

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        """

        self.screen.blit(self.image, self.position)

    def __eq__(self, o):
        """
        Overload of == operator to know if layer is unique or not.

        Parameters
        ----------
        o : Layer
            Layer to compare to self.

        Returns
        -------
        bool
            Is unique.

        """

        return bool((
                o.position == self.position
                and o.file == self.file
                and o.screen == self.screen
        ))
