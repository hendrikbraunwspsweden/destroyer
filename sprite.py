import pygame
from gfx import blit_alpha
import units

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
            self._original_image = pygame.image.load(image)
        else:
            self._original_image = image
        self._image = self._original_image
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

    def rotate(self, degrees):
        center = self._image.get_rect().center
        self._image = pygame.transform.rotate(self._original_image, -degrees)
        self._rect = self._image.get_rect(center=center)
        self.__get_params()

    def reset_rotation(self):
        self._image = self._original_image
        self._rect = pygame.Rect(self._x,self._y,self._image.get_rect()[2], self._image.get_rect()[3])
        self.__get_params()

    def get_center(self):
        return self._rect.center

    def set_center(self, x,y):
        self._rect.center = (x,y)
        self.__get_params()

    def project(self, bearing, distance):
        new_center = units.project_point(self._rect.center[0], self._rect.center[1], bearing, distance)
        self.set_center(new_center[0], new_center[1])

    def extract_by_width(self, width):
        try:
            return self._image.subsurface(self._x,self._y,width,self._y_size)
        except:
            return self._image

    def extract_by_height(self, height):
        try:
            return self._image.subsurface(self._x,self._y,self._x_size,height)
        except:
            return self._image

    @classmethod
    def from_text(cls, text, x=0,y=0, font_name="Arial", font_size=20, color=(255,255,255)):
        myfont = pygame.font.SysFont(font_name, font_size)
        image = myfont.render(text, True, color)
        return Sprite(image, x,y)