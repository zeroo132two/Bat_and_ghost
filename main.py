import pygame
import random

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((734, 367))
pygame.display.set_caption("Летучая мышь против привидений")
icon = pygame.image.load('import/icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('import/forest.jpg').convert_alpha()
walk_left = [
    pygame.image.load('import/bat_left/bat5.png').convert_alpha(),
    pygame.image.load('import/bat_left/bat6.png').convert_alpha(),
    pygame.image.load('import/bat_left/bat7.png').convert_alpha(),
    pygame.image.load('import/bat_left/bat8.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('import/bat_right/bat1.png').convert_alpha(),
    pygame.image.load('import/bat_right/bat2.png').convert_alpha(),
    pygame.image.load('import/bat_right/bat3.png').convert_alpha(),
    pygame.image.load('import/bat_right/bat4.png').convert_alpha(),
]

ghost = pygame.image.load('import/ghost.png').convert_alpha()
ghost_list_in_game = []
ghost_health = {}

player_anim_count = 0
bg_x = 0

player_speed = 7
player_x = 50
player_y = 210

is_jump = False
jump_count = 8

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

cloud_timer = pygame.USEREVENT + 2
pygame.time.set_timer(cloud_timer, 3000)

lable = pygame.font.Font('import/press.ttf', 25)
score_lable_font = pygame.font.Font('import/press.ttf', 20)

lose_lable = lable.render('Вы проиграли!', False, (180, 0, 0))
restart_lable = lable.render('Начать заново', False, (0, 0, 0))
exit_lable = lable.render('Выйти', False, (0, 0, 0))

restart_lable_rect = restart_lable.get_rect(center=(734 // 2, 180))
exit_lable_rect = exit_lable.get_rect(topleft=(734 // 2, 220))

play_lable = lable.render('Играть', False, (0, 0, 0))
quit_lable = lable.render('Выход', False, (0, 0, 0))

play_lable_rect = play_lable.get_rect(topleft=(320, 140))
quit_lable_rect = quit_lable.get_rect(topleft=(320, 180))

shots_left = 5
shot = pygame.image.load('import/shot.png').convert_alpha()
shots = []

score = 0
lives = 3

heart = pygame.image.load('import/heart.png').convert_alpha()

gameplay = True
out_of_ammo_start = None
menu = True
victory = False


#препядствия
obstacles = []  # Список препятствий
obstacle_timer = pygame.USEREVENT + 3
pygame.time.set_timer(obstacle_timer, 4000)
obstacle_image = pygame.image.load('import/cloud.png').convert_alpha()


running = True
while running:

    if menu:
        screen.fill((124, 180, 216))

        screen.blit(play_lable, play_lable_rect)
        screen.blit(quit_lable, quit_lable_rect)

        mouse = pygame.mouse.get_pos()
        if play_lable_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            menu = False
            gameplay = True
            score = 0
            lives = 3
            shots_left = 5
            shots.clear()
        if quit_lable_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False
            pygame.quit()


    elif victory:
        screen.fill((17, 13, 61))

        win_lable = lable.render('Вы победили!', False, (255, 255, 255))
        screen.blit(win_lable, (734 // 2 - win_lable.get_width() // 2, 100))

        main_menu_label = lable.render('Главное меню', False, (0, 0, 0))
        main_menu_rect = main_menu_label.get_rect(center=(734 // 2, 200))
        screen.blit(main_menu_label, main_menu_rect)

        mouse = pygame.mouse.get_pos()
        if main_menu_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            victory = False
            menu = True
            shots.clear()



    elif gameplay:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 734, 0))

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        score_text = score_lable_font.render(f'Баллов: {score}', True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        ammo_text = score_lable_font.render(f'Снарядов: {shots_left}', True, (255, 255, 255))
        screen.blit(ammo_text, (20, 50))

        for i in range(lives):
            screen.blit(heart, (20 + i * 40, 80))



        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 15



                if el.x < -10:
                    ghost_list_in_game.pop(i)


                if player_rect.colliderect(el):
                    ghost_list_in_game.pop(i)

                    lives -= 1
                    if lives <= 0:
                        gameplay = False
        if obstacles:
            for i, obstacle in enumerate(obstacles):
                screen.blit(obstacle_image, obstacle)
                obstacle.x -= 7

                if obstacle.x < -50:
                    obstacles.pop(i)

                if player_rect.colliderect(obstacle):
                    lives -= 1
                    obstacles.pop(i)
                    if lives <= 0:
                        gameplay = False

        if shots:
            for i, el in enumerate(shots):
                screen.blit(shot, (el.x, el.y))
                el.x += 8

                if el.x > 740:
                    shots.pop(i)

                if ghost_list_in_game:
                    for index, ghost_el in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_id = id(ghost_el)

                            if ghost_el in ghost_list_in_game:
                                ghost_list_in_game.pop(index)
                                shots.pop(i)
                                score += 100
                                shots_left += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 300:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -734:
            bg_x = 0

        if shots_left == 0:
            if out_of_ammo_start is None:
                out_of_ammo_start = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - out_of_ammo_start >= 5000:
                gameplay = False
        else:
            out_of_ammo_start = None

        if score >= 1000:
            gameplay = False
            victory = True
    else:
        screen.fill((17, 13, 61))
        if shots_left == 0 and out_of_ammo_start is not None:
            out_of_ammo_text = lable.render('Снаряды кончились,вы проиграли', True, (180, 0, 0))
            screen.blit(out_of_ammo_text, (734 // 2 - out_of_ammo_text.get_width() // 2, 150))
        else:
            screen.blit(lose_lable, (734 // 2 - lose_lable.get_width() // 2, 100))

        screen.blit(restart_lable, restart_lable_rect)
        screen.blit(exit_lable, exit_lable_rect)

        mouse = pygame.mouse.get_pos()
        if restart_lable_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            shots.clear()
            shots_left = 5
            score = 0
            lives = 3
            out_of_ammo_time = None
        if exit_lable_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            running = False
            pygame.quit()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            new_guard = ghost.get_rect(topleft=(740, 210))
            ghost_list_in_game.append(new_guard)
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_q and shots_left > 0:
            shots.append(shot.get_rect(topleft=(player_x + 30, player_y + 10)))
            shots_left -= 1
        if event.type == obstacle_timer:
            new_obstacle = obstacle_image.get_rect(topleft=(740, 210))
            obstacles.append(new_obstacle)

    clock.tick(15)