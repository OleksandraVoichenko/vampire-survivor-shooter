import pygame.sprite
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from player import Player
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = None
        self.all_sprites = AllSprites()
        self.collisions_sprites = pygame.sprite.Group()
        self.setup()


    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)
            self.screen.fill((0, 0, 0))

            self.all_sprites.draw(self.player.rect.center)
            pygame.display.flip()

        pygame.quit()


    def setup(self):
        game_map = load_pygame(join('..', 'data', 'maps', 'world.tmx'))
        for x, y, image in game_map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), image, self.all_sprites)

        for obj in game_map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collisions_sprites))

        for obj in game_map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collisions_sprites)

        for obj in game_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collisions_sprites)


if __name__ == '__main__':
    game = Game()
    game.run()
