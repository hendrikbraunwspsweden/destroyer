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


class Destroyer_gfx(object):

    def __init__(self, window_size, destroyer, enemies, bullets, fades, bg_image):
        self.__destroyer = destroyer
        self.__enemies = enemies
        self.__bullets = bullets
        self.__fades = fades
        self.__screen = pygame.display.set_mode(window_size)
        self.__background_path = bg_image
        self.__window_size = window_size
        self.make_background()
        self.__explosions = []

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

        pygame.draw.line(self.__screen, (102,102,102), (self.__window_size[0]/2, self.__window_size[1]/2),
                         (self.__destroyer.get_pipe()), 8)

        for e in self.__enemies.get_enemies():
            self.__screen.blit(e.get_image()[0], e.get_image()[1])

        pygame.display.flip()

