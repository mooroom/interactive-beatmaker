import pygame, random, math
from pygame.locals import *

pygame.init()

white = (255, 255, 255, 50)
black = (0, 0, 0)
grey_off = Color('#212121')
grey = Color('#424242')

green_off = Color('#417015')
green = Color('#81E029')

red_off = Color('#7F160F')
red = Color('#FE2C1E')

blue_off = Color('#006C5D')
blue = Color('#00D8B9')

screen = pygame.display.set_mode((1300, 800))
clock = pygame.time.Clock()

graphic_display = Rect(300,0,1000,500)

# class Graphic(pygame.sprite.Sprite):
#     def __init__(self, color, rect):
#         pygame.sprite.Sprite.__init__(self)

class Pulse(pygame.sprite.Sprite):
    def __init__(self, rect, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([rect.width, rect.height])
        self.rect = rect
        self.color = color
        self.radius = 0
        self.thickness = 1

        self.delta = 4

    def speedUp(self, delta):
        self.delta += delta

    def speedDown(self, delta):
        self.delta -= delta

    def changeColor(self, color):
        self.color = color

    def changeThickness(self, thickness):
        self.thickness = thickness

    def update(self):
        self.radius += self.delta
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, self.thickness)
        print(self.image.get_rect())

        if(self.radius > 300):
            self.kill()

# class Pulse_A(Pulse):
#     def __init__(self, center):
#         Pulse.__init__(se)

pulses = pygame.sprite.Group()
colorTypes = (red, blue, green)

def game_loop():

    

    # pulse1 = Pulse(Rect(500,250,10,10), red)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys=pygame.key.get_pressed()
        
        if keys[K_RIGHT]:
            pulses.add(Pulse(Rect(random.randint(0,1300),random.randint(0,800),0,0), red))
        if keys[K_LEFT]:
            for pulse in pulses:
                pulse.speedUp(random.randint(4,8))
        if keys[K_UP]:
            for pulse in pulses:
                pulse.changeThickness(random.randint(1,10))
        if keys[K_DOWN]:
            for pulse in pulses:
                pulseColor = random.choice(colorTypes)
                pulse.changeColor(pulseColor)

        screen.fill(black)
        
        # pulses.draw(screen)
        pulses.update()
        # pygame.draw.rect(screen, green, graphic_display)
        pygame.display.update()
        clock.tick(30)

game_loop()