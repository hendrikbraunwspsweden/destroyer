import sys, pygame
import datetime
from math import sin, cos, radians, pi
from time import sleep
import math
from random import randrange

def project_point(original_x, original_y, bearing, distance):

    if bearing >= 360:
        bearing = bearing -360

    if bearing == 0:
        return [original_x, original_y - distance]
    if bearing == 90:
        return [original_x + distance, original_y]
    if bearing == 180:
        return [original_x, original_y + distance]
    if bearing == 270:
        return [original_x - distance, original_y]

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

        if type == 0:
            self.__pipe_length = 30

            self.__image = pygame.image.load("./media/warship.png")
            self.__image_size = self.__image.get_rect()[2], self.__image.get_rect()[3]

            self.__rect = pygame.Rect(self.__window_size[0]/2 - self.__image_size[0]/2,
                self.__window_size[1]/2 - self.__image_size[1]/2,
                self.__image_size[0], self.__image_size[1])

            self.__tower_image = pygame.image.load("./media/tower1.png")
            self.__tower_size = self.__tower_image.get_rect()[2], self.__tower_image.get_rect()[3]

            self.__tower_rect = pygame.Rect(self.__window_size[0]/2 - self.__tower_size[0]/2,
                                            self.__window_size[1]/2 - self.__tower_size[1]/2,
                                            self.__tower_size[0], self.__tower_size[1])
            self.__pipe = (self.__window_size[0]/2, self.__window_size[1]/2 - 10)

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

        self.__pipe = project_point(self.__window_size[0]/2, self.__window_size[1]/2,
                                    self.__tower_direction, self.__pipe_length)

    def set_reload_time(self, time):
        self.__reload_time = time

    def get_reload_time(self):
        return self.__reload_time

    def get_image(self):
        return self.__image, self.__rect

    def get_tower(self):
        return self.__tower_image, self.__tower_rect

    def get_pipe(self):
        return self.__pipe

    def shoot(self):
        if self.__last_shot is None:
            self.__last_shot = datetime.datetime.now()
            return True
        else:
            delta = datetime.datetime.now() - self.__last_shot
            if delta.total_seconds()*1000 > self.__reload_time:
                self.__last_shot = datetime.datetime.now()
                return True
            else:
                return False

    def get_direction(self):
        return self.__tower_direction

class Enemy(object):

    def __init__(self, enemy_type, strength, px_per_second, origin, direction):
        self.__strength = strength
        self.__position = origin
        self.__direction = direction
        self.__px_per_second = px_per_second
        self.__direction = direction
        self.__old_time = datetime.datetime.now()
        self.__image = None
        self.__image_size = None

        if enemy_type == 0:
            self.__image = pygame.image.load("./media/submarine.png")
            if self.__direction == 1:
                self.__image = pygame.transform.rotate(self.__image, 180)

        self.__image_size = self.__image.get_rect()[2], self.__image.get_rect()[3]

        self.__rect = pygame.Rect(self.__position[0], self.__position[1]-self.__image_size[1]/2,
                                  self.__image_size[0], self.__image_size[1])

    def get_rect(self):
        rect = self.__position[0], self.__position[1], self.__position[0] + self.__rect[2], self.__position[1] + \
               self.__rect[3]

        return rect

    def get_direction(self):
        return self.__direction

    def get_position(self):
        return self.__position

    def move(self):
        new_time = datetime.datetime.now()
        time_delta = new_time - self.__old_time
        self.__old_time = new_time
        vector_delta = math.floor(time_delta.total_seconds() * self.__px_per_second)

        if self.__direction == 3:
            self.__position = self.__position[0] - vector_delta, self.__position[1]
            self.__rect = pygame.Rect(self.__position[0]-vector_delta, self.__position[1] - self.__image_size[1]/2,
                                      self.__image_size[0], self.__image_size[1])

        if self.__direction == 1:
            self.__position = self.__position[0] + vector_delta, self.__position[1]
            self.__rect = pygame.Rect(self.__position[0]-vector_delta, self.__position[1] - self.__image_size[1]/2,
                                      self.__image_size[0], self.__image_size[1])

    def get_image(self):
        return self.__image, self.__rect

class Enemies():
    def __init__(self, wait_time_range, speed_range, max_enemies, window_size):
        self.__enemy_list = []
        self.__wait_time_range = wait_time_range
        self.__max_enemies = max_enemies
        self.__old_time = datetime.datetime.now()
        self.__next_enemy_in = 0
        self.__window_size = window_size
        self.__speed_range = speed_range

    def add_enemy(self):

        def check_y_position(y):
            for e in self.get_enemies():
                if e.get_rect()[1] - 40 < y < e.get_rect()[3] + 40:
                    return True
            return False

        def randomize():
            type = 0
            strength = 100

            speed = randrange(self.__speed_range[0], self.__speed_range[1], 1)

            good_y = False

            while not good_y:
                y_rand = randrange(0,2,1)
                if y_rand == 0:
                    y = randrange(10, self.__window_size[1]/2-40)
                if y_rand == 1:
                    y = randrange(self.__window_size[1]/2+40, self.__window_size[1]-10)
                if not check_y_position(y):
                    good_y = True

            dir_rand = randrange(0,2,1)
            direction = 1 if dir_rand == 0 else 3
            if direction == 1:
                origin = -150,y
            if direction == 3:
                origin = self.__window_size[0], y

            return type, strength, speed, y, direction, origin

        if len(self.__enemy_list) == 0:
            type, strength, speed, y, direction, origin = randomize()
            self.__enemy_list.append(Enemy(0, strength, speed, origin, direction))
            self.__next_enemy_in = randrange(self.__wait_time_range[0], self.__wait_time_range[1], 1)
            self.__old_time = datetime.datetime.now()
        else:
            if len(self.get_enemies()) < self.__max_enemies:
                new_time = datetime.datetime.now()
                if (new_time - self.__old_time).total_seconds() > self.__next_enemy_in:
                    type, strength, speed, y, direction, origin = randomize()
                    self.__enemy_list.append(Enemy(0,strength, speed, origin, direction))
                    self.__next_enemy_in = randrange(self.__wait_time_range[0], self.__wait_time_range[1], 1)
                    self.__old_time = new_time


    def move(self):
        for e in self.__enemy_list:
            e.move()

    def get_enemies(self):
        return self.__enemy_list

    def remove_enemies(self, indices):
        if len(indices) > 0:
            new_list = []
            for e in range(len(self.__enemy_list)):
                if not e in indices:
                    new_list.append(self.__enemy_list[e])
            self.__enemy_list = new_list


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

        if type == 0:
            self.__image = pygame.image.load("./media/bullet1.png")

        self.__image = pygame.transform.rotate(self.__image, - self.__direction)
        self.__image_size = self.__image.get_rect()[2], self.__image.get_rect()[3]

        self.__rect = pygame.Rect(self.__position[0]-self.__image_size[0]/2, self.__position[1] - self.__image_size[1]/2,
                                  self.__image_size[0], self.__image_size[1])

    def move(self):
        new_time = datetime.datetime.now()
        time_delta = new_time - self.__old_time
        self.__old_time = new_time
        vector_delta = math.floor(time_delta.total_seconds() * self.__px_per_second)

        self.__position = project_point(self.__position[0], self.__position[1], self.__direction, vector_delta)

        self.__rect = pygame.Rect(self.__position[0]-self.__image_size[0]/2, self.__position[1] - self.__image_size[1]/2,
                              self.__image_size[0], self.__image_size[1])

    def get_position(self):
        return [int(math.floor(self.__position[0])), int(math.floor(self.__position[1]))]

    def __del__(self):
        pass

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
        if len(indices)>0:
            new_list = []
            for b in range(len(self.__bullet_list)):
                if not b in indices:
                    new_list.append(self.__bullet_list[b])
            self.__bullet_list = new_list


class Destroyer_logic(object):

    def __init__(self, destroyer, enemies, bullets, window_size):
        self.__destroyer = destroyer
        self.__bullets = bullets
        self.__enemies = enemies
        self.__window_size = window_size

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
                    enemy_remove_list.append(e)
        return bullet_remove_list, enemy_remove_list

    def __check_enemies(self):
        enemies_remove_list = []
        enemies = self.__enemies.get_enemies()
        for i in range(len(self.__enemies.get_enemies())):
            rect = enemies[i].get_rect()
            if enemies[i].get_direction() == 3:
                if rect[2] <= 0:
                    enemies_remove_list.append(i)
            if enemies[i].get_direction() == 1:
                if rect[2] >= self.__window_size[0] + (rect[2]-rect[0]):
                    enemies_remove_list.append(i)
        return enemies_remove_list

    def check(self):

        bullet_remove_list_1 = self.__check_bullets()
        bullet_remove_list_2, enemy_remove_list_1 = self.__check_bullets_enemies()
        enemy_remove_list_2 = self.__check_enemies()

        bullet_remove_list = list(set(bullet_remove_list_1 + bullet_remove_list_2))
        enemy_remove_list = list(set(enemy_remove_list_1 + enemy_remove_list_2))

        self.__bullets.remove_bullets(bullet_remove_list)
        self.__enemies.remove_enemies(enemy_remove_list)

        if len(self.__enemies.get_enemies()) == 0:
            self.__enemies.add_enemy()


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

        self.__screen.blit(self.__destroyer.get_tower()[0], self.__destroyer.get_tower()[1])

        pygame.draw.line(self.__screen, (102,102,102), (self.__window_size[0]/2, self.__window_size[1]/2),
                         (self.__destroyer.get_pipe()), 8)

        for e in self.__enemies.get_enemies():
            self.__screen.blit(e.get_image()[0], e.get_image()[1])

        pygame.display.flip()


class Destroyer_game(object):

    def __init__(self, window_size=(1024,800), game_speed=1, max_enemies=10, enemy_wait_range=(1, 2), speed_range=(120,180)):
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
        enemies = Enemies(enemy_wait_range, speed_range, max_enemies, window_size)
        enemies.add_enemy()
        logic = Destroyer_logic(destroyer, enemies, bullets, window_size)
        graphics = Destroyer_gfx(window_size, destroyer, enemies, bullets, "./media/background.png")
        graphics.draw()
        exit_game = False

        while not exit_game:

            enemies.add_enemy()
            enemies.move()
            bullets.move()
            logic.check()

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

if __name__ == "__main__":
    myGame = Destroyer_game()
