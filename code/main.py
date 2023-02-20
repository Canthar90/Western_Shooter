import pygame, sys
from settings import * 
from pygame.math import Vector2 as vector
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite


class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load(r"graphics\other\bg.png").convert()
        
    def customize_draw(self, player):
        
        # change the offset vector 
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2
        
        # blit the surfaces 
        # bg
        self.display_surface.blit(self.bg, -self.offset)
        # sprites inside of the group (player)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Western shooter')
		self.clock = pygame.time.Clock()
  
		# group
		self.all_sprites = Allsprites()
		self.setup()
  
	def setup(self):
		tmx_map = load_pygame("data\map.tmx")
  
		# tiles
		for x, y, surf in tmx_map.get_layer_by_name('fence').tiles():
			Sprite(pos=(x*64,y*64), surf=surf, groups=self.all_sprites)
		
  
		# objects
		for obj in tmx_map.get_layer_by_name('objects'):
			Sprite((obj.x, obj.y), obj.image, self.all_sprites)
   
		# entities
		for obj in tmx_map.get_layer_by_name("entities"):
			if obj.name == "Player":
				self.player = Player((obj.x, obj.y), self.all_sprites, PATHS['player'], None)

	def run(self):
		while True:
			# event loop 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			dt = self.clock.tick() / 1000
   
			# update groups
			self.all_sprites.update(dt)
			# draw groups
			self.display_surface.fill("black")
			self.all_sprites.customize_draw(self.player)

			pygame.display.update()    

if __name__ == '__main__':
	game = Game()
	game.run()