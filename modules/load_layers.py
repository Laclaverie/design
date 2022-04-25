# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 09:48:37 2020

    Load all layers' filename.

@author: Julien
"""

from os import listdir
from os.path import isfile, join

from modules.variables import FOLDER


def load():
    """
    Load all layers' filename.

    Parameters
    ----------
    None.

    Returns
    -------
    array of strings
        Array containing all layers' filename.

    """

    files = []
    for file in listdir(FOLDER):
        if isfile(join(FOLDER, file)) and ".png" in file:
            files.append(file)
    return files
