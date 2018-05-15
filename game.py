########################################################################################################################
# Destroyer - a small boat shooter game.                                                                               #
# Copyright (C) 2018 by Hendrik Braun                                                                                  #
#                                                                                                                      #
# This program is free software: you can redistribute it and/or modify it under the terms of the                       #
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or         #
# (at your option) any later version.                                                                                  #
#                                                                                                                      #
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied   #
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more        #
# details.                                                                                                             #
#                                                                                                                      #
# You should have received a copy of the GNU General Public License along with this program.                           #
# If not, see <http://www.gnu.org/licenses/>.                                                                          #
########################################################################################################################


import pygame
import sys
from units import *
from gfx import *
from logic import *
from unit_handling import *
from time import sleep

class Game_level(object):
    def __init__(self, init_level=0):
        self.__game_level = init_level

    def increase(self):
        self.__game_level += 1

    def get_level(self):
        return self.__game_level

class Destroyer_game(object):
    """
    The following dictionaries give the game level dependend variable values for game level brakes, maximum enemies
    and enemy wait ranges. Game level breaks define how many enemies the player has to sink before going to the next
    level. Max enemies defines the maximum number of enemies per game level. Enemy wait time ranges define the wait
    time interval in seconds that is used when spawning the next enemy.
    """
    __game_level_breaks = {
        0:5,
        1:5,
        2:5,
        3:5,
        4:20,
        5:20,
        6:20,
        7:20,
        8:20,
        9:20
    }

    __max_enemies = {
        0:1,
        1:15,
        2:5,
        3:5,
        4:5,
        5:5,
        6:5,
        7:5,
        8:5,
        9:5
    }

    __enemy_wait_time_ranges = {
        0:(1,3),
        1:(1,3),
        2:(1,3),
        3:(3,7),
        4:(3,7),
        5:(3,7),
        6:(3,7),
        7:(3,7),
        8:(3,7),
        9:(3,7),
    }

    def __init__(self, window_size=(1024,800), init_game_level=0, font_size=16):
        """
        Main class for the game creating and managing all game object class instances.

        :param window_size      : window size as x,y
        :param init_game_level  : the initial game level
        :param enemy_wait_range : range of spawn waiting times between enemies in seconds
        :param font_size        : font size for HUD
        :type window_size       : set
        :type init_game_level   : set
        :type font_size         : int

        :returns:
        """
        self.__window_size = window_size
        self.__enemies = []
        self.__bullets = []
        self.__enemy_strenght = None
        self.__font_size = font_size
        self.__total_enemies = 0
        self.__max_level = max(self.__game_level_breaks.keys())
        self.__next_level_in = self.__game_level_breaks[init_game_level]
        self.__max_enemies_ff = self.__max_enemies[init_game_level]
        self.__wait_time_range = self.__enemy_wait_time_ranges[init_game_level]

        pygame.init()
        pygame.font.init()
        game_level = Game_level(init_game_level)
        points = Points()
        texts = Texts()
        explosions = Explosions()
        destroyer = Destroyer(0,500, 5000, self.__window_size)
        bullets = Bullets((self.__window_size[0]/2, self.__window_size[1]/2), self.__window_size)
        torpedos = Torpedos()
        crates = Crates(self.__window_size, self.__font_size + 20, destroyer, game_level)
        enemies = Enemies(self.__wait_time_range, self.__max_enemies_ff, torpedos, crates, game_level,
                          self.__window_size, font_size)
        crates.set_enemies(enemies)
        fades = Fades()
        enemies.add_enemy()
        logic = Destroyer_logic(destroyer, enemies, bullets, torpedos, explosions, fades, texts, points, crates,
                                self.__window_size)
        graphics = Destroyer_gfx(window_size, destroyer, enemies, bullets, torpedos, explosions, fades, texts, points,
                                 crates, game_level, font_size, "./media/background.png")

        graphics.draw()
        exit_game = False


        while not exit_game:

            #Level handling
            if enemies.get_sunk_count() == self.__next_level_in:
                if game_level.get_level() < self.__max_level:
                    game_level.increase()
                    enemies.reset_sunk_count()
                    enemies.set_max_enemies(self.__max_enemies[game_level.get_level()])
                    enemies.set_wait_time_range(self.__enemy_wait_time_ranges[game_level.get_level()])
                    self.__next_level_in = self.__game_level_breaks[game_level.get_level()]
                    texts.add_text((window_size[0]/2, window_size[1]/2), "LEVEL UP!", font_size=20, positive=True)


            enemies.add_enemy()
            enemies.move()
            enemies.shoot()
            torpedos.move()
            bullets.move()
            explosions.change_frames()
            fades.fade()
            texts.move()
            crates.make_crate()
            crates.check()

            self.__total_enemies = enemies.get_total_enemies()

            if logic.check():
                sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                destroyer.turn_tower(1,2)

            if keys[pygame.K_LEFT]:
                destroyer.turn_tower(3,2)

            if keys[pygame.K_SPACE]:
                if destroyer.shoot():
                    bullets.add_bullet(0,100, destroyer.get_direction(), 800)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type is pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key == "escape":
                        exit_game = True


            graphics.draw()
            #sleep(0.005)
            #screen.fill(black)
            #screen.blit(ball, ballrect)
            #pygame.display.flip()


    def __del__(self):
        pass
