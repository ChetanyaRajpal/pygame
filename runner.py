import pygame
from sys import exit
from random import randint

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= randint(4, 6)
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# Audio
jump_sound = pygame.mixer.Sound("audio/jump.mp3")
pygame.mixer.music.load('audio/music.wav')
pygame.mixer.music.set_volume(0.5)  # Adjust volume if needed

# Background
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = text_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = text_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 320))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


pygame.mixer.music.play(loops=-1) 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    jump_sound.play()
                    player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            if event.type == snail_animation_timer:
                snail_frame_index = 1 - snail_frame_index  # Toggle between 0 and 1
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                fly_frame_index = 1 - fly_frame_index  # Toggle between 0 and 1
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                obstacle_rect_list.clear()
                player_rect.midbottom = (80, 300)

    # Game Logic
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player Movement
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision Detection
        game_active = collision(player_rect, obstacle_rect_list)

        if score % 10 == 0:
            pygame.time.set_timer(obstacle_timer, max(1000, 2000 - (score // 10) * 100))

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        score_message = text_font.render(f'Your Score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(score_message if score > 0 else game_message, score_message_rect)

        # ✅ Stop obstacles when game is over
        pygame.time.set_timer(obstacle_timer, 2000) 

    pygame.display.update()
    clock.tick(60)
