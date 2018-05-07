import sys, pygame
import datetime

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
    __position = [None,None]
    __direction = 0
    __speed = 0

    def __init__(self, type, power, origin, direction, speed):
        self.__type = type
        self.__power = power
        self.__position = origin
        self.__direction = direction
        self.__speed = speed

    def move(self):
        pass

    def get_position(self):
        return self.__position

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
            if (self.__window_size[0]>= bullet_list[i].get_position()[0] <= 0) or (self.__window_size[1] >= bullet_list[i].get_position()[1] <= 0):
                bullet_remove_list.append(i)

class Destroyer_game(object):

    __enemies = []
    __bullets = []
    __enemy_strenght = None
    __game_speed = None
    __max_enemies = 1
    __window_size = ()

    def __init__(self, window_size=(400,400), game_speed=1, max_enemies=1):
        self.__window_size = window_size
        self.__game_speed = game_speed
        self.__max_enemies = max_enemies

        pygame.init()
        screen = pygame.display.set_mode(window_size)
        destroyer = Destroyer(0, 1000)
        bullets = Bullets((window_size[0]/2, window_size[1]/2), window_size)

        exit_game = False

        while not exit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                if event.type is pygame.KEYDOWN:
                    key = pygame.key.name(event.key)

                    if key == "escape":
                        exit_game = True

                    if key == "right":
                        destroyer.turn_tower(1,1)

                    if key == "left":
                        destroyer.turn_tower(3,1)

                    if key == "space":
                        if destroyer.shoot():
                            bullets.add_bullet(0,100, destroyer.get_direction(), 100)

            bullets.move()


            #screen.fill(black)
            #screen.blit(ball, ballrect)
            #pygame.display.flip()


    def __del__(self):
        pass

if __name__ == "__main__":
    myGame = Destroyer_game()
