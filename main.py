import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1056, 672))
pygame.display.set_caption("Робот против охранников")
icon = pygame.image.load('import/icon.jpg').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('import/bg.png').convert_alpha()
walk_left = [
    pygame.image.load('import/player_left/robo5.png').convert_alpha(),
    pygame.image.load('import/player_left/robo6.png').convert_alpha(),
    pygame.image.load('import/player_left/robo7.png').convert_alpha(),
    pygame.image.load('import/player_left/robo8.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('import/player_right/robo1.png').convert_alpha(),
    pygame.image.load('import/player_right/robo2.png').convert_alpha(),
    pygame.image.load('import/player_right/robo3.png').convert_alpha(),
    pygame.image.load('import/player_right/robo4.png').convert_alpha(),
]

guard = pygame.image.load('import/guard.png').convert_alpha()
guard_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 10
player_x = 150
player_y = 485

is_jump = False
jump_count = 8

guard_timer = pygame.USEREVENT + 1
pygame.time.set_timer(guard_timer, 3500)

lable = pygame.font.Font('import/tektur.ttf', 40)
lose_lable = lable.render('Вы проиграли!', False, (117, 0, 0))
restart_lable = lable.render('Играть заново', False, (0, 0, 0))
restart_lable_rect = restart_lable.get_rect(topleft=(428, 400))

shots_left = 10
shot = pygame.image.load('import/shot.png').convert_alpha()
shots = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1056, 0))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if guard_list_in_game:
            for (i, el) in enumerate(guard_list_in_game):
                screen.blit(guard, el)
                el.x -= 10

                if el.x < -10:
                    guard_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 900:
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
        if bg_x == -1056:
            bg_x = 0

        if shots:
            for (i, el) in enumerate(shots):
                screen.blit(shot, (el.x, el.y))
                el.x += 4

                if el.x > 1060:
                    shots.pop(i)

                if guard_list_in_game:
                    for (index, guard_el) in enumerate(guard_list_in_game):
                        if el.colliderect(guard_el):
                            guard_list_in_game.pop(index)
                            shots.pop(i)
    else:
        screen.fill((52, 52, 52))
        screen.blit(lose_lable, (428, 300))
        screen.blit(restart_lable, restart_lable_rect)

        mouse = pygame.mouse.get_pos()
        if restart_lable_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            guard_list_in_game.clear()
            shots.clear()
            shots_left = 10

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == guard_timer:
            guard_list_in_game.append(guard.get_rect(topleft=(1060, 485)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_q and shots_left > 0:
            shots.append(shot.get_rect(topleft=(player_x + 30, player_y + 10)))
            shots_left -= 1

    clock.tick(15)