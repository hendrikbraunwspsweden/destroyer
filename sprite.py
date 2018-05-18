import pygame

class Sprite(object):
    def __init__(self, image, rect):
        self._image = image
        self._rect = rect
        self._x = rect[0]
        self._y = rect [1]
        self._x_size = rect[2]
        self._y_size = rect[3]

    def new_post(self, x, y):
        pass

    def move(self, delta_x, delta_y):
        pass

    def resize(self):
        pass

    def reset_size(self):
        pass