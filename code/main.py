import pygame, sys
from settings import * 
from pygame.math import Vector2 as vector
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet
from monster import Coffin, Cactus


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
		self.bullet_surf = pygame.image.load("graphics\other\particle.png").convert_alpha()
  
		# groups
		self.all_sprites = Allsprites()
		self.obstacles = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.monsters = pygame.sprite.Group()
  
		self.setup()
		self.music = pygame.mixer.Sound("sound\music.mp3")
		self.music.play(loops=-1)
		self.shoot =  pygame.mixer.Sound(r"sound\bullet.wav")
  
	def create_bullet(self, pos, direction, up_down):
		self.shoot.play()
		Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets], up_down)

	def bullet_collision(self):
		if pygame.sprite.spritecollide(self.player, self.bullets,
                                 True, pygame.sprite.collide_mask):
			self.player.damage()
		
		for sprite in self.obstacles:
			pygame.sprite.spritecollide(sprite, self.bullets,
                               True, pygame.sprite.collide_mask)
   
		for bullet in self.bullets:
			collide_sprite = pygame.sprite.spritecollide(bullet, self.monsters, 
                                                False, pygame.sprite.collide_mask)
			if collide_sprite:
				bullet.kill()
				for sprite in collide_sprite:
					sprite.damage()
				
	def setup(self):
		tmx_map = load_pygame("data\map.tmx")
  
		# tiles
		for x, y, surf in tmx_map.get_layer_by_name('fence').tiles():
			Sprite(pos=(x*64,y*64), surf=surf, groups=[self.all_sprites, self.obstacles])
		
  
		# objects
		for obj in tmx_map.get_layer_by_name('objects'):
			Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])
   
		# entities
		for obj in tmx_map.get_layer_by_name("entities"):
			if obj.name == "Player":
				self.player = Player(pos=(obj.x, obj.y), groups=self.all_sprites, 
                         path=PATHS['player'], collision_sprites=self.obstacles,
                         create_bullet = self.create_bullet)
    
			if obj.name == 'Coffin':
				Coffin(pos=(obj.x, obj.y), groups=[self.all_sprites, self.monsters],
           				path=PATHS['coffin'], collision_sprites=self.obstacles,
               			player=self.player)
    
			if obj.name == "Cactus":
				Cactus(pos=(obj.x, obj.y), groups=[self.all_sprites, self.monsters],
           				path=PATHS['cactus'], collision_sprites=self.obstacles,
               			player=self.player,
                  		create_bullet=self.create_bullet)

	def run(self):
		while True:
			# event loop 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			dt = self.clock.tick(200) / 1000
   
			# update groups
			self.all_sprites.update(dt)
			self.bullet_collision()
			# draw groups
			self.display_surface.fill("black")
			self.all_sprites.customize_draw(self.player)

			pygame.display.update()    

if __name__ == '__main__':
	game = Game()
	game.run()