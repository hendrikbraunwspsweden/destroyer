from gfx import *
import pygame

class Points(object):
    def __init__(self):
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

    def __init__(self, destroyer, enemies, bullets, torpedos, explosions, fades, points, window_size):
        self.__destroyer = destroyer
        self.__bullets = bullets
        self.__enemies = enemies
        self.__fades = fades
        self.__window_size = window_size
        self.__torpedos = torpedos
        self.__explosions = explosions
        self.__points = points

    def __check_bullets(self):
        bullet_remove_list = []
        bullet_list = self.__bullets.get_bullets()

        for i in range(len(bullet_list)):
            if not (self.__window_size[0] >= bullet_list[i].get_position()[0] >= 0) or not (self.__window_size[1] >= bullet_list[i].get_position()[1] >= 0):
                bullet_remove_list.append(i)
        return bullet_remove_list

    def __check_bullets_enemies(self):
        enemy_remove_list = []
        bullet_remove_list = []
        enemy_list = self.__enemies.get_enemies()
        bullet_list = self.__bullets.get_bullets()

        for b in range(len(bullet_list)):
            for e in range(len(enemy_list)):
                if bullet_list[b].get_image()[1].colliderect(enemy_list[e].get_image()[1]):
                    bullet_remove_list.append(b)
                    print(enemy_list[e].get_hp(), bullet_list[b].get_power())
                    if enemy_list[e].reduce_hp(bullet_list[b].get_power()):
                        enemy_remove_list.append(e)
                        self.__points.add_points(enemy_list[e].get_params()["points"])
                        self.__explosions.add_explosion(Explosion(bullet_list[b].get_position(), 20))
                        self.__fades.add_fade(enemy_list[e].get_image()[0], enemy_list[e].get_image()[1], 0.5)
        return bullet_remove_list, enemy_remove_list

    def __check_enemies(self):
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
        torpedos_remove_list = []
        torpedos = self.__torpedos.get_torpedos()
        destroyer_destroyed = False
        for i in range(len(self.__torpedos.get_torpedos())):
            rect = torpedos[i].get_rect()

            if torpedos[i].get_image()[1].colliderect(self.__destroyer.get_image()[1]):
                torpedos_remove_list.append(i)
                self.__explosions.add_explosion(Explosion(torpedos[i].get_position(), 20))
                print(self.__torpedos.get_torpedos()[i].get_damage())
                if self.__destroyer.reduce_hp(self.__torpedos.get_torpedos()[i].get_damage()):
                    destroyer_destroyed = True

            elif torpedos[i].get_direction() == 0:
                if rect[1] <= 0:
                    torpedos_remove_list.append(i)
            elif torpedos[i].get_direction() == 1:
                if rect[0] >= self.__window_size[0]:
                    torpedos_remove_list.append(i)
            elif torpedos[i].get_direction() == 2:
                if rect[1] > self.__window_size:
                    torpedos_remove_list.append(i)
            elif torpedos[i].get_direction() == 3:
                if rect[2] <= 0:
                    torpedos_remove_list.append(i)
        return torpedos_remove_list, destroyer_destroyed

    def __check_bullets_torpedos(self):
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
        return bullet_remove_list, torpedo_remove_list

    def check(self):

        bullet_remove_list_1 = self.__check_bullets()
        bullet_remove_list_2, enemy_remove_list_1 = self.__check_bullets_enemies()
        enemy_remove_list_2 = self.__check_enemies()
        torpedo_remove_list_1, destroyer_destroyed = self.__check_torpedos()
        bullet_remove_list_3, torpedo_remove_list_2 = self.__check_bullets_torpedos()

        bullet_remove_list = list(set(bullet_remove_list_1 + bullet_remove_list_2 + bullet_remove_list_3))
        enemy_remove_list = list(set(enemy_remove_list_1 + enemy_remove_list_2))
        torpedo_remove_list = list(set(torpedo_remove_list_1 + torpedo_remove_list_2))

        self.__bullets.remove_bullets(bullet_remove_list)
        self.__enemies.remove_enemies(enemy_remove_list)
        self.__torpedos.remove_torpedos(torpedo_remove_list)

        if len(self.__enemies.get_enemies()) == 0:
            self.__enemies.add_enemy()

        if destroyer_destroyed:
            return True
        else:
            return False

