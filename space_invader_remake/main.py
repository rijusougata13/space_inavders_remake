import pygame
import os
import math
import random
import time

#initialize pygame
pygame.init()

#screen
winScreenWidth=800
winScreenHeight=600
screen = pygame.display.set_mode((winScreenWidth, winScreenHeight))
#title icon
pygame.display.set_caption('space invaders created  by fscty')

# player image
playerImg = pygame.image.load('spaceship.png')
playerX = winScreenWidth-430
playerY = winScreenHeight-120
playerX_change = 0
def player(x, y):
    screen.blit(playerImg, (x, y))
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, winScreenWidth-64))
    enemyY.append(random.randint(winScreenHeight-550, winScreenHeight-450))
    enemyX_change.append(3)
    enemyY_change.append(35)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

#bomb 
bomb_image=pygame.image.load('bomb.png')
bombX=0
bombY=50
bombX_change=0
bombY_change=5
bomb_state='ready'
def fire_bomb(x,y):
    global bomb_state
    bomb_state='fire'
    screen.blit(bomb_image,(x,y+10))

#collision detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
#bullet image
bullet_image=pygame.image.load('bullet.png')
bulletX=0
bulletY=winScreenHeight-150
bulletX_change=0
bulletY_change=4
bullet_state='ready'
def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bullet_image,(x+16,y+10))
#life
life_value=3
font=pygame.font.Font('freesansbold.ttf',50)
textX_life=300
textY_life=10
def show_life(x,y):
    life=font.render('life:'+str(life_value),True,(255,255,0))
    screen.blit(life,(x,y))



#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',22)
textX=10
textY=10
def show_score(x,y):
    score=font.render('score:'+str(score_value),True,(255,0,0))
    screen.blit(score,(x,y))

#game over
game_over_text=pygame.font.Font('freesansbold.ttf',102)
def game_over(x,y):
    over=font.render('GAME OVER :"(',True,(0,255,0))
    screen.blit(over,(x,y))
#background image
background=pygame.image.load('download.jpeg')
background=pygame.transform.scale(background, (winScreenWidth, winScreenHeight))
#game loop
running=True
while running:
    screen.fill((255,255,0))
        #background
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            running=False
        # player movement
        if event.type==pygame.KEYDOWN :
            if  event.key==pygame.K_LEFT:
                playerX_change=-2.7
            if event.key==pygame.K_RIGHT:
                playerX_change=2.7
            if event.key==pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT :
                playerX_change=0
    #player boundary check
    if(playerX<0):
        playerX=0
    if(playerX>winScreenWidth-50):
        playerX=winScreenWidth-50
    for i in range(num_of_enemies):
        if enemyY[i]>winScreenHeight-150:
            for j in range(num_of_enemies):
                enemyY[j]=2000*100
            game_over(winScreenWidth-500,winScreenHeight-300)
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= winScreenWidth-64:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
                #firing bomb
            if bomb_state is 'ready':
                bombX=enemyX[i]
                bombY=enemyY[i]
                fire_bomb(bombX,bombY)
            bulletY = winScreenHeight-120
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, winScreenWidth-64)
            enemyY[i] = random.randint(50, winScreenHeight-450)

        enemy(enemyX[i], enemyY[i], i)
    #change player pos
    playerX+=playerX_change
    
    #firing bomb
    if bomb_state is 'fire':
        fire_bomb(bombX,bombY)
        bombY+=bombY_change
    if bombY>=winScreenHeight-120:
        bombY=50
        bomb_state='ready'


    #firing bullet
    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    #multiple bullet firing
    if bulletY<=0:
        bulletY=450
        bullet_state='ready'
    #calling player
    player(playerX,playerY)
    #score
    show_score(textX,textY)    
    #life
    show_life(textX_life,textY_life)
    
    #bomb collison
    bomb_collision=isCollision(playerX, playerY, bombX-10, bombY)
    if bomb_collision:
        life_value-=1
        bombY=50
        bomb_state='ready'
        if life_value==0:
            for j in range(num_of_enemies):
                enemyY[j]=2000*100
                game_over(winScreenWidth-500,winScreenHeight-300)
                break

    #showing all update
    pygame.display.update()
