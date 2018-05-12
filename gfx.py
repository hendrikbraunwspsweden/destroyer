import pygame
import datetime

def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

class Fade_fx(object):
    def __init__(self, image, rect, time):
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


class Explosion(object):
    def __init__(self, origin, pause):
        self.__frame = 1
        self.__image = pygame.image.load("./media/explosion/frame_1.png")
        self.__old_time = datetime.datetime.now()
        self.__rect = pygame.Rect(origin[0]-63, origin[1]-132, 62, 132)
        self.__pause = pause

    def next_frame(self):
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

class Muzzle_flash(object):
    def __init__(self, origin, angle, show_for):
        self.__frame = 1
        self.__image = pygame.image.load("./media/muzzle_flash.png")
        self.__old_time = datetime.datetime.now()
        self.__rect = pygame.Rect(origin[0]-63, origin[1]-132, 62, 132)
        self.__show_for = show_for
        self.__origin = origin

    def next_frame(self):
        new_time = datetime.datetime.now()
        if (new_time - self.__old_time).total_seconds()*1000 >= self.__show_for:
            return True
        return False

    def get_image(self):
        return self.__image, self.__rect

class Explosions(object):
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

    def __init__(self, window_size, destroyer, enemies, bullets, torpedos, explosions, fades, points, font_size,
                 bg_image):
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
        self.__font_size = font_size
        self.make_background()

    def __render_hud(self):
        myfont = pygame.font.SysFont('Comic Sans MS', self.__font_size)
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

        self.__render_hud()

        pygame.display.update()

