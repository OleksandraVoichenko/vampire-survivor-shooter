from math import atan2, degrees

import pygame.sprite

from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)


class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        self.player = player
        self.distance= 140
        self.player_dir = pygame.Vector2(1, 0)

        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('..', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center=self.player.rect.center + self.player_dir * self.distance)


    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_dir = (mouse_pos - player_pos).normalize()


    def rotate_gun(self):
        angle = degrees(atan2(self.player_dir.x, self.player_dir.y)) - 90
        if self.player_dir.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)


    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_dir * self.distance


class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.bullet_dir = direction
        self.speed = 1200
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

    def update(self, dt):
        self.rect.center += self.bullet_dir * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= 1000:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player

        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6

        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.enemy_dir = pygame.Vector2()
        self.speed = 300


    def animate(self, delta_t):
        self.frame_index += self.animation_speed * delta_t
        self.image = self.frames[int(self.frame_index) % len(self.frames)]


    def move(self, delta_t):
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.enemy_dir = (player_pos - enemy_pos).normalize()

        self.rect.center += self.enemy_dir * self.speed * delta_t


    def update(self, dt):
        self.move(dt)
        self.animate(dt)