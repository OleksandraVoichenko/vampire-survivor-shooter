import pygame.sprite
from player import Player
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()

        self.player = Player((400, 300), self.all_sprites)

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




if __name__ == '__main__':
    game = Game()
    game.run()
