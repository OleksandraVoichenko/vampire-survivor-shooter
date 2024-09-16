from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('/home/oleksandra/drive/vampire-survivor/images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.dir = pygame.Vector2()
        self.speed = 300

    def input(self):
        keys = pygame.key.get_pressed()
        self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.dir = self.dir.normalize() if self.dir else self.dir

    def move(self, dt):
        self.rect.center += self.dir * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)