import pygame
from random import randint

def score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    game_score = text.render(f'{current_time}', False, (0, 0, 0))
    score_rect = game_score.get_rect(center = (400, 50))
    screen.blit(game_score, score_rect)

def enemies(enemy_list):
    if enemy_list:
        for enemy in enemy_list:
            enemy.x -= 5

            if enemy.bottom == 305: screen.blit(skeleton, enemy)
            else: screen.blit(orc, enemy)

        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
        return enemy_list
    else: return []

def collisions(player, enemy):
    if enemy:
        for enemy_rect in enemy:
            if player.colliderect(enemy_rect): return False
    return True

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Game 1")
clock = pygame.time.Clock()

gravity = 0
game_active = True
start_time = 0

text = pygame.font.SysFont('comicsansms', 60)
background = pygame.image.load('assets/Bg/Background_2.png').convert()
ground = pygame.image.load('assets/Bg/ground.png').convert_alpha()
game_over = pygame.image.load('assets/Knight/gameover.png')
player = pygame.image.load('assets/Knight/knightidle.png').convert_alpha()
skeleton = pygame.image.load('assets/Knight/skeletonidle.png').convert_alpha()
orc = pygame.image.load('assets/Knight/orcidle.png').convert_alpha()

player_rect = player.get_rect(midbottom=(80, 305))
skele_rect = skeleton.get_rect(midbottom=(500, 305))
orc_rect = orc.get_rect(midbottom=(500, 210))

enemies_list = []

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

while True:
    clock.tick(60)  
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
    
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 305:
                    gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    skele_rect.right = 800
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                enemies_list.append(skeleton.get_rect(bottomright = (randint(900, 1000), 305)))
            else:
                enemies_list.append(orc.get_rect(bottomright = (randint(900, 1000), 210)))

        

    if game_active:

        screen.blit(background, (0, 0))
        screen.blit(ground, (0, 0))

        # gravity cycle
        gravity += 1    # gravity increases
        player_rect.y += gravity    # gravity is added to the y position to initiate a "jump"
        if player_rect.bottom >= 305: player_rect.bottom = 305 # to prevent player from sliding through the ground
        screen.blit(player, player_rect)
        


#        skele_rect.x -= 5
#        if skele_rect.right < 0: skele_rect.left = 900
#        screen.blit(skeleton, skele_rect)

        score()
        
        enemies_list = enemies(enemies_list)

        game_active = collisions(player_rect, enemies_list)

    else:
        screen.blit(game_over, (0, 0))
        enemies_list.clear()



    pygame.display.update()
    