# -*- codeing: utf-8 -*-
import pygame
from pygame.locals import *
from sys import exit
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self,imgBullet,init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = imgBullet
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_position
        self.speed = 10
    def move(self):
        self.rect.top -= self.speed
        

class Player(pygame.sprite.Sprite):
    def __init__(self,imgPlane,player_rect,init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        for i in range(len(player_rect)):
            self.image.append(imgPlane.subsurface(player_rect[i]).convert_alpha())#attention
        self.rect = player_rect[0]
        self.rect.topleft = init_position
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False
    def shoot(self, bullet_img):
        bullet = Bullet(imgBullet,self.rect.midtop)
        self.bullets.add(bullet)
    def moveUp(self):
        if self.rect.top <= 0 :
            self.rect.top =0
        else:
            self.rect.top-= self.speed
    def moveDown(self):
        if self.rect.top >= SCREEN_HIGHT - self.rect.height:
            self.rect.top = SCREEN_HIGHT - self.rect.height
            
        else:
            self.rect.top += self.speed
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed
    def moveRight(self):#attention: 有没有self.rect.right?
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        else:
            self.rect.right += self.speed
class Enemy(pygame.sprite.Sprite):
    def __init__(self,imgEnemy,imgEnemyDown,init_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = imgEnemy
        self.rect = self.image.get_rect()
        self.rect.topleft = init_position
        self.imgDown = imgEnemyDown
        self.speed = 2
        self.down_index = 0
        
        #enemy moved, border judging
    def move(self):
        self.rect.top += self.speed
        


SCREEN_WIDTH = 480
SCREEN_HIGHT = 800

#reset Game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))
pygame.display.set_caption('Plane Fight')

#load background img, gameover img, plane img,player img
imgBK= pygame.image.load('resources/image/background.png')
imgPlane = pygame.image.load('resources/image/shoot.png')
imgGameover=pygame.image.load('resources/image/gameover.png')
imgPlayer = imgPlane.subsurface(pygame.Rect(0,99,102,126))#attention: this postion has already been saved in a pack file

player_rect = []
player_rect.append(pygame.Rect(0,99,102,126))
player_rect.append(pygame.Rect(165,360,102,126))
player_rect.append(pygame.Rect(165,234,102,126))
player_rect.append(pygame.Rect(330,624,102,126))
player_rect.append(pygame.Rect(330,498,102,126))
player_rect.append(pygame.Rect(432,624,102,126))
player_position = [200,600]
player = Player(imgPlane,player_rect,player_position)

bullet_rect = pygame.Rect(1004,987,9,21)
imgBullet = imgPlane.subsurface(bullet_rect)

enemy1_rect = pygame.Rect(534,612,57,43)
imgEnemy1 = imgPlane.subsurface(enemy1_rect)
imgEnemy1Down = []
imgEnemy1Down.append(imgPlane.subsurface(pygame.Rect(267,347,57,43)))
imgEnemy1Down.append(imgPlane.subsurface(pygame.Rect(873,697,57,43)))
imgEnemy1Down.append(imgPlane.subsurface(pygame.Rect(267,296,57,43)))
imgEnemy1Down.append(imgPlane.subsurface(pygame.Rect(930,697,57,43)))
enemies1 = pygame.sprite.Group()

#attention
enemiesDown = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16

score = 0

clock = pygame.time.Clock()

running = True


while running:
    clock.tick(60)
    if not player.is_hit:
        if shoot_frequency % 15 ==0:
            player.shoot(imgBullet)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0
    if enemy_frequency % 50 == 0:
        enemy1_position = [random.randint(0,SCREEN_WIDTH - enemy1_rect.width),0]
        enemy1 = Enemy(imgEnemy1, imgEnemy1Down, enemy1_position)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0
    
    for bullet in player.bullets:
        bullet.move()
        
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)
    
    for enemy in enemies1:
        enemy.move()
        
        if pygame.sprite.collide_circle(enemy, player):
            enemiesDown.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            break
        if enemy.rect.top < 0:
            enemies1.remove(enemy)
            
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets,1,1)
    for enemy_down in enemiesDown:
        enemiesDown.add(enemy_down)

    #draw background
    screen.fill(0)
    screen.blit(imgBK, (0,0))
    
    #绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index],player.rect)
        player.img_index = int(shoot_frequency / 8)
    else:
        player.img_index = int(player_down_index / 8)
        screen.blit(player.image[player.img_index],player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False
    for enemy_down in enemiesDown:
        if enemy_down.down_index == 0 :
            pass
        if enemy_down.down_index > 7:
            enemiesDown.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.imgDown[int(enemy_down.down_index / 2)],enemy_down.rect)
        enemy_down.down_index += 1
    player.bullets.draw(screen)
    enemies1.draw(screen)
    
    #draw scroing
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score),True,(128,128,128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10,10]
    screen.blit(score_text,text_rect)
    
    #refresh screen
    pygame.display.update()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #get a key from keyboard            
    key_pressed = pygame.key.get_pressed()
    #respond to key
    if key_pressed[K_w] or key_pressed[K_UP]:
        player.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.moveDown()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.moveLeft()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.moveRight()
font = pygame.font.Font(None,48)
text = font.render('Score: '+ str(score),True,(255,0,0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(imgGameover,(0,0))
screen.blit(text,text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
        
        


        
        
        
        
        

            
