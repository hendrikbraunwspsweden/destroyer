import pygame
from gfx import blit_alpha

class Sprite(object):

    def __get_params(self):
        self._x = self._rect[0]
        self._y = self._rect [1]
        self._x_size = self._rect[2]
        self._y_size = self._rect[3]
        self.__original_x_size = self._x_size
        self.__original_y_size = self._y_size

    def __init__(self, image, x=0,y=0):
        if isinstance(image, str):
            self._image = pygame.image.load(image)
        else:
            self._image = image
        self._rect = pygame.Rect(x,y,self._image.get_rect()[2], self._image.get_rect()[3])
        self.__get_params()

    def move_to(self, x, y):
        self._rect = pygame.Rect(x,y,self._x_size, self._y_size)
        self.__get_params()

    def move(self, delta_x, delta_y):
        self._rect = pygame.Rect(self._x + delta_x, self._y + delta_y, self._x_size, self._y_size)
        self.__get_params()

    def resize(self, size_x, size_y):
        self._image = pygame.transform.scale(self._image, (size_x, size_y))
        self._rect = self._image.get_rect()
        self.__get_params()

    def reset_size(self):
        self._image = pygame.transform.scale(self._image, (self.__original_x_size, self.__original_y_size))
        self._rect = self._image.get_rect()
        self.__get_params()

    def draw(self, screen, opacity=100):
        opacity = opacity * 2.55
        if opacity == 255:
            screen.blit(self._image, self._rect)
        else:
            blit_alpha(screen, self._image, self._rect, opacity)

    def get_image(self):
        return self._image

    def get_rect(self):
        return self._rect

    def get_size(self):
        return self._x_size, self._y_size

    def get_pos(self):
        return self._x, self._y

    def set_rect(self, rect):
        self._rect = rect

    @classmethod
    def from_text(cls, text, x=0,y=0, font_name="Arial", font_size=20, color=(255,255,255)):
        myfont = pygame.font.SysFont(font_name, font_size)
        image = myfont.render(text, True, color)
        return Sprite(image, x,y)