from units import *

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
