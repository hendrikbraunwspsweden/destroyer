import pygame
import sys
from units import *
from gfx import *
from logic import *
from unit_handling import *
from time import sleep

class Destroyer_game(object):

    def __init__(self, window_size=(1024,800), game_speed=0, max_enemies=7, enemy_wait_range=(1, 3), font_size=22):
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
        destroyer = Destroyer(0,500, 500, window_size)
        bullets = Bullets((window_size[0]/2, window_size[1]/2), window_size)
        torpedos = Torpedos()
        enemies = Enemies(enemy_wait_range, max_enemies, torpedos, game_speed, window_size, font_size)
        fades = Fades()
        enemies.add_enemy()
        logic = Destroyer_logic(destroyer, enemies, bullets, torpedos, explosions, fades, texts, points, window_size)
        graphics = Destroyer_gfx(window_size, destroyer, enemies, bullets, torpedos, explosions, fades, texts, points,
                                 font_size, "./media/background.png")
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
