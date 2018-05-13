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

class Destroyer_game(object):

    def __init__(self, window_size=(1024,800), game_speed=0, max_enemies=5, enemy_wait_range=(5, 8), font_size=16):
        self.__window_size = window_size
        self.__game_speed = game_speed
        self.__max_enemies = max_enemies
        self.__enemies = []
        self.__bullets = []
        self.__enemy_strenght = None
        self.__max_enemies = max_enemies
        self.__window_size = window_size
        self.__font_size = font_size


        pygame.init()
        pygame.font.init()
        points = Points()
        texts = Texts()
        explosions = Explosions()
        destroyer = Destroyer(0,500, 5000, window_size)
        bullets = Bullets((window_size[0]/2, window_size[1]/2), window_size)
        torpedos = Torpedos()
        crates = Crates(self.__window_size, self.__font_size + 20, destroyer)
        enemies = Enemies(enemy_wait_range, max_enemies, torpedos, crates, game_speed, window_size, font_size)
        crates.set_enemies(enemies)
        fades = Fades()
        enemies.add_enemy()
        logic = Destroyer_logic(destroyer, enemies, bullets, torpedos, explosions, fades, texts, points, crates,
                                window_size)
        graphics = Destroyer_gfx(window_size, destroyer, enemies, bullets, torpedos, explosions, fades, texts, points,
                                 crates, font_size, "./media/background.png")
        graphics.draw()
        exit_game = False

        while not exit_game:
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
