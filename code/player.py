import pygame
import sys
from pygame.math import Vector2 as vector
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, collision_sprites, create_bullet):
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
        self.hittbox =  self.rect.inflate(-self.rect.width*0.6, -self.rect.height*0.6)
        self.collisions_sprites = collision_sprites
        
        # attack
        self.attacking = False
        
        self.create_bullet = create_bullet
        self.bullet_shoot =  False
        
    
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
                    self.animations[key].append(surf)
        
    def input(self):
        keys =  pygame.key.get_pressed()
        
        if not self.attacking:
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
                
            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = vector()
                self.frame_index = 0
                self.bullet_shoot = False
                
                match self.status.split('_')[0]:
                    case 'left':
                        self.bullet_direction = vector(-1, 0)
                    case 'right':
                        self.bullet_direction = vector(1, 0)
                    case 'up':
                        self.bullet_direction = vector(0, -1)
                    case 'down':
                        self.bullet_direction = vector(0, 1)
                
    def get_status(self):
        
        # idle
        if self.direction.x == 0 and self.direction.y == 0 and not self.attacking:
            self.status =  self.status.split("_")[0] + "_idle"
        # attacking
        if self.attacking:
            self.status =  self.status.split("_")[0] + "_attack"
         
    def move(self, dt):
        # normalize vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hittbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hittbox.centerx
        self.collision("horizontal")
        
        
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hittbox.centery = round(self.pos.y)
        self.rect.centery =  self.hittbox.centery
        self.collision("vertical")
                
    def animate(self, dt):
        current_animation = self.animations[self.status]
        
        self.frame_index += 7 * dt
        
        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shoot:
            bullet_start_pos = self.rect.center + self.bullet_direction * 75
            
            self.create_bullet(pos=bullet_start_pos, direction=self.bullet_direction, up_down=self.status)
            self.bullet_shoot = True
        
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
                
        self.image = current_animation[int(self.frame_index)]
        
    def collision(self, direction):
        for sprite in self.collisions_sprites.sprites():
            if sprite.hittbox.colliderect(self.hittbox):
                if direction == "horizontal":
                    if self.direction.x > 0: # moving right
                        self.hittbox.right =  sprite.hittbox.left
                    if self.direction.x < 0: # moving left
                        self.hittbox.left = sprite.hittbox.right
                    self.pos.x = self.hittbox.centerx
                    self.rect.centerx = self.hittbox.centerx
                else:        
                    if self.direction.y > 0: # move down
                        self.hittbox.bottom = sprite.hittbox.top
                    if self.direction.y < 0:#move up
                        self.hittbox.top = sprite.hittbox.bottom
                    self.pos.y = self.hittbox.centery
                    self.rect.centery = self.hittbox.centery
        
    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)