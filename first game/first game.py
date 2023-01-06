import pygame
import random
import math
from pygame import mixer

pygame.init()

#---------------------- Creat screen ----------------------# 
screen = pygame.display.set_mode((800 , 600))
#---------------------- Backgroung ----------------------#  
background = pygame.image.load('back_ground.jpg')
#---------------------- Backgroung  sound----------------------# 
mixer.music.load('background.wav')
mixer.music.play(-1)
#---------------------- Titel and Icon ----------------------# 
pygame.display.set_caption("Space Invanders")
icon = pygame.image.load('space-ship.png')
pygame.display.set_icon(icon)
#---------------------- Score ----------------------#
score_value = 0
font = pygame.font.Font('freesansbold.ttf' , 32)
textX = 10 
textY = 10 
def show_score (x , y ):
    score = font.render('Score: ' + str(score_value) , True , (255 , 255 , 255))
    screen.blit(score , (x , y))
#---------------------- game over  ----------------------#
game_over_font = pygame.font.Font('freesansbold.ttf' , 64)
def game_over_text ():
    over_text = game_over_font.render( "Game over :( ", True , (255 , 255 , 255))
    screen.blit(over_text , (200 ,250 ))
#---------------------- Player ----------------------# 
playerimg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0 
def player(x , y):
   screen.blit(playerimg , (x , y)) 

#---------------------- Enemy ----------------------# 
enemyimg = []
EnemyX = []
EnemyY=[]
EnemyX_change = []
EnemyY_change = []
num_of_enemies = 6 
for i in range(num_of_enemies):

    enemyimg.append(pygame.image.load('alien.png'))
    EnemyX.append(random.randint(0 , 735))
    EnemyY.append(random.randint(50 , 150))
    EnemyX_change.append(0.2)  
    EnemyY_change.append(20) 

def enemy(x , y , i):
    screen.blit(enemyimg[i] , (x , y)) 


#---------------------- bullet ----------------------# 
# ready = you can not see the bullet 
# fire = the bullet is moving 
bulletimg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletX_change = 0 
bulletY_change = 0.9 
bullet_state = 'ready'
def fire_bullet(x , y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg , (x+16 , y+10 ))

#---------------------- collision ----------------------# 
def isCollsion(enemyX , enemyY , bulletX , bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX , 2)) + (math.pow(enemyY - bulletY , 2)))
    if distance < 27 :
        return True
    else:
        return False

#====================== Game loop ======================#
running = True
while running:
#---------------------- Change the color ----------------------# 
    screen.fill((100,150,50))

#---------------------- background image ----------------------#  
    screen.blit(background , (0 , 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#---------------------- press the key left or right or space ----------------------#    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0 
#---------------------- press the key up or down ----------------------# 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5              
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0 
#---------------------- press space ----------------------# 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound =mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX , bulletY)

#---------------------- Call the ship ----------------------# 
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0 :
        playerX = 0 
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0 :
        playerY = 0 
    elif playerY >= 536:
        playerY = 536
    player(playerX , playerY)

#---------------------- Call the enemy ----------------------# 
    
    for i in range (num_of_enemies):
        #Game over 
        if EnemyY[i] > 440 :
            for j in range (num_of_enemies):
              EnemyY[j] = 2000  
            game_over_text()
            break
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0 :
            EnemyX_change[i] = 0.2 
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -0.2
            EnemyY[i] += EnemyY_change[i]
#---------------------- collison ---------------------- #  
        collision = isCollsion(EnemyX[i] , EnemyY[i]  , bulletX , bulletY)
        if collision:
            explosion_sound =mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            EnemyX[i] = random.randint(0 , 735)
            EnemyY[i] = random.randint(50 , 150)  
        enemy(EnemyX[i] , EnemyY[i] , i )  
#---------------------- bullet movment ----------------------# 
    if bulletY <= 0 :
        bullet_state = 'ready'
    if bullet_state is 'fire': 
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change

    
#---------------------- update changes in game ----------------------# 
    show_score(textX , textY)
    pygame.display.update()
