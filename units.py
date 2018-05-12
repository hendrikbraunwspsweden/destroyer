from math import sin, cos, radians
import pygame
import datetime
from math import floor
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

    def __init__(self, type, reload_time, hp, window_size):
        self.__tower_direction = 0
        self.__image = None
        self.__reload_time = None
        self.__hp = hp
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

    def reduce_hp(self, hp):
        ################################################################################################################
        # Reduced hp by a specified number and returns True if no hp left                                              #
        ################################################################################################################
        self.__hp -= hp
        if self.__hp <= 0:
            return True
        else:
            return False


class Enemy(object):
    ####################################################################################################################
    # Base class for enemy objects. That can be ships as well as for example torpedos. The parameter dict _param_dict  #
    # defines the general outline of how the attributes for each sub class are defined:                                #
    # "strength" (int)      : enemy strength points                                                                    #
    # "min_speed" (int)     : minimum unit speed in px/sec                                                             #
    # "max_speed" (int)     : maximum unit speed int px/sec                                                            #
    # "min_dist" (int)      : minumum distance from the unit to the destroyer's horizontal center line in px           #
    # "has_torpedo" (bool)  : defines if the unit shoots torpedos                                                      #
    # "torpedo_type(int)    : torpedo type                                                                             #
    # "torpedo_speed(int)   : torpedo speed in px/sec                                                                  #
    # "torpedo_chance(float): chance of shooting torpedo, between 0.0 and 1.0                                          #
    # "points (int)         : points awarded to player when enemy is shot                                              #
    ####################################################################################################################

    _param_dict = {
        "hp":None,
        "min_speed":None,
        "max_speed": None,
        "min_dist":None,
        "has_torpedo":None,
        "torpedo_type":None,
        "torpedo_speed":None,
        "torpedo_chance":None,
        "points":None
    }

    def __init__(self, hp, px_per_second, origin, direction):
        self._hp = hp
        self._position = origin
        self._direction = direction
        self._px_per_second = px_per_second
        self._direction = direction
        self._old_time = datetime.datetime.now()
        self._image = None
        self._image_size = None
        self._rect = None
        self._has_torpedo = None
        self._torpedo_shot = False

    def get_rect(self):
        rect = self._position[0], self._position[1], self._position[0] + self._rect[2], self._position[1] + \
               self._rect[3]
        return rect

    def get_direction(self):
        return self._direction

    def get_position(self):
        return self._position

    def get_center_point(self):
        return self._position[0] + self._image_size[0]/2, self._position[1] + self._image_size[1]/2

    def move(self):
        new_time = datetime.datetime.now()
        time_delta = new_time - self._old_time
        self._old_time = new_time
        vector_delta = floor(time_delta.total_seconds() * self._px_per_second)
        if vector_delta == 0:
            vector_delta = 1

        if self._direction == 0:
            self._position = self._position[0], self._position[1] - vector_delta
            self._rect = pygame.Rect(self._position[0] - self._image_size[0]/2, self._position[1],
                                     self._image_size[0], self._image_size[1])

        if self._direction == 1:
            self._position = self._position[0] + vector_delta, self._position[1]
            self._rect = pygame.Rect(self._position[0], self._position[1] - self._image_size[1]/2,
                                     self._image_size[0], self._image_size[1])

        if self._direction == 2:
            self._position = self._position[0], self._position[1] + vector_delta
            self._rect = pygame.Rect(self._position[0] - self._image_size[0]/2, self._position[1],
                                     self._image_size[0], self._image_size[1])

        if self._direction == 3:
            self._position = self._position[0] - vector_delta, self._position[1]
            self._rect = pygame.Rect(self._position[0], self._position[1] - self._image_size[1]/2,
                                     self._image_size[0], self._image_size[1])

    def get_image(self):
        return self._image, self._rect

    def has_torpedo(self):
            if self._param_dict["has_torpedo"]:
                if self._has_torpedo is None:
                    chance = self._param_dict["torpedo_chance"]*10
                    rand = randrange(1,10,1)
                    print(rand,chance)
                    if rand <= chance:
                        self._has_torpedo = True
                        return True
                    else:
                        self._has_torpedo = False
                        return False
                else:
                    if self._has_torpedo:
                        return True
                    else:
                        return False

            else:
                return False

    def set_torpedo_shot(self):
        self._torpedo_shot = True

    def get_torpedo_shot(self):
        return self._torpedo_shot

    def reduce_hp(self, hp):
        ################################################################################################################
        # Reduced hp by a specified number and returns True if no hp left                                              #
        ################################################################################################################
        self._hp -= hp
        if self._hp <= 0:
            return True
        else:
            return False

    def get_hp(self):
        return self._hp

    def set_ship_param(self, param, value):
        try:
            self._param_dict[param] = value
        except:
            return 1


class Submarine(Enemy):

    param_dict = {
        "hp":200,
        "min_speed":60,
        "max_speed":80,
        "min_dist":100,
        "has_torpedo":True,
        "torpedo_type":1,
        "torpedo_speed":30,
        "torpedo_chance":0.6,
        "points":100
    }

    def __init__(self, px_per_second, origin, direction):

        Enemy.__init__(self, self.param_dict["hp"], px_per_second, origin, direction)

        #Handing over parameter dict to parent
        self._param_dict = self.param_dict

        #Setting image related parameters
        self._image = pygame.image.load("./media/submarine.png")
        if self._direction == 1:
            self._image = pygame.transform.rotate(self._image, 180)
        self._image_size = self._image.get_rect()[2], self._image.get_rect()[3]
        self._rect = pygame.Rect(self._position[0], self._position[1]-self._image_size[1]/2,
                                 self._image_size[0], self._image_size[1])

    @classmethod
    def get_params(cls):
        return cls.param_dict


class Torpedoboat(Enemy):

    param_dict = {
        "hp":100,
        "min_speed":150,
        "max_speed":200,
        "min_dist":100,
        "has_torpedo":True,
        "torpedo_type":0,
        "torpedo_speed":0,
        "torpedo_chance":0.4,
        "points":100
    }

    def __init__(self, px_per_second, origin, direction):

        Enemy.__init__(self, self.param_dict["hp"], px_per_second, origin, direction)

        #Handing over parameter dict to parent
        self._param_dict = self.param_dict

        #Setting image related parameters
        self._image = pygame.image.load("./media/torpedoboat.png")
        if self._direction == 1:
            self._image = pygame.transform.rotate(self._image, 180)
        self._image_size = self._image.get_rect()[2], self._image.get_rect()[3]
        self._rect = pygame.Rect(self._position[0], self._position[1]-self._image_size[1]/2,
                                 self._image_size[0], self._image_size[1])

    @classmethod
    def get_params(cls):
        return cls.param_dict


class Torpedo_0(Enemy):

    param_dict = {
        "hp":100,
        "min_speed":60,
        "max_speed":60,
        "min_dist":100,
        "has_torpedo":False,
        "torpedo_type":0,
        "torpedo_speed":0,
        "torpedo_chance":0,
        "points":300,
        "damage":50
    }

    def __init__(self, px_per_second, origin, direction):

        Enemy.__init__(self, self.param_dict["hp"], px_per_second, origin, direction)

        #Handing over the parameter dict to the parent class
        self._param_dict = self.param_dict

        #Setting image related parameters
        self._image = pygame.image.load("./media/torpedo1.png")
        if self._direction == 0:
            self._image = pygame.transform.rotate(self._image, 180)
        self._image_size = self._image.get_rect()[2], self._image.get_rect()[3]
        self._rect = pygame.Rect(self._position[0], self._position[1]-self._image_size[1]/2,
                                 self._image_size[0], self._image_size[1])

    @classmethod
    def get_params(cls):
        return cls.param_dict

    def get_damage(self):
        return self._param_dict["damage"]

class Torpedo_1(Enemy):

    param_dict = {
        "hp":100,
        "min_speed":60,
        "max_speed":60,
        "min_dist":100,
        "has_torpedo":False,
        "torpedo_type":0,
        "torpedo_speed":0,
        "torpedo_chance":0,
        "points":300,
        "damage":100
    }

    def __init__(self, px_per_second, origin, direction):

        Enemy.__init__(self, self.param_dict["hp"], px_per_second, origin, direction)

        #Handing over the parameter dict to the parent class
        self._param_dict = self.param_dict

        #Setting image related parameters
        self._image = pygame.image.load("./media/torpedo1.png")
        if self._direction == 0:
            self._image = pygame.transform.rotate(self._image, 180)
        self._image_size = self._image.get_rect()[2], self._image.get_rect()[3]
        self._rect = pygame.Rect(self._position[0], self._position[1]-self._image_size[1]/2,
                                 self._image_size[0], self._image_size[1])

    @classmethod
    def get_params(cls):
        return cls.param_dict

    def get_damage(self):
        return self._param_dict["damage"]

class Enemies():

    def __init__(self, wait_time_range, max_enemies, torpedos, window_size, ship_ratios=[(1,20),(20,100)]):
        ################################################################################################################
        # Ship_ratios is specified of number ranges between 1 and 100 for the different ship types. If ship type 1 is  #
        # to have a 70% chance of appearing and it is first in the list, then the range should be defined as (1,70)    #
        # and if ship type 2 then is supposed to have a 30% chance of appearing, the range has to be specified as      #
        # (70,100). The ship type class that will be initiated based on the randomized number is defined in add_enemy  #
        ################################################################################################################

        self.__enemy_list = []
        self.__wait_time_range = wait_time_range
        self.__max_enemies = max_enemies
        self.__old_time = datetime.datetime.now()
        self.__next_enemy_in = 0
        self.__window_size = window_size
        self.__ship_ratios = ship_ratios
        self.__torpedos = torpedos

    def add_enemy(self):

        def check_y_position(y):
            #Method to check if any other enemy is on the same position or within a frame of 80 pixels

            for e in self.get_enemies():
                if e.get_rect()[1] - 40 < y < e.get_rect()[3] + 40:
                    return True
            return False

        def make_ship():
            ############################################################################################################
            # Function to randomize a ship and its params based on the ratios specified in __ship_ratios.              #
            ############################################################################################################

            ship_type = randrange(1,100,1)
            ship_type_count = len(self.__ship_ratios)
            for i in range(ship_type_count):
                if ship_type in range(self.__ship_ratios[i][0], self.__ship_ratios[i][1]):
                    ship_type = i
                    break


            #Define ship types
            if ship_type == 0:
                param_dict = Submarine.get_params()
            elif ship_type == 1:
                param_dict = Torpedoboat.get_params()

            speed = randrange(param_dict["min_speed"], param_dict["max_speed"], 1)

            good_y = False

            while not good_y:
                y_rand = randrange(0,2,1)
                if y_rand == 0:
                    y = randrange(10, self.__window_size[1]/2-param_dict["min_dist"])
                if y_rand == 1:
                    y = randrange(self.__window_size[1]/2+param_dict["min_dist"], self.__window_size[1]-10)
                if not check_y_position(y):
                    good_y = True

            dir_rand = randrange(0,2,1)
            direction = 1 if dir_rand == 0 else 3
            if direction == 1:
                origin = -150,y
            if direction == 3:
                origin = self.__window_size[0], y

            #Assign classes to the ship types
            if ship_type == 0:
                ship = Submarine(speed, origin, direction)
            elif ship_type == 1 :
                ship = Torpedoboat(speed, origin, direction)

            return ship

        if len(self.__enemy_list) == 0:
            self.__enemy_list.append(make_ship())
            self.__next_enemy_in = randrange(self.__wait_time_range[0], self.__wait_time_range[1], 1)
            self.__old_time = datetime.datetime.now()
        else:
            if len(self.get_enemies()) < self.__max_enemies:
                new_time = datetime.datetime.now()
                if (new_time - self.__old_time).total_seconds() > self.__next_enemy_in:
                    self.__enemy_list.append(make_ship())
                    print(self.__enemy_list[-1].has_torpedo())
                    self.__next_enemy_in = randrange(self.__wait_time_range[0], self.__wait_time_range[1], 1)
                    self.__old_time = new_time

    def move(self):
        for e in self.__enemy_list:
            e.move()

    def shoot(self):
        for e in self.__enemy_list:
            if e.has_torpedo() and not e.get_torpedo_shot():
                if e.get_direction() == 1:
                    center_point = e.get_center_point()
                    if center_point[0] > self.__window_size[0]/2:
                        if center_point[1] < self.__window_size[1]/2:
                            direction = 2
                        else:
                            direction = 0
                        if e.get_params()["torpedo_type"] == 0:
                            self.__torpedos.add_torpedo(Torpedo_0(Torpedo_0.get_params()["min_speed"],
                                                                  center_point,direction))
                        if e.get_params()["torpedo_type"] == 1:
                            self.__torpedos.add_torpedo(Torpedo_1(Torpedo_1.get_params()["min_speed"],
                                                              center_point,direction))
                        e.set_torpedo_shot()

                if e.get_direction() == 3:
                    center_point = e.get_center_point()
                    if center_point[0] < self.__window_size[0]/2:
                        if center_point[1] < self.__window_size[1]/2:
                            direction = 2
                        else:
                            direction = 0
                        if e.get_params()["torpedo_type"] == 0:
                            self.__torpedos.add_torpedo(Torpedo_0(Torpedo_0.get_params()["min_speed"],
                                                                  center_point,direction))
                        if e.get_params()["torpedo_type"] == 1:
                            self.__torpedos.add_torpedo(Torpedo_1(Torpedo_1.get_params()["min_speed"],
                                                                  center_point,direction))
                        e.set_torpedo_shot()


    def get_enemies(self):
        return self.__enemy_list

    def remove_enemies(self, indices):
        if len(indices) > 0:
            new_list = []
            for e in range(len(self.__enemy_list)):
                if not e in indices:
                    new_list.append(self.__enemy_list[e])
            self.__enemy_list = new_list

    def set_max_enemies(self, count):
        self.__max_enemies = count


class Torpedos(object):
    def __init__(self):
        self.__torpedo_list = []

    def get_torpedos(self):
        return self.__torpedo_list

    def add_torpedo(self, torpedo):
        self.__torpedo_list.append(torpedo)

    def move(self):
        for t in self.__torpedo_list:
            t.move()

    def remove_torpedos(self, indices):
        if len(indices) > 0:
            new_list = []
            for e in range(len(self.__torpedo_list)):
                if not e in indices:
                    new_list.append(self.__torpedo_list[e])
            self.__torpedo_list = new_list


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
        vector_delta = floor(time_delta.total_seconds() * self.__px_per_second)

        self.__position = project_point(self.__position[0], self.__position[1], self.__direction, vector_delta)

        self.__rect = pygame.Rect(self.__position[0]-self.__image_size[0]/2, self.__position[1] - self.__image_size[1]/2,
                                  self.__image_size[0], self.__image_size[1])

    def get_position(self):
        return [int(floor(self.__position[0])), int(floor(self.__position[1]))]

    def __del__(self):
        pass

    def get_image(self):
        return self.__image, self.__rect

    def get_power(self):
        return self.__power


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
