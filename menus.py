import pygame
import sys
from time import sleep
from gfx import blit_alpha


class Menu(object):
    __entries = {
        0:"",
        1:"",
        2:""
    }

    def paint(self):
        self.__screen.blit()

    def __init__(self, screen, title, background, **kwargs):
        self.__screen = screen
        self.__title = title
        self.__background = background

        self.__add_text = (kwargs["add_text"],None)

    def show(self):
        option = 0
        max_option = max(self.__entries.keys())

        exit = False
        sleep(0.5)

        while not exit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type is pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key == "down":
                        if not option == max_option:
                            option += 1
                        else:
                            option = 0

                    if key == "up":
                        if not option == 0:
                            option -= 1
                        else:
                            option = max_option

                    if key == "escape":
                        option = -1
                        exit = True

                    if key == "return":
                        exit = True

        return option

class Ingame_menu(Menu):
    __entries={
        0:"Settings",
        1:"Return to game",
        2:" ",
        3:"Exit game"
    }

    def __init__(self, screen, title, background, **kwargs):
        Menu.__init__(self,screen, title, background, **kwargs)

