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
        self.bullet_sprites = pygame.sprite.Group()
        self.setup()
        self.load_images()

        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_pos = []


    def load_images(self):
        self.bullet_surf = pygame.image.load(join('..', 'images', 'gun', 'bullet.png')).convert_alpha()


    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_dir * 50
            Bullet(self.bullet_surf, pos, self.gun.player_dir, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()


    def gun_timer(self):
        if not self.can_shoot:
            curr_time = pygame.time.get_ticks()
            if curr_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True


    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.gun_timer()
            self.input()
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
                self.gun = Gun(self.player, self.all_sprites)


if __name__ == '__main__':
    game = Game()
    game.run()
