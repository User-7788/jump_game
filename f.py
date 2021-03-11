import time
from random import choice

import pygame

pygame.init()

width = 500
height = 650
size = width, height

screen = pygame.display.set_mode(size)
pygame.display.set_caption("jump game")

# icon = pygame.image.load('data/icon.jpg')
# pygame.display.set_icon(icon)

B_GREEN = (139, 255, 182)
B_GREEN_C = (89, 205, 132)
B_CHOSEN = (183, 255, 1)
SIMPLE = 'Simple'
PIC = {}
g = 0.1
clock = pygame.time.Clock()
fps = 60
r_b_down = False
l_b_down = False
h = 110
lis_x = [0, 100, 200, 300, 400]
pl_v = 1
platforms = []
tim = 0


def load_image(pic):
    name = 'data' + '/' + pic
    try:
        if name[-2:] == 'jpg':
            im = pygame.image.load(name).convert()
        else:
            im = pygame.image.load(name).convert_alpha()

        return im
    except Exception:
        pass


class Platform:
    def __init__(self, x, y, typ=SIMPLE, w=100, h=5):
        self.x = x
        self.y = y
        self.typ = typ
        self.w = w
        self.h = h
        if typ == SIMPLE:
            self.color = (0, 0, 205)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y,
                                              self.w, self.h))


def create_new(last):
    if last.y >= 650:
        platforms.remove(last)
        platforms.append(Platform(choice(lis_x), 0))


def is_on_platform(p):
    global vy, pic, tim
    if (y + pic.get_height() >= (p.y - (abs(vy) // 2))) and (y + pic.get_height() <= p.y + p.h + (abs(vy) // 2)) and (
            x + (pic.get_width() // 2) >= p.x) and (x + (pic.get_width() // 2) <= (p.x + p.w)) and (vy >= 0):
        vy = -6
        pic = pygame.image.load("data/down.png").convert_alpha()
        tim = 0


class Button:
    def __init__(self, x, y, w=300, h=50, color_1=(255, 0, 70), color_2=(0, 0, 0), txt_c=(0, 0, 0)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color_now = color_1
        self.color_2 = color_2
        self.color_1 = color_1
        self.txt_c = txt_c

    def draw(self, text, xy, big=50):
        global pos, B_CHOSEN
        font = pygame.font.Font(None, big)
        pygame.draw.rect(screen, self.color_now, (self.x, self.y,
                                                  self.w, self.h))
        pygame.draw.rect(screen, self.color_2, (self.x, (self.y + 9 * (self.h // 10)),
                                                self.w, (self.h // 10)))
        if not self.should_i_color(pos) and not self.color_now == B_CHOSEN:
            light_c = []
            for i in self.color_now:
                light_c.append(i + 30 if i + 30 <= 255 else 255)
            light_c = light_c[0], light_c[1], light_c[2]

            pygame.draw.rect(screen, light_c, (self.x, self.y,
                                               self.w, (self.h // 10)))

        screen.blit(font.render(text, 1, self.txt_c), xy)

    def is_cliced(self):
        x_m, y_m = event.pos
        if (x_m <= (self.x + self.w) and (x_m >= self.x)) and (
                y_m <= (self.y + self.h) and (y_m >= self.y)):
            return True
        return False

    def should_i_color(self, pos, do_it=False):
        x_m, y_m = pos
        c = ((x_m <= (self.x + self.w) and (x_m >= self.x)) and (
                y_m <= (self.y + self.h) and (y_m >= self.y))) or do_it
        if c:
            self.color_now = self.color_2
        else:
            self.color_now = self.color_1
        return c


is_menu = True
is_paused = False
is_end = False
hard_level = 1

start_b = Button(60, 150, 390, 100, color_1=(193, 84, 193), color_2=(143, 34, 143))
easy_b = Button(60, 270, 390, 60, color_1=B_CHOSEN, color_2=B_CHOSEN, txt_c=(50, 50, 50))
norm_b = Button(60, 340, 390, 60, color_1=B_GREEN, color_2=B_GREEN_C, txt_c=(50, 50, 50))
hard_b = Button(60, 410, 390, 60, color_1=B_GREEN, color_2=B_GREEN_C, txt_c=(50, 50, 50))
menu_quit_b = Button(60, 490, 390, 100, color_1=(255, 102, 255), color_2=(215, 62, 215))
pause_b = Button(5, 5, 50, 50, color_1=(141, 0, 255), color_2=(91, 0, 205))

for i in range(1, 6):
    p = Platform(choice(lis_x), 125 * i)
    platforms.append(p)

running = True

pic = pygame.image.load("data/normal.png").convert_alpha()
x = width // 2
y = 100
vx = 4
vy = 0

while running:
    pygame.display.flip()
    clock.tick(fps)
    screen.fill((0, 0, 0))

    pos = pygame.mouse.get_pos()

    if not is_menu and not is_end:
        screen.fill((133, 247, 215))

        if is_paused:
            font = pygame.font.Font(None, 30)

            s = pygame.Surface((width, height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))

            for p in platforms:
                p.draw()

            screen.blit(pic, [x, y])

            screen.blit(s, (0, 0))

            pause_b.draw('>', (20.5, 4), big=63)
            screen.blit(font.render('|', 10, pause_b.txt_c), (20, 18.5))
            screen.blit(font.render('|', 10, pause_b.txt_c), (19, 18.5))

            pause_b.should_i_color(pos)


        else:
            if tim >= 5:
                pic = pygame.image.load("data/normal.png").convert_alpha()
            else:
                tim += 1
            q = sorted(platforms, key=lambda x: x.y)[-1]
            create_new(q)
            for p in platforms:
                p.y += pl_v
                is_on_platform(p)
                p.draw()

            screen.blit(pic, [x, y])

            if y <= 0:
                vy = 0
                y = 0
            if r_b_down and not (x + pic.get_width()) > width:
                x += vx
            elif l_b_down and not x <= 0:
                x -= vx
            vy += g
            y += vy

            pause_b.draw('| |', (15, 9.5), big=55)
            pause_b.should_i_color(pos)



    elif is_menu and not is_end:
        screen.fill((141, 0, 255))

        start_b.draw('START GAME', (117, 182), big=60)
        start_b.should_i_color(pos)

        easy_b.draw('EASY level', (156, 285), big=50)
        easy_b.should_i_color(pos)

        norm_b.draw('NORMAL level', (134, 355), big=50)
        norm_b.should_i_color(pos)

        hard_b.draw('HARD level', (157, 425), big=50)
        hard_b.should_i_color(pos)

        menu_quit_b.draw('QUIT', (213, 523), big=50)
        menu_quit_b.should_i_color(pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_menu:
                if menu_quit_b.is_cliced():
                    running = False
                elif easy_b.is_cliced():
                    hard_level = 1

                    easy_b.color_1 = B_CHOSEN
                    easy_b.color_2 = B_CHOSEN

                    norm_b.color_1 = B_GREEN
                    norm_b.color_2 = B_GREEN_C

                    hard_b.color_1 = B_GREEN
                    hard_b.color_2 = B_GREEN_C

                elif norm_b.is_cliced():
                    hard_level = 2

                    norm_b.color_1 = B_CHOSEN
                    norm_b.color_2 = B_CHOSEN

                    easy_b.color_1 = B_GREEN
                    easy_b.color_2 = B_GREEN_C

                    hard_b.color_1 = B_GREEN
                    hard_b.color_2 = B_GREEN_C

                elif hard_b.is_cliced():
                    hard_level = 3

                    hard_b.color_1 = B_CHOSEN
                    hard_b.color_2 = B_CHOSEN

                    norm_b.color_1 = B_GREEN
                    norm_b.color_2 = B_GREEN_C

                    easy_b.color_1 = B_GREEN
                    easy_b.color_2 = B_GREEN_C

                elif start_b.is_cliced():
                    is_menu = False
            if not is_menu and not is_end:
                if pause_b.is_cliced():
                    is_paused = not is_paused

        if event.type == pygame.KEYDOWN:
            if not (is_menu and is_end):

                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE]:
                    is_paused = not is_paused
                if pressed[pygame.K_RIGHT]:
                    x += vx
                    r_b_down = True
                    l_b_down = False
                if pressed[pygame.K_LEFT]:
                    x -= vx
                    l_b_down = True
                    r_b_down = False

        if event.type == pygame.KEYUP:
            if not (is_menu and is_end):
                if l_b_down:
                    l_b_down = False
                elif r_b_down:
                    r_b_down = False

pygame.quit()
