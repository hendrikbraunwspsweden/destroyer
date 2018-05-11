import pygame
import sys
from units import *
from gfx import *
from logic import *
from time import sleep

class Destroyer_game(object):

    def __init__(self, window_size=(1024,800), game_speed=1, max_enemies=3, enemy_wait_range=(2, 4)):
        self.__window_size = window_size
        self.__game_speed = game_speed
        self.__max_enemies = max_enemies
        self.__enemies = []
        self.__bullets = []
        self.__enemy_strenght = None
        self.__max_enemies = max_enemies
        self.__window_size = window_size

        pygame.init()
        destroyer = Destroyer(0,500, window_size)
        bullets = Bullets((window_size[0]/2, window_size[1]/2), window_size)
        enemies = Enemies(enemy_wait_range, max_enemies, window_size)
        fades = Fades()
        enemies.add_enemy()
        logic = Destroyer_logic(destroyer, enemies, bullets, fades, window_size)
        graphics = Destroyer_gfx(window_size, destroyer, enemies, bullets, fades, "./media/background.png")
        graphics.draw()

        exit_game = False

        while not exit_game:

            enemies.add_enemy()
            enemies.move()
            bullets.move()
            logic.check()
            fades.fade()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                destroyer.turn_tower(1,2)

            if keys[pygame.K_LEFT]:
                destroyer.turn_tower(3,2)

            if keys[pygame.K_SPACE]:
                if destroyer.shoot():
                    bullets.add_bullet(0,100, destroyer.get_direction(), 500)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type is pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key == "escape":
                        exit_game = True


            graphics.draw()
            sleep(0.005)
            #screen.fill(black)
            #screen.blit(ball, ballrect)
            #pygame.display.flip()


    def __del__(self):
        pass
