from random import randint
from pytmx.util_pygame import load_pygame

import pygame.sprite
from player import Player
from sprites import *
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.collisions_sprites = pygame.sprite.Group()
        self.setup()

        self.player = Player((400, 300), self.all_sprites, self.collisions_sprites)


    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)
            self.screen.fill((0, 0, 0))

            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    def setup(self):
        map = load_pygame('/home/oleksandra/drive/vampire-survivor/data/maps/world.tmx')
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collisions_sprites))


if __name__ == '__main__':
    game = Game()
    game.run()
