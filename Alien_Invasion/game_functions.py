
import sys
import os
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien
import json

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responde a pressionamentos de tecla"""

    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        #Finaliza o jogo ao pressionar Q ou ESC
        sys.exit()

    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    if event.key == pygame.K_RIGHT:
        #Move a espaçonave para a direita
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        #Move a espaçonave para a esquerda
        ship.moving_left = True

    elif event.key == pygame.K_UP:
        #Move a espaçonave para cima
        ship.moving_up = True

    elif event.key == pygame.K_DOWN:
        #Move a espaçonave para baixo
        ship.moving_down = True


def check_keyup_events(event, ship):
    """Responde quando a tecla for solta"""

    if event.key == pygame.K_RIGHT:
        #Para o movimento da espaçonave para a direita
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        #Para o movimento da espaçonave para a esquerda
        ship.moving_left = False

    elif event.key == pygame.K_UP:
        #Para o movimento da espaçonave para cima
        ship.moving_up = False

    elif event.key == pygame.K_DOWN:
        #Para o movimento da espaçonave para baixo
        ship.moving_down = False
    

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responde a eventos de pressionamento de teclas e de mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, 
                              ship, aliens, bullets, mouse_x, mouse_y)
        

def check_play_button(ai_settings, screen, stats, sb, play_button, 
                      ship, aliens, bullets, mouse_x, mouse_y):
    """Inicia um novo jogo quando o jogador clicar em play"""
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Inicia os atributos para o game"""

    #Reinicia a velocidade do jogo
    ai_settings.initialize_dynamic_settings()

    #Oculta o cursor do mouse
    pygame.mouse.set_visible(False)

    #Reinicia os dados estatísticos do jogo
    stats.reset_stats()
    stats.game_active = True
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ship()

    #Esvazia a lista de aliens e de projéteis
    aliens.empty()
    bullets.empty()

    #Cria uma nova frota e centraliza a espaçonave
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responde ao fato de a espaçonave ter sido atingida por um alien"""
    #Decrementa ship_left
    if stats.ships_left > 0:
        #Decrementa ships_left
        stats.ships_left -=1

        #Atualiza o painel de pontuações
        sb.prep_ship()

        #Esvazia a lista de aliens e de projéteis
        aliens.empty()
        bullets.empty()

        #Cria uma nova frota e centraliza a espaçonave
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)

        #Faz uma pausa
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)



def fire_bullet (ai_settings, screen, ship, bullets):
    """Dispara um projétil se o limite ainda não foi atingido"""
    #Cria um novo projétil e o adiciona ao grupo de projéteis
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Atualiza a posição dos projéteis e se livra dos projéteis antigos"""

    #Atualiza as posiçoes dos projéteis
    bullets.update()

    #Livra-se dos projéteis que desapareceram da tela
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    
    #Verifica se algum projétil atingiu os aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.aliens_points*len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    

    if len(aliens) == 0:
        #Destrói os projéteis existentes, aumenta a velocidade do jogo,
        # cria uma nova frota e inicia um novo nivel
        bullets.empty()
        ai_settings.increase_speed()
        stats.score += ai_settings.aliens_points*10
        sb.prep_score()
        stats.level +=1
        sb.prep_level()
        check_high_score(stats, sb)
        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    """ Verifica se há uma nova pontuação máxima."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        filename = 'Alien_Invasion/record.json'
        with open (filename, 'w') as f_obj:
            json.dump(stats.high_score, f_obj)
        sb.prep_high_score()


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #Cria um alien e o posiciona na linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = float(alien_width + 1.5 * alien_width * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_aliens_x(ai_settings, alien_width):
    """Determina o número de alienígenas que cabem em uma linha"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (1.5 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina o número de linhas com aliens que cabem na tela."""
    available_space_y = (ai_settings.screen_height - (3* alien_height) - ship_height)
    number_rows = int(available_space_y/(1.5* alien_height))
    return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
    """Cria uma frota completa de aliens"""
    #Cria um alien e calcula o número de aliens em uma linha
    #O espaçamento entre os aliens é igual a meia largura de um alien

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
 
    #Cria a frota completa
    for row_number in range(number_rows):
            #Cria a primeira linha de aliens
        for alien_number in range(number_aliens_x):
            #Cria um alien e o posiciona na linha
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Responde apropriadamente se algum alien alcançar uma borda"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Faz toda a frota descer e muda a sua posição"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Verifica se algum alien alcançou a parte inferior da tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Trata esse caso do mesmo modo que é feito quando a espaçonave é atingida
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Atualiza as posições de todos os aliens da frota"""
    check_fleet_edges (ai_settings, aliens)
    aliens.update()

    #Verifica se houve colisões entre aliens e a espaçonave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    #Verifica se há algum alien que atingiu a parte inferior da tela
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_screen (ai_settings, screen, stats, sb, ship, 
                   aliens, bullets, play_button):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    screen.fill(ai_settings.bg_color)
    ai_settings.clock = pygame.time.Clock()

    #Desenha a pontuação
    sb.show_score()

    #Redesenha todos os projéteis atrás da espaçonave e dos alienígenas
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    aliens.draw(screen)
    ship.blitme()
    ai_settings.clock.tick(400)

    #Desenha o botão 'Play' se o jogo estiver inativo
    if not stats.game_active:
        play_button.draw_button()

    #Deixa a tela mais recente visível
    pygame.display.flip()


    

