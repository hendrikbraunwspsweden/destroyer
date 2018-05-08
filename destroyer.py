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

    def __init__(self, type, reload_time, window_size):
        self.__tower_direction = 0
        self.__image = None
        self.__reload_time = None
        self.__last_shot = None
        self.__window_size = window_size
        print(self.__window_size)

        if type == 0:
            self.__image_size = (282,35)
            self.__rect = pygame.Rect(self.__window_size[0]/2 - self.__image_size[0]/2,
                self.__window_size[1]/2 - self.__image_size[1]/2,
                self.__image_size[0], self.__image_size[1])
            self.__image = pygame.image.load("./media/warship.png")

            self.__tower_rect = pygame.Rect(self.__window_size[0]/2 - 5, self.__window_size[1]/2 - 5, 10, 10)

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

    def get_image(self):
        return self.__image, self.__rect

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

    def get_direction(self):
        return self.__tower_direction

class Enemy(object):

    def __init(self, type, strength):
        self.__type = None
        self.__strength = None
        self.__position = None
        self.__direction = 0

    def get_position(self):
        return 0

    def move(self, direction, speed):
        pass

class Bullet(object):

    def __init__(self, type, power, origin, direction, px_per_second):
        self.__type = type
        self.__power = power
        self.__position = list(origin)
        self.__direction = direction
        self.__old_time = datetime.datetime.now()
        self.__px_per_second = px_per_second
        self.__original_time = datetime.datetime.now()
        self.__image = None
        self.__image_size = (6,23)
        self.__rect = pygame.Rect(self.__position[0]-self.__image_size[0]/2, self.__position[1] - self.__image_size[1]/2, 20, 30)

        if type == 0:
            self.__image = pygame.image.load("./media/bullet1.png")
            loc = self.__image.get_rect().center
            self.__image = pygame.transform.rotate(self.__image, -self.__direction)
            self.__image.get_rect().center = loc

    def move(self):
        new_time = datetime.datetime.now()
        time_delta = new_time - self.__old_time
        self.__old_time = new_time
        vector_delta = math.floor(time_delta.total_seconds() * self.__px_per_second)
        self.__position = project_point(self.__position[0], self.__position[1], self.__direction, vector_delta)
        self.__rect.x = self.__position[0] - self.__image_size[0]/2
        self.__rect.y = self.__position[1] - self.__image_size[1]/2

    def get_position(self):
        return [int(math.floor(self.__position[0])), int(math.floor(self.__position[1]))]

    def __del__(self):
        print((datetime.datetime.now() - self.__original_time).total_seconds())

    def get_image(self):
        return self.__image, self.__rect

class Bullets(object):

    def __init__(self, origin, window_size):
        self.__origin = origin
        self.__window_size = window_size
        self.__bullet_list = []

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

    def __init__(self, window_size, destroyer, enemies, bullets, bg_image):
        self.__destroyer = destroyer
        self.__enemies = enemies
        self.__bullets = bullets
        self.__screen = pygame.display.set_mode(window_size)
        self.__background_path = bg_image
        self.__window_size = window_size
        self.make_background()

    def make_background(self):
        self.__background = pygame.image.load(self.__background_path)
        self.__background = pygame.transform.scale(self.__background, (self.__window_size[0], self.__window_size[1]))
        self.__background_rect = self.__background.get_rect()
        self.__background_rect.left, self.__background_rect.top = [0,0]

    def draw(self):
        self.__screen.blit(self.__background, self.__background_rect)
        self.__screen.blit(self.__destroyer.get_image()[0], self.__destroyer.get_image()[1])
        for b in self.__bullets.get_bullets():
            self.__screen.blit(b.get_image()[0], b.get_image()[1])
        pygame.display.flip()


class Destroyer_game(object):

    def __init__(self, window_size=(1024,800), game_speed=1, max_enemies=1):
        self.__window_size = window_size
        self.__game_speed = game_speed
        self.__max_enemies = max_enemies
        self.__enemies = []
        self.__bullets = []
        self.__enemy_strenght = None
        self.__max_enemies = max_enemies
        self.__window_size = window_size

        pygame.init()
        destroyer = Destroyer(0,100, window_size)
        bullets = Bullets((window_size[0]/2, window_size[1]/2), window_size)
        logic = Destroyer_logic(destroyer, None, bullets, window_size)
        graphics = Destroyer_gfx(window_size, destroyer, None, bullets, "./media/background.png")

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
                            bullets.add_bullet(0,100, destroyer.get_direction(), 2000)

            graphics.draw()
            sleep(0.005)
            #screen.fill(black)
            #screen.blit(ball, ballrect)
            #pygame.display.flip()


    def __del__(self):
        pass

if __name__ == "__main__":
    myGame = Destroyer_game()
