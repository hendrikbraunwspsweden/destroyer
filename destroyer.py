import sys, pygame
import datetime
from math import sin, cos, radians, pi
from time import sleep
import math

def project_point(original_x, original_y, bearing, distance):

    if bearing >= 360:
        bearing = bearing -360

    if bearing == 0:
        return [original_x, original_y - distance]
    if bearing == 90:
        return [original_x - distance, original_y]
    if bearing == 180:
        return [original_x, original_y + distance]
    if bearing == 270:
        return [original_x + distance, original_y]

    if 0 <= bearing < 90:
        angle = bearing
        move_x = sin(radians(angle))*distance
        move_y = cos(radians(angle))*distance
        return [original_x + move_x, original_y - move_y]

    if 90 <= bearing < 180:
        angle = bearing - 90
        move_x = cos(radians(angle))*distance
        move_y = sin(radians(angle))*distance
        return [original_x + move_x, original_y + move_y]

    if 180 <= bearing < 270:
        angle = bearing - 180
        move_x = sin(radians(angle))*distance
        move_y = cos(radians(angle))*distance
        return [original_x - move_x, original_y + move_y]

    if 270 <= bearing < 360:
        angle = bearing - 270
        move_x = cos(radians(angle))*distance
        move_y = sin(radians(angle))*distance
        return [original_x - move_x, original_y - move_y]


class Destroyer(object):
    __tower_direction = 0
    __image = None
    __reload_time = None
    __last_shot = None

    def __init__(self, type, reload_time):
        if type == 0:
            self.__image = "./media/warship.jpeg"

        self.__reload_time = reload_time

    def turn_tower(self, direction, steps):
        if direction == 1:
            if self.__tower_direction >=360:
                self.__tower_direction = self.__tower_direction - 360
            self.__tower_direction += steps

        if direction == 3:
            if self.__tower_direction <= 0:
                self.__tower_direction = self.__tower_direction + 360
            self.__tower_direction -= steps

    def set_reload_time(self, time):
        self.__reload_time = time

    def get_reload_time(self):
        return self.__reload_time

    def shoot(self):
        if self.__last_shot is None:
            self.__last_shot = datetime.datetime.now()
            return True
        else:
            delta = datetime.datetime.now() - self.__last_shot
            print(delta.total_seconds()*1000)
            if delta.total_seconds()*1000 > self.__reload_time:
                self.__last_shot = datetime.datetime.now()
                return True
            else:
                return False

    def get_image(self):
        return self.__image

    def get_direction(self):
        return self.__tower_direction

class Enemy(object):
    __type = None
    __strength = None
    __position = None
    __direction = 0

    def __init(self, type, strength):
        pass

    def get_position(self):
        return 0

    def move(self, direction, speed):
        pass

class Bullet(object):
    __type = None
    __power = None
    __position = []
    __direction = 0
    __old_time = None
    __px_per_second = None
    __original_time = None

    def __init__(self, type, power, origin, direction, px_per_second):
        self.__type = type
        self.__power = power
        self.__position = list(origin)
        self.__direction = direction
        self.__old_time = datetime.datetime.now()
        self.__px_per_second = px_per_second
        self.__original_time = datetime.datetime.now()

    def move(self):
        new_time = datetime.datetime.now()
        time_delta = new_time - self.__old_time
        self.__old_time = new_time
        vector_delta = math.floor(time_delta.total_seconds() * self.__px_per_second)
        self.__position = project_point(self.__position[0], self.__position[1], self.__direction, vector_delta)

    def get_position(self):
        return [int(math.floor(self.__position[0])), int(math.floor(self.__position[1]))]

    def __del__(self):
        print((datetime.datetime.now() - self.__original_time).total_seconds())

class Bullets(object):

    __bullet_list = []
    __origin = ()
    __window_size = ()

    def __init__(self, origin, window_size):
        self.__origin = origin
        self.__window_size = window_size

    def add_bullet(self, type, power, direction, speed):
        self.__bullet_list.append(Bullet(type, power, self.__origin, direction, speed))

    def move(self):
        pop_list = []
        for i in range(len(self.__bullet_list)):
            if self.__bullet_list[i].move() == -1:
                pop_list.append(i)

        for p in pop_list:
            self.__bullet_list.pop(p)

    def get_bullets(self):
        return self.__bullet_list

    def remove_bullets(self, indices):
        for i in indices:
            self.__bullet_list.pop(i)


class Destroyer_logic(object):

    __destroyer = None
    __enemies = []
    __bullets = []
    __window_size = 0

    def __init__(self, destroyer, enemies, bullets, window_size):
        self.__destroyer = destroyer
        self.__bullets = bullets
        self.__enemies = enemies
        self.__window_size = window_size

    def check(self):
        bullet_remove_list = []
        bullet_list = self.__bullets.get_bullets()

        for i in range(len(bullet_list)):
            if not (self.__window_size[0] >= bullet_list[i].get_position()[0] >= 0) or not (self.__window_size[1] >= bullet_list[i].get_position()[1] >= 0):
                bullet_remove_list.append(i)

        self.__bullets.remove_bullets(bullet_remove_list)

class Destroyer_gfx(object):
    __destroyer = None
    __bullets = None
    __enemies = None
    __screen = None

    def __init__(self, screen, destroyer, enemies, bullets):
        self.__destroyer = destroyer
        self.__enemies = enemies
        self.__bullets = bullets
        self.__screen = screen

    def draw(self):
        for b in self.__bullets.get_bullets():
            pygame.draw.circle(self.__screen, (255,255,255), b.get_position(), 5,1)

class Destroyer_game(object):

    __enemies = []
    __bullets = []
    __enemy_strenght = None
    __game_speed = None
    __max_enemies = 1
    __window_size = ()

    def __init__(self, window_size=(800,800), game_speed=1, max_enemies=1):
        self.__window_size = window_size
        self.__game_speed = game_speed
        self.__max_enemies = max_enemies

        pygame.init()
        screen = pygame.display.set_mode(window_size)
        destroyer = Destroyer(0,1000)
        bullets = Bullets((window_size[0]/2, window_size[1]/2), window_size)
        logic = Destroyer_logic(destroyer, None, bullets, window_size)
        graphics = Destroyer_gfx(screen, destroyer, None, bullets)

        exit_game = False

        while not exit_game:

            bullets.move()
            logic.check()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type is pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key == "escape":
                        exit_game = True

                    if key == "right":
                        destroyer.turn_tower(1,4)

                    if key == "left":
                        destroyer.turn_tower(3,4)

                    if key == "space":
                        if destroyer.shoot():
                            bullets.add_bullet(0,100, destroyer.get_direction(), 100)

            graphics.draw()
            pygame.display.update()
            sleep(0.01)
            #screen.fill(black)
            #screen.blit(ball, ballrect)
            #pygame.display.flip()


    def __del__(self):
        pass

if __name__ == "__main__":
    myGame = Destroyer_game()
