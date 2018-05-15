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


from gfx import *
import pygame

class Points(object):
    def __init__(self):
        """
        # Class for handling game points.
        """
        self.__points = 0

    def add_points(self, points):
        self.__points += points

    def reduce_points(self, points):
        if self.__points >= 0 + points:
            self.__points -= points
        else:
            self.__points = 0

    def get_points(self):
        return self.__points

class Destroyer_logic(object):

    def __init__(self, destroyer, enemies, bullets, torpedos, explosions, fades, texts, points, crates, window_size):

        """
         This is where all the game logic magic happens. Takes the instances of the different game objects and checks
         for e.g. collisions. Defines what happens when collisions are detected.
         destroyer (Destroyer)     : game instance of destroyer class
         enemies (Enemies)         : game instance of enemies class
         bullets (Bullets)         : game instance of bullets class
         torpedos (Torpedos)       : game instance of torpedos class
         explosions (Explosions)   : game instance of Explosions class
         fades (Fades)             : game instance of Fades class
         texts (Texts)             : game instance of Texts class
         points (Points)           : game instance of points class
         crates (Crates)           : game instance of crates class
         window_size (list of int) : window size as x(int), y(int)
        """

        self.__destroyer = destroyer
        self.__bullets = bullets
        self.__enemies = enemies
        self.__fades = fades
        self.__window_size = window_size
        self.__torpedos = torpedos
        self.__explosions = explosions
        self.__points = points
        self.__texts = texts
        self.__crates = crates

    def __check_bullets(self):

        """
         Checks if any of the bullets are outside the game window. Returns a list of indices for the bullets that are
         to be removed.
        """
        bullet_remove_list = []
        bullet_list = self.__bullets.get_bullets()

        for i in range(len(bullet_list)):
            if not (self.__window_size[0] >= bullet_list[i].get_position()[0] >= 0) or \
                    not (self.__window_size[1] >= bullet_list[i].get_position()[1] >= 0):
                bullet_remove_list.append(i)
        return bullet_remove_list

    def __check_bullets_enemies(self):
        """
         Checks for collisions between bullets and enemies and what happens in that case. Returns list of bullets and
         enemies that are to be removed.
        """
        enemy_remove_list = []
        bullet_remove_list = []
        enemy_list = self.__enemies.get_enemies()
        bullet_list = self.__bullets.get_bullets()

        for b in range(len(bullet_list)):
            for e in range(len(enemy_list)):
                if bullet_list[b].get_image()[1].colliderect(enemy_list[e].get_image()[1]):
                    bullet_remove_list.append(b)
                    self.__explosions.add_explosion(Explosion(bullet_list[b].get_position(), 20))
                    if enemy_list[e].reduce_hp(bullet_list[b].get_power()):
                        enemy_remove_list.append(e)
                        self.__points.add_points(enemy_list[e].get_params()["points"])
                        self.__fades.add_fade(enemy_list[e].get_image()[0], enemy_list[e].get_image()[1], 0.5)
                        self.__texts.add_text(bullet_list[b].get_position(), "+{}".
                                              format(enemy_list[e].get_params()["points"]))
        return bullet_remove_list, enemy_remove_list

    def __check_enemies(self):
        """
         Checks if any of the enemies are outside the game window. Returns a list of enemies that are to be removed
        """
        enemies_remove_list = []
        enemies = self.__enemies.get_enemies()
        for i in range(len(self.__enemies.get_enemies())):
            rect = enemies[i].get_rect()

            if enemies[i].get_direction() == 0:
                if rect[1] <= 0:
                    enemies_remove_list.append(i)
                    self.__points.reduce_points(enemies[i].get_params()["points"]/2)

            if enemies[i].get_direction() == 1:
                if rect[0] >= self.__window_size[0]:
                    enemies_remove_list.append(i)
                    self.__points.reduce_points(enemies[i].get_params()["points"]/2)

            if enemies[i].get_direction() == 2:
                if rect[1] > self.__window_size:
                    enemies_remove_list.append(i)
                    self.__points.reduce_points(enemies[i].get_params()["points"]/2)

            if enemies[i].get_direction() == 3:
                if rect[2] <= 0:
                    enemies_remove_list.append(i)
                    self.__points.reduce_points(enemies[i].get_params()["points"]/2)
        return enemies_remove_list

    def __check_torpedos(self):
        """
         Checks if any of the torpedos are outside the game window. Returns a list of torpedos that are to be removed
        """
        torpedos_remove_list = []
        torpedo_list = self.__torpedos.get_torpedos()
        destroyer_destroyed = False
        for i in range(len(self.__torpedos.get_torpedos())):
            rect = torpedo_list[i].get_rect()

            if torpedo_list[i].get_image()[1].colliderect(self.__destroyer.get_image()[1]):
                torpedos_remove_list.append(i)
                self.__explosions.add_explosion(Explosion(torpedo_list[i].get_position(), 20))
                self.__texts.add_text(torpedo_list[i].get_position(), "-{}".
                                      format(torpedo_list[i].get_params()["points"]), positive = False)
                if self.__destroyer.reduce_hp(self.__torpedos.get_torpedos()[i].get_damage()):
                    destroyer_destroyed = True

            elif torpedo_list[i].get_direction() == 0:
                if rect[1] <= 0:
                    torpedos_remove_list.append(i)
            elif torpedo_list[i].get_direction() == 1:
                if rect[0] >= self.__window_size[0]:
                    torpedos_remove_list.append(i)
            elif torpedo_list[i].get_direction() == 2:
                if rect[1] > self.__window_size:
                    torpedos_remove_list.append(i)
            elif torpedo_list[i].get_direction() == 3:
                if rect[2] <= 0:
                    torpedos_remove_list.append(i)
        return torpedos_remove_list, destroyer_destroyed

    def __check_bullets_torpedos(self):

        """
         Checks for collisions between bullets and torpedos and what happens in that case. Returns list of bullets
         torpedos that are to be removed.
        """

        torpedo_remove_list = []
        bullet_remove_list = []
        torpedo_list = self.__torpedos.get_torpedos()
        bullet_list = self.__bullets.get_bullets()

        for b in range(len(bullet_list)):
            for e in range(len(torpedo_list)):
                if bullet_list[b].get_image()[1].colliderect(torpedo_list[e].get_image()[1]):
                    bullet_remove_list.append(b)
                    torpedo_remove_list.append(e)
                    self.__points.add_points(torpedo_list[e].get_params()["points"])
                    self.__explosions.add_explosion(Explosion(bullet_list[b].get_position(), 20))
                    self.__fades.add_fade(torpedo_list[e].get_image()[0], torpedo_list[e].get_image()[1], 0.5)
                    self.__texts.add_text(bullet_list[b].get_position(), "+{}".
                                          format(torpedo_list[e].get_params()["points"]))
        return bullet_remove_list, torpedo_remove_list

    def __check_bullets_crates(self):

        """
         Checks for collisions between bullets and crates and what happens in that case. Returns list of bullets and
         crates that are to be removed.
        """

        bullet_remove_list = []
        crate_remove_list = []
        bullet_list = self.__bullets.get_bullets()
        crate_list = self.__crates.get_crates()

        for b in range(len(bullet_list)):
            for c in range(len(crate_list)):
                if bullet_list[b].get_image()[1].colliderect(crate_list[c].get_rect()):
                    bullet_remove_list.append(b)
                    crate_remove_list.append(c)
                    self.__points.add_points(crate_list[c].get_points())
                    self.__explosions.add_explosion(Explosion(bullet_list[b].get_position(), 20))
                    if crate_list[c].get_type() == 0:
                        self.__destroyer.increase_hp(crate_list[c].get_effect_points())
                        self.__texts.add_text(bullet_list[b].get_position(), "+{}hp".
                                              format(crate_list[c].get_effect_points()))
        return bullet_remove_list, crate_remove_list

    def __check_enemies_crates(self):

        """
         Checks for collisions between enemies and crates and what happens in that case. Returns list of crates that
         are to be removed.
        """
        crates_remove_list = []
        crate_list = self.__crates.get_crates()
        enemies_list = self.__enemies.get_enemies()
        for e in range(len(self.__enemies.get_enemies())):
            for c in range(len(crate_list)):
                if enemies_list[e].get_rect().colliderect(crate_list[c].get_rect()):
                    crates_remove_list.append(c)
        return crates_remove_list

    def check(self):

        """
         Runs the collision check functions above. The returned lists containing the list indices of the objects that
         are to be deleted are combined per object type. The lists are then "destilled" down to unique indices in
         order to prevent double entries leading to problems during removal. Calls the remove methods for each object
         type with the "destilled" list as argument. Spawns a new enemy in case all enemies are gone.
        """

        bullet_remove_list_1 = self.__check_bullets()
        bullet_remove_list_2, enemy_remove_list_1 = self.__check_bullets_enemies()
        enemy_remove_list_2 = self.__check_enemies()
        torpedo_remove_list_1, destroyer_destroyed = self.__check_torpedos()
        bullet_remove_list_3, torpedo_remove_list_2 = self.__check_bullets_torpedos()
        bullet_remove_list_4, crate_remove_list_1 = self.__check_bullets_crates()
        crate_remove_list_2 = self.__check_enemies_crates()

        bullet_remove_list = list(set(bullet_remove_list_1 + bullet_remove_list_2 + bullet_remove_list_3 +
                                      bullet_remove_list_4))
        enemy_remove_list = list(set(enemy_remove_list_1 + enemy_remove_list_2))
        torpedo_remove_list = list(set(torpedo_remove_list_1 + torpedo_remove_list_2))
        crate_remove_list = list(set(crate_remove_list_1 + crate_remove_list_2))

        self.__bullets.remove_bullets(bullet_remove_list)
        self.__enemies.remove_enemies(enemy_remove_list)
        self.__torpedos.remove_torpedos(torpedo_remove_list)
        self.__crates.remove_crates(crate_remove_list)

        if len(self.__enemies.get_enemies()) == 0:
            self.__enemies.add_enemy()

        if destroyer_destroyed:
            return True
        else:
            return False

