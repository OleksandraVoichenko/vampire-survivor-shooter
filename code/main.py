from random import choice
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
        self.enemy_sprites = pygame.sprite.Group()

        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_pos = []

        self.load_images()
        self.setup()


    def load_images(self):
        self.bullet_surf = pygame.image.load(join('..', 'images', 'gun', 'bullet.png')).convert_alpha()

        folders = list(walk(join('..', 'images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('..', 'images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)


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
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_pos), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collisions_sprites)

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
            else:
                self.spawn_pos.append((obj.x, obj.y))


if __name__ == '__main__':
    game = Game()
    game.run()
