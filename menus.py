import pygame
import sys
from time import sleep
from gfx import blit_alpha
from sprite import Sprite


class Menu(object):
    _entries = {
        0:"",
        1:"",
        2:""
    }

    def paint(self):
        for key,item in self._entries_sprite_dict.iteritems():
            item.draw(self._screen)

    def __init__(self, screen, window_size, title, background, **kwargs):
        self._screen = screen
        self._title = title
        self._background = background
        self._entries_sprite_dict = {}

        self.__add_text = (kwargs["add_text"],None)
        entry_size_y = 20
        start_y = window_size[1]/2 - len(self._entries) * entry_size_y
        i = 0

        for key, item in self._entries.iteritems():
            print(item)
            sprite = Sprite.from_text(item)
            size=sprite.get_size()
            sprite.move_to(window_size[0]/2 - size[0]/2, start_y + i * entry_size_y)
            self._entries_sprite_dict.update({key:sprite})
            i += 1

    def show(self):
        option = 0
        max_option = max(self._entries.keys())

        exit = False
        sleep(0.5)

        while not exit:
            self.paint()

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
    _entries={
        0:"Settings",
        1:"Return to game",
        2:" ",
        3:"Exit game"
    }

    def __init__(self, screen, size, title, background, **kwargs):
        Menu.__init__(self,screen, size, title, background, **kwargs)

