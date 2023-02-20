import pygame
from entity import Entity


class Coffin(Entity):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(pos, groups, path, collision_sprites)
        
   
class Cactus(Entity):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(pos, groups, path, collision_sprites)