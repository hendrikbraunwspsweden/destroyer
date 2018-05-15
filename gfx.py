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


import pygame
import datetime

def blit_alpha(target, source, location, opacity):

    """
     Function for blit:ing objects with specified opacity onto the game window                                        
    """

    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

class Fade_fx(object):
    def __init__(self, image, rect, time):

        """
         Class for fade effects. Those are for example boats that have been shot, so they don't just disappear but    
         rather fade out.                                                                                             
         image (pygame.image)  : image to be faded                                                                    
         rect (pygame.Rect)    : position rectangle of the image                                                      
         time (int)            : fade time in seconds                                                                 
        """

        self._image = image
        self._rect = rect
        self._time = time
        self._steps = 255/self._time
        self._old_time = datetime.datetime.now()
        self._total_time = 0
        self._alpha = 255

    def fade(self):
        if self._alpha < 0:
            return -1
        else:
            new_time = datetime.datetime.now()
            self._total_time += (new_time - self._old_time).total_seconds()
            self._alpha = 255 - self._steps * self._total_time
        self._old_time = new_time
        return 0

    def get_image(self):
        return self._image, self._rect

    def get_alpha(self):
        return self._alpha


class Fades(object):
    def __init__(self):

        """
         Class for managing all the fades in the game window                                                          
        """

        self.__fade_list = []

    def add_fade(self, image, rect, time):
        self.__fade_list.append(Fade_fx(image, rect, time))

    def fade(self):
        new_fades = []
        for i in range(len(self.__fade_list)):
            if not self.__fade_list[i].fade() == -1:
                new_fades.append(self.__fade_list[i])
        self.__fade_list = new_fades

    def get_fades(self):
        return self.__fade_list


class Text_fx(object):
    def __init__(self, origin, text, time, movement, positive=True):

        """
         Class for text effects. Those are for example the point texts shown when an enemy is destroyed. The text is  
         moved and faded at the same time, giving it a smooth appearance.                                             
         origin (list of int)  : origin of the text. This will be the bottom center position of the text rectangle    
         text (string)         : text to be displayed                                                                 
         time (int)            : time until complete fade and movement in ms                                          
         movement (int)        : text movement range towards north in pixels                                          
         positive (bool)       : if positive, text is black, otherwise red                                            
        """

        self._text = text
        self._time = time
        self._movement = movement

        self._alpha_steps = 255.0/self._time
        self._steps = self._movement/float(self._time)
        self._origin = origin
        self._old_time = datetime.datetime.now()
        self._time_delta = 0
        self._alpha = 255
        self._color = (0,0,0)
        self._rect = None

        if not positive:
            self._color = (190,28,28)

        myfont = pygame.font.SysFont('Arial', 16)
        self._image = myfont.render(self._text, False, self._color)
        rect = self._image.get_rect()
        self._size_x, self._size_y = rect[2], rect[3]
        self._position = (self._origin[0] - (self._size_x/2), self._origin[1] - (self._size_y/2))
        self._rect = (self._position[0], self._position[1], self._size_x, self._size_y)

    def move(self):
        if self._alpha < 0:
            return -1
        else:
            new_time = datetime.datetime.now()
            self._time_delta += (new_time - self._old_time).total_seconds() * 1000
            self._alpha = 255 - self._alpha_steps * self._time_delta
            self._position = (self._position[0], round(self._origin[1] - self._steps * self._time_delta, 0))
            self._rect = pygame.Rect(self._position[0], self._position[1], self._size_x, self._size_y)
        self._old_time = new_time
        return 0

    def get_image(self):
        return self._image, self._rect

    def get_alpha(self):
        return self._alpha


class Texts(object):

    """
     Class holding all text effect objects in the game                                                                
    """

    def __init__(self):
        self.__text_list = []

    def add_text(self, origin, text, positive=True):
        self.__text_list.append(Text_fx(origin, text, 1000, 80, positive=positive))

    def move(self):
        new_texts = []
        for i in range(len(self.__text_list)):
            if not self.__text_list[i].move() == -1:
                new_texts.append(self.__text_list[i])
        self.__text_list = new_texts

    def get_texts(self):
        return self.__text_list


class Explosion(object):
    def __init__(self, origin, pause):

        """
         Explosion animation class. Shows the sequence of explosion images at specified intervals to create the       
         illusion of an awesome explosion                                                                             
         origin (list of int)  : origin as x,y. Usually the impact point of the bullet Lower center of the image      
                                 rectangle                                                                            
         pause (int)           : pause between the images in ms                                                       
        """

        self.__frame = 1
        self.__image = pygame.image.load("./media/explosion/frame_1.png")
        self.__old_time = datetime.datetime.now()
        self.__rect = pygame.Rect(origin[0]-63, origin[1]-132, 62, 132)
        self.__pause = pause

    def next_frame(self):

        """
         Method to walk through the frames and change image if the specified pause time has elapsed. If the explosion 
         sequence is finished, it returns True, otherwise False.                                                      
        """

        new_time = datetime.datetime.now()
        if self.__frame > 17:
            return True
        if (new_time - self.__old_time).total_seconds()*1000 >= self.__pause:
            self.__image = pygame.image.load("./media/explosion/frame_{}.png".format(self.__frame))
            self.__old_time = new_time
            self.__frame += 1
        return False

    def get_image(self):
        return self.__image, self.__rect


class Explosions(object):

    """
     Class holding all instances of explosion objects in the game.                                                    
    """

    def __init__(self):
        self.__explosion_list = []

    def add_explosion(self, explosion):
        self.__explosion_list.append(explosion)

    def change_frames(self):
        new_list = []
        for e in self.__explosion_list:
            if not e.next_frame():
                new_list.append(e)
        self.__explosion_list = new_list

    def get_explosions(self):
        return self.__explosion_list


class Destroyer_gfx(object):

    def __init__(self, window_size, destroyer, enemies, bullets, torpedos, explosions, fades, texts, points, crates,
                 font_size, bg_image):
        """
         Main graphics class. This is where all the elements are drawn.                                               
         window_size (list of int) : window size in px as x,y                                                         
         destroyer (Destroyer)     : Destroyer class game instance                                                    
         enemies (Enemies)         : Enemies class game instance                                                      
         bullets (Bullets)         : Bullets class game instance                                                      
         torpedos (Torpedos)       : Torpedos class game instance                                                     
         explosions (Explosions)   : Explosions class game instance                                                   
         fades (Fades)             : Fades class game instance                                                        
         texts (Texts)             : Texts class game instance                                                        
         points (Points)           : Points class game instance                                                       
         crates (Creates)          : Crates class game instance                                                       
         font_size (int)           : HUD font size                                                                    
         bg_image (string)         : path to the background image                                                     
        """
        self.__destroyer = destroyer
        self.__enemies = enemies
        self.__bullets = bullets
        self.__torpedos = torpedos
        self.__fades = fades
        self.__screen = pygame.display.set_mode(window_size)
        self.__background_path = bg_image
        self.__window_size = window_size
        self.__explosions = explosions
        self.__points = points
        self.__texts = texts
        self.__font_size = font_size
        self.__crates = crates
        self.make_background()

    def __render_hud(self):
        myfont = pygame.font.SysFont('Arial', self.__font_size)
        rect = pygame.Rect(0,0,self.__window_size[0],self.__font_size)
        pygame.draw.rect(self.__screen, (150,150,150), rect, 0)

        points = myfont.render('Points: {}'.format(self.__points.get_points()), False, (255, 255, 255))
        self.__screen.blit(points, (0,0))

        hp_ratio = self.__destroyer.get_hp() / float(self.__destroyer.get_max_hp())
        surface = myfont.render('Life: {}'.format(self.__destroyer.get_hp()), False, (255, 255*hp_ratio,255*hp_ratio))

        self.__screen.blit(surface, (100,0))


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

        for c in self.__crates.get_crates():
            self.__screen.blit(c.get_image()[0], c.get_image()[1])

        for f in self.__fades.get_fades():
            blit_alpha(self.__screen, f.get_image()[0], f.get_image()[1], f.get_alpha())

        self.__screen.blit(self.__destroyer.get_tower()[0], self.__destroyer.get_tower()[1])

        for t in self.__torpedos.get_torpedos():
            self.__screen.blit(t.get_image()[0], t.get_image()[1])

        for e in self.__enemies.get_enemies():
            self.__screen.blit(e.get_image()[0], e.get_image()[1])

        pygame.draw.line(self.__screen, (102,102,102), (self.__window_size[0]/2, self.__window_size[1]/2),
                         (self.__destroyer.get_pipe()), 8)

        for e in self.__explosions.get_explosions():
            self.__screen.blit(e.get_image()[0], e.get_image()[1])

        for f in self.__texts.get_texts():
            blit_alpha(self.__screen, f.get_image()[0], f.get_image()[1], f.get_alpha())

        self.__render_hud()

        pygame.display.update()

