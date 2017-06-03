import pygame
from pygame.locals import *
import random
import math

pi = 3.14159

# - Initialize the game
pygame.init
width,height = 640,480
screen = pygame.display.set_mode((width,height))
keys=[False,False,False,False]

# - load resources
playerImg = pygame.image.load('resources/images/dude.png')
grassImg = pygame.image.load('resources/images/grass.png')
castleImg = pygame.image.load('resources/images/castle.png')
arrowImg = pygame.image.load('resources/images/bullet.png')
badgerImg = pygame.image.load('resources/images/badguy.png')
#shootsound = pygame.mixer.sound('resources/audio/shoot.wav')
#hitsound = pygame.mixer.sound('resources/audio/explode.wav')
#enemysound = pygame.mixer.sound('resources/audio/enemy.wav')
#hitSound.set_volume(0.06)
#enemySound.set_volume(0.1)
#shootSound.set_volume(0.06)
#pygame.mixer.music.load('resources/audio/moonlight.wav')
#pygame.mixer.music.play(-1,0.0)
#pygame.mixer.music.set_volume(0.25)
player_position_init = [100,100]
# - keep looping through
running = 1
exitCode= 0

timer = [100]
timer_temp = 0
health_value = 100
class Arrow (pygame.sprite.Sprite):
    def __init__(self,img_arrow,init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_arrow
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_position
        self.speed = 10
        self.arrows = []
        self.velx = 0
        self.vely = 0
    def draw(self):
        index = 0
        for bullet in self.arrows:
            self.velx = math.cos(bullet[0])*self.speed
            self.vely = math.sin(bullet[0])*self.speed
            bullet[1] += self.velx
            bullet[2] += self.vely
            if bullet[1] <0 or bullet [1] > screen.get_width() or bullet[2] <0 or bullet[2] > screen.get_height():
                self.arrows.pop(index)
            index += 1
            for projectile in self.arrows:
                arrow_new = pygame.transform.rotate(self.image, 360-projectile[0]*180/pi )
                screen.blit(arrow_new,(projectile[1],projectile[2]))
            
class Player(pygame.sprite.Sprite):
    def __init__(self,player_img,init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_position
    def rotate(self):
        mouse_position = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_position[1]-(self.rect.top),mouse_position[0]-(self.rect.left))
        self.new_image = pygame.transform.rotate(self.image,360-self.angle*180/pi)
        self.position = (self.rect.left-self.new_image.get_rect().width/2,self.rect.top-self.new_image.get_rect().height/2)
    def move_up(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed
    def move_down(self):
        if self.rect.top >= screen.get_rect().height:
            self.rect.top = screen.get_rect().height
        else:
            self.rect.bottom += self.speed
    def move_left(self):
        if self.rect.left <= 0 :
            self.rect.left = 0
        else:
            self.rect.left -= self.speed
    def move_right(self):
        if self.rect.left >= screen.get_rect().width:
            self.rect.left = screen.get_rect().width
        else: 
            self.rect.right += self.speed

class Badger(pygame.sprite.Sprite):
    def __init__(self,badgerImg):
        self.image = badgerImg
        #self.position = init__position
        self.badgers = []
        self.speed = 7
        self.index = 0

    def produce(self,timer):
        global timer_temp
        #input a timer, timer is a para defined in while running loop.
        if timer[0] == 0:
            self.badgers.append([screen.get_width(),random.randint(0,screen.get_height()-self.image.get_height())])
            timer[0] = 100 - timer_temp*2
            if timer_temp > 35:
                timer_temp = 35
            else:
                timer_temp+= 5
    def draw(self):
        global health_value
        for badger_temp in self.badgers:
            #successful attack
            if badger_temp[0] < 0:
                health_value -= random.randint(10,15)
                self.badgers.pop(self.index)
            # move badger
            badger_temp[0] -= self.speed
            
            
            #draw badger
            screen.blit(self.image,badger_temp)
            self.index += 1
        self.index = 0
#define three classes of player, arrow, badger
player = Player(playerImg,player_position_init)
arrow = Arrow(arrowImg,player_position_init)
badger = Badger(badgerImg)
def collision_detect(arrows,badgers):
    #input list of arrows and badgers
    index_badger = 0
    for badger in badgers:
        badger_rect = pygame.Rect(badgerImg.get_rect())
        badger_rect.top = badger[1]
        badger_rect.left = badger[0]
        index_arrow = 0
        for arrow in arrows:
            arrow_rect = pygame.Rect(arrowImg.get_rect())
            arrow_rect.top = arrow[2]
            arrow_rect.left = arrow[1]
            #arrow hit badger, score
            if badger_rect.colliderect(arrow_rect):
                badgers.pop(index_badger)
                arrows.pop(index_arrow)#attention: out of range? maybe arrow going out border and collide with badger at the same time?
            index_arrow += 1 
        index_badger += 1 
#main part of the game 
while running:
    timer[0] -= 1 
    # 5. clear screen before drawing it again
    screen.fill(0)
    # 6.1 draw the screen elements
    for x in range(int(screen.get_width()/grassImg.get_width())+1):
        for y in range(int(screen.get_height()/grassImg.get_height()+1)):
            screen.blit(grassImg,(x*grassImg.get_width(),y*grassImg.get_height()))
    screen.blit(castleImg,(0,30))
    screen.blit(castleImg,(0,135))
    screen.blit(castleImg,(0,240))
    screen.blit(castleImg,(0,345))
    #before draw player img, rotate player img according to mouse move.
    player.rotate()
    #draw player 
    screen.blit(player.new_image,player.position)
	#draw arrow(made by MOUSEBUTTONDOWN)
    arrow.draw()
    #produce badgers(badguys), according to the timer.
    badger.produce(timer)
    #collision dectection, pop out the collided arrows and badgers
    collision_detect(arrow.arrows,badger.badgers)
    #draw badgers
    badger.draw()
    


    # 7. update screen
    pygame.display.flip()
    #8 loop through events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #shootSound.play()
            mouse_position = pygame.mouse.get_pos()
            arrow.arrows.append([math.atan2(mouse_position[1]-(player.position[1]+32),mouse_position[0]-
                                            (player.position[0]+26)),player.position[0]+32,player.position[1]+32])
        key_pressed = pygame.key.get_pressed()
            # move player:  
        if key_pressed[K_w] or key_pressed[K_UP]:
                player.move_up()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.move_left()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.move_down()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.move_right()
        
        
    
    
    
    
    
    
    
