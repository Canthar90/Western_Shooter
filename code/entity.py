import pygame
from pygame.math import Vector2 as vector
from os import walk
from math import sin


class Entity(pygame.sprite.Sprite):
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
        self.hittbox =  self.rect.inflate(-self.rect.width*0.6, -self.rect.height*0.6)
        self.collisions_sprites = collision_sprites
        self.mask = pygame.mask.from_surface(self.image)
        
        # attack
        self.attacking = False
        self.damage_sound = pygame.mixer.Sound("sound\hit.mp3")
        self.damage_sound.set_volume(0.6)
        
        self.health = 3
        self.is_vurnable = True
        self.hit_time = 0
        
    
    def blink(self):
        if not self.is_vurnable and self.wave_value():
            mask =  pygame.mask.from_surface(self.image)
            white_surf =  mask.to_surface()
            white_surf.set_colorkey((0,0,0))
            self.image = white_surf
            
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False
        
    def damage(self):
        if self.is_vurnable:
            self.health -= 1
            self.is_vurnable = False
            self.hit_time =  pygame.time.get_ticks()
            self.damage_sound.play()
                    
    def check_death(self):
        if self.health <= 0:
            self.kill()
                
    def invincibility_timer(self):
        if not self.is_vurnable:
            current_time = pygame.time.get_ticks()
            
            if current_time -  self.hit_time > 400:
                self.is_vurnable = True
        
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