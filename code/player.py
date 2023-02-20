import pygame
import sys
from pygame.math import Vector2 as vector
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(groups)
        self.import_assets(path)
        self.frame_index = 0
        self.status = 'down_idle'
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        
        # float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 300
        
        # collisions
        self.hittbox =  self.rect.inflate(0, -self.rect.height/2)
        self.collisions_sprites = collision_sprites
        
    
    def import_assets(self, path):
        self.animations = {}
        
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    loc_path = folder[0].replace("\\", "/") + "/" + name
                    surf = pygame.image.load(loc_path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    print(key + " " + name)
                    self.animations[key].append(surf)
        print(self.animations)
        
        
    def input(self):
        keys =  pygame.key.get_pressed()
        
        # horizontal input
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        else:
            self.direction.x = 0

        # vertical input
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0
        
    def move(self, dt):
        # normalize vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hittbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hittbox.centerx
        
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hittbox.centery = round(self.pos.y)
        self.rect.centery =  self.hittbox.centery
                
    def animate(self, dt):
        current_animation = self.animations[self.status]
        print(self.status)
        
        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
        
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)