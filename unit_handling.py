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

from units import *

class Enemies():

    def __init__(self, wait_time_range, max_enemies, torpedos, crates, game_speed, window_size, top_distance,
                 ship_ratios=[(1, 20), (20, 100)], max_torpedos=2):
        ################################################################################################################
        # Class for handling all enemy ship objects.                                                                   #
        # wait_time_range (list of int)     : range of minimum wait time to maximum wait time for spawn of next enemy  #
        # max_enemies (int)                 : maximum numbers of enemies at once on the screen                         #
        # torpedos (Torpedos)               : game instance of Torpedos class                                          #
        # crates (Crates)                   : game instance of Crates class                                            #
        # game_speed (int)                  : game speed between 0 and n. Boat speed is adjusted by the game speed     #
        #                                     multiplier defined in the class of the boat types                        #
        # window_size (list of int)         : window size in x,y                                                       #
        # top_distance (int)                : minimum y position for spwaning enemies in order to avoid HUD            #
        # ship_ratios (list of ranges)      : see description below                                                    #
        # max_torpedos (int)                : maximum number of torpedos on the screen at the same time                #
        #                                                                                                              #
        #                                                                                                              #
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
        self.__crates = crates
        self.__game_speed = game_speed
        self.__top_distance = top_distance
        self.__max_torpedos = max_torpedos
        self.__total_enemies = 0

    def add_enemy(self):
        ################################################################################################################
        # Method for evaluating if an enemy is to be added, based on the actual number and the time passed since the   #
        # last spawn.                                                                                                  #
        ################################################################################################################

        def check_y_position(y):
            ############################################################################################################
            # Method to check if any other enemy is on the same position or within a frame of 80 pixels. If so, the    #
            # position is regarded as bad and a new ship will not be spawned within that range.                        #
            ############################################################################################################

            for e in self.__enemy_list:
                rect = e.get_rect()
                if rect[1] - 40 < y < rect[3] + 40:
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
                    y = randrange(self.__top_distance + 10, self.__window_size[1]/2-param_dict["min_dist"])
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
            self.__total_enemies += 1
            self.__next_enemy_in = randrange(self.__wait_time_range[0], self.__wait_time_range[1], 1)
            self.__old_time = datetime.datetime.now()
        else:
            if len(self.__enemy_list) < self.__max_enemies:
                new_time = datetime.datetime.now()
                if (new_time - self.__old_time).total_seconds() > self.__next_enemy_in:
                    self.__enemy_list.append(make_ship())
                    self.__total_enemies += 1
                    self.__next_enemy_in = randrange(self.__wait_time_range[0], self.__wait_time_range[1], 1)
                    self.__old_time = new_time

    def move(self):
        ################################################################################################################
        # Move all ships.                                                                                              #
        ################################################################################################################
        for e in self.__enemy_list:
            e.move(self.__game_speed)

    def shoot(self):
        ################################################################################################################
        # Method for making the existing ships shoot torpedos under defined cicumstances, being that they have are on  #
        # or have passed the center of the screen, they are equipped with a torpedo (which is defined in the parameter #
        # dictionary in the ship class) and there are less than the allowed maximum amount of torpedos on the screen at#
        # this point in time. If there are more, the ship looses it's torpedo.                                         #
        ################################################################################################################

        for e in self.__enemy_list:
            if e.has_torpedo() and not e.get_torpedo_shot():
                if e.get_direction() == 1:
                    center_point = e.get_center_point()
                    if center_point[0] > self.__window_size[0]/2:
                        if self.__torpedos.count() >= self.__max_torpedos:
                            e.set_torpedo_shot()
                        else:
                            if center_point[1] < self.__window_size[1]/2:
                                direction = 2
                            else:
                                direction = 0

                            torpedo_type = e.get_params()["torpedo_type"]
                            if torpedo_type == 0:
                                self.__torpedos.add_torpedo(Torpedo_0(Torpedo_0.get_params()["min_speed"],
                                                                      center_point,direction))
                            if torpedo_type == 1:
                                self.__torpedos.add_torpedo(Torpedo_1(Torpedo_1.get_params()["min_speed"],
                                                                      center_point,direction))
                            e.set_torpedo_shot()

                if e.get_direction() == 3:
                    center_point = e.get_center_point()
                    if center_point[0] < self.__window_size[0]/2:
                        if self.__torpedos.count() >= self.__max_torpedos:
                            e.set_torpedo_shot()
                        else:
                            if center_point[1] < self.__window_size[1]/2:
                                direction = 2
                            else:
                                direction = 0

                            torpedo_type = e.get_params()["torpedo_type"]
                            if torpedo_type == 0:
                                self.__torpedos.add_torpedo(Torpedo_0(Torpedo_0.get_params()["min_speed"],
                                                                      center_point,direction))
                            if torpedo_type == 1:
                                self.__torpedos.add_torpedo(Torpedo_1(Torpedo_1.get_params()["min_speed"],
                                                                      center_point,direction))
                            e.set_torpedo_shot()


    def get_enemies(self):
        return self.__enemy_list

    def remove_enemies(self, indices):
        ################################################################################################################
        # Removes the enemies at given indices. Called from the Destroyer_logic class game instance.                   #
        # indices (list of int) : indices of the enemies that are to be deleted.                                       #
        ################################################################################################################

        if len(indices) > 0:
            new_list = []
            for e in range(len(self.__enemy_list)):
                if not e in indices:
                    new_list.append(self.__enemy_list[e])
            self.__enemy_list = new_list

    def set_max_enemies(self, count):
        self.__max_enemies = count

    def get_total_enemies(self):
        return self.__total_enemies


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

    def count(self):
        return len(self.__torpedo_list)


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

class Crates(object):
    def __init__(self, window_size, y_margin, destroyer, wait_range=(20,30), timeout=8, max_crates=2):
        ################################################################################################################
        # Class for handling crates in the game. Crates appear on randomized positions in the game at random time      #
        # intervals.                                                                                                   #
        # window_size (list of int) : game window size as x,y                                                          #
        # y_margin (int)            : y margin for crate positions based for avoiding HUD                              #
        # destroyer (Destroyer)     : Destroyer game instance                                                          #
        # wait_range (range of int) : range of seconds between which the time delta for the next crate spawn is        #
        #                             randomized.                                                                      #
        # timeout (int)             : defines how long in seconds crates are in existence after spawning.              #
        # max_crates (int)          : the maximum number of crates on the screen at the same point in time             #
        ################################################################################################################

        self._window_size = window_size
        self._wait_range = wait_range
        self._max_crates = max_crates
        self._y_margin = y_margin
        self._destroyer = destroyer
        self._enemies = None
        self._crates_list = []
        self._old_time = datetime.datetime.now()
        self._pause = randrange(wait_range[0], wait_range[1], 1)
        self._timeout = timeout
        self._crate_type = None

    def make_crate(self):
        ################################################################################################################
        # Checks if the time randomized during the last crate spawning event has elapsed. If that is the case, a new   #
        # crate is created based on randomized values. The randomized values are checked against existing ship and the #
        # destroyer positions. The values are randomized until no collision is found.                                  #
        # TODO: Randomize crate types                                                                                  #
        ################################################################################################################
        new_time = datetime.datetime.now()
        if (new_time-self._old_time).total_seconds() > self._pause:
            self._crate_type = randrange(0,1,1)
            good_pos = False
            enemies = self._enemies.get_enemies()
            destroyer = self._destroyer.get_image()
            crate_size = Crate.get_size()

            while not good_pos:
                print("makeing crates")
                good_pos_int = 0
                x = randrange(0,self._window_size[0], 1)
                y = randrange(self._y_margin, self._window_size[1] - 30, 1)

                for e in enemies:
                    #rect = pygame.Rect(0, e.get_rect()[1], self._window_size[0], e.get_rect()[3])
                    if e.get_rect().colliderect(pygame.Rect(x,y,crate_size[0], crate_size[1])):
                        good_pos_int += 1

                if destroyer[1].colliderect(pygame.Rect(x,y,crate_size[0], crate_size[1])):
                    good_pos_int += 1

                if good_pos_int == 0:
                    good_pos = True

            self._crates_list.append(Crate((x,y),100, 0, 100))
            self._pause = randrange(self._wait_range[0], self._wait_range[1], 1)
            self._old_time = new_time

    def get_crates(self):
        return self._crates_list

    def remove_crates(self, indices):
        if len(indices)>0:
            new_list = []
            for b in range(len(self._crates_list)):
                if not b in indices:
                    new_list.append(self._crates_list[b])
            self._crates_list = new_list

    def check(self):
        remove_list = []
        for c in range(len(self._crates_list)):
            if self._crates_list[c].get_age() > self._timeout:
                remove_list.append(c)
        self.remove_crates(remove_list)

    def set_enemies(self, enemies):
        ################################################################################################################
        # The enemies object for the crates class has to be set after initialization due to a circular reference, e.g. #
        # that the crates class uses the enemy class and the enemy class uses the crates class. Initialize the crates  #
        # class first, hand it over to the instance of the enemy class and then set the enemies instance in the crates #
        # instance using this method.                                                                                  #
        ################################################################################################################
        self._enemies = enemies