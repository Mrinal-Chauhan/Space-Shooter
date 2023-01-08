import pygame
from pygame.locals import *
import random


if True:  #Variables!!
    screen_dimen = (900,600)
    white,black,red = (255,255,255),(0,0,0),(240,0,0)
    fps = 60
    run,counter_collision,death_counter,StartScreen,GameStart,death_occured = True,True,True,True,True,False
    spaceship_velocity,bullet_velocity,ast_velocity = 4,3,2
    bullets,asteroids = [],[]
    ast_count = 0
    ast_onscreen = 5
    rand_spawn = random.randint(105,695)
    current_y = 0
    asteroid_hp = 5
    score = 0
    scores_list = []
    lifes = 3
    DEATH = pygame.USEREVENT + 1
    RETRY = pygame.USEREVENT + 2

def load():
    global background,spaceship_img,ast_img,font_score,font_endscreen1,font_endscreen2,font_startscreen,font_startscreen2,heart_img,laser_sound
    background = pygame.image.load('data/bg.png')
    background = pygame.transform.scale(background,screen_dimen) 
    spaceship_img = pygame.image.load('data/spaceship.png')
    spaceship_img = pygame.transform.scale(spaceship_img,(70,70))
    ast_img = pygame.image.load('data/asteroid.png')
    ast_img = pygame.transform.scale(ast_img,(80,80))
    heart_img = pygame.image.load('data/heart.png')
    heart_img = pygame.transform.scale(heart_img,(47,47))
    font_score = pygame.font.Font('data/font.otf',50)
    font_endscreen1 = pygame.font.SysFont('comicsans',120)
    font_endscreen2 = pygame.font.SysFont('comicsans',50)
    font_startscreen = pygame.font.Font('data/font.otf',120)
    font_startscreen2 = pygame.font.Font('data/font.otf',30)



def draw_screen(spaceship,asteroids,bullets):
    screen.blit(background,(0,0))  
    screen.blit(spaceship_img,(spaceship.x,spaceship.y))
    for ast in asteroids:
        screen.blit(ast_img,(ast[0].x,ast[0].y))
    for bullet in bullets:
        pygame.draw.rect(screen,(255,255,255),bullet)
    screen.blit(scorecard,(10,10))
    screen.blit(heart_img,(850 + (3 - lifes)*50 ,15))
    screen.blit(heart_img,(800 + (3 - lifes)*50 ,15))
    screen.blit(heart_img,(750 + (3 - lifes)*50 ,15))
    
    pygame.display.update() 

def spaceship_movement():
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and (spaceship.x - spaceship_velocity)>0:
        spaceship.x -= spaceship_velocity
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and (spaceship.x + spaceship_velocity)<830:
        spaceship.x += spaceship_velocity

def bullet_spawn(spaceship):
    for event2 in list_events:
        if event2.type == pygame.KEYDOWN:
            if event2.key == pygame.K_SPACE:
                bullet = pygame.Rect(spaceship.x + 33,spaceship.y-15,6,18)
                bullets.append(bullet)

def handle_asteroid():
    global asteroid,ast_count,rand_spawn,score,lifes
    for ast in asteroids:
        if ast[0].y >= 600:
            lifes -= 1
            ast_count -= 1
            asteroids.remove(ast)
        if ast[1] == 0:
            ast_count -= 1
            asteroids.remove(ast)
            score += 1
    if ast_count <= ast_onscreen:
        if ast_count == 0 or asteroids[-1][0].y >= 140:
            rand_spawn = random.randint(105,695)
            asteroid = pygame.Rect(rand_spawn,20,70,100)
            asteroid_data = [asteroid,asteroid_hp]
            asteroids.append(asteroid_data)
            ast_count += 1
    for ast in asteroids:
        ast[0].y += ast_velocity

def bullet_controls():
    global current_y, counter_collision
    for bullet in bullets:
        bullet.y -= 3
        for ast in asteroids:
            if ast[0].colliderect(bullet):
                ast[1] -= 1
                if counter_collision:
                    current_y = bullet.y
                    counter_collision = False
            if bullet.y == current_y - 6:
                bullets.remove(bullet)
                current_y = 0
                counter_collision = True

def scores():
    global score,scorecard
    score_display = 'SCORE:' + str(score)
    scorecard = font_score.render(score_display,True,white,black)

def life_handling():
    global lifes,ast_count
    for ast in asteroids:
        if ast[0].colliderect(spaceship):
            asteroids.remove(ast)
            ast_count -= 1
            lifes -= 1
    if lifes <= 0:
        pygame.event.post(pygame.event.Event(DEATH))

def death():
    global death_counter
    global score
    scores_list.append(score)
    score = 0
    death_counter = False
    highscore = max(scores_list)
    final_text1 = font_endscreen1.render("GAME OVER",1,white)
    final_text2 = font_score.render("HIGHSCORE:"+ str(highscore),1,red,black)
    final_text3 = font_endscreen2.render("CLICK HERE TO RETRY",1,white)
    final_text4 = font_endscreen2.render("!!NEW HIGHSCORE!!",1,red)
    screen.blit(final_text1,(450 - final_text1.get_width()/2, 200))
    screen.blit(final_text2,(900 - final_text2.get_width() ,10))
    screen.blit(final_text3,(450 - final_text3.get_width()/2,350))
    if highscore == scores_list[-1]:
        screen.blit(final_text4,(450 - final_text4.get_width()/2,300))
    pygame.event.post(pygame.event.Event(RETRY))
    pygame.display.update()


def main():
    global StartScreen,screen,spaceship,run,list_events,asteroid,scorecard,death_counter,lifes,asteroids,ast_count,bullets,GameStart,clock,death_occured

    if GameStart:
        screen = pygame.display.set_mode(screen_dimen)
        pygame.display.set_caption('Space Shooter') 
        load()

        scorecard = font_score.render('SCORE:',True,white,black)
        spaceship = pygame.Rect(365,520,70,70)
        asteroid = pygame.Rect(rand_spawn,100,100,100)
        clock = pygame.time.Clock() 
        
    while StartScreen:
        screen.blit(background,(0,0))
        startscreen_text = font_startscreen.render('SPACE SHOOTER',1,white)
        startscreen_text2 = font_startscreen2.render('Click here to Continue',1,white)
        screen.blit(startscreen_text,(450 - startscreen_text.get_width()/2, 250 - startscreen_text.get_height()/2))
        screen.blit(startscreen_text2,(450 - startscreen_text2.get_width()/2, 310))
        pygame.display.update()
        list_events2 = pygame.event.get()
        for event3 in list_events2:
            if str(event3) == '<Event(256-Quit {})>':
                pygame.quit()
            if str(event3)[0:25] == '<Event(1026-MouseButtonUp':
                StartScreen = False
    
    while run: 
        clock.tick(fps)
        list_events = pygame.event.get()

        for event in list_events:
            if event.type == pygame.QUIT:
                GameStart,death_counter,run = False,False,False
                pygame.quit()
                return()
            if event.type == DEATH:
                death()
                death_occured = True
            if death_occured:
                if event.type == pygame.MOUSEBUTTONUP:
                    run = False 

        if death_counter:
            spaceship_movement()
            life_handling()
            draw_screen(spaceship,asteroids,bullets)
            bullet_spawn(spaceship)
            bullet_controls()
            handle_asteroid()
            scores()
        
    run = True
    lifes = 3
    asteroids,bullets = [],[]
    ast_count = 0
    death_counter = True
    main()


pygame.init()
pygame.font.init()
pygame.mixer.init()
if __name__ == "__main__":
    main()
# pygame.quit()

# sounds, touchup, random asteroid size, speed if possible
