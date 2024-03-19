import pygame, sys, os
import game_window as WIN
import entity_classes as ENTITY
from battle_menu import Battle
import pygame.event as EVENTS


pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("debug: player actions")
clock = pygame.time.Clock()

# Sprite Groups
game_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
sword_sprite = pygame.sprite.Group()

# Player Entity
player = ENTITY.Player()
game_sprites.add(player)

# Mob Entities
for i in range(5):
    dummy_wraith = ENTITY.Mob()
    dummy_wraith.set_speed(0, 0)
    game_sprites.add(dummy_wraith)
    mob_sprites.add(dummy_wraith)

# Sword Entity
sword = ENTITY.Sword()
game_sprites.add(sword)
sword_sprite.add(sword)

# Game Loop
looping = True
while looping:
    clock.tick(WIN.FPS)
    # Input Events
    for event in EVENTS.get():
        if event.type == pygame.KEYDOWN:
            # Escape Key
            if event.key == pygame.K_ESCAPE:
                WIN.game_exit()
            # G key
            if event.key == pygame.K_g:
                # Access Sword Menu
                if player.access_sword() is not None:
                    access = Battle(player)
                    access.sword_menu()
        # check click on window exit button
        if event.type == pygame.QUIT:
            WIN.game_exit()
    # 'updating' the game
    # update all game sprites
    game_sprites.update()

    # Player and Mob collision
    player_mob_collide = pygame.sprite.spritecollide(player, mob_sprites, False)
    if player_mob_collide:
        combat = Battle(player, player_mob_collide)
        remaining_mob = combat.combat_screen()
        if remaining_mob:
            # Run away was chosen
            # TODO make this invulnerability for a few seconds. changing position could lead to bugs
            player.warp(player.rect.x - 10, player.rect.y - 10)
        else:
            # Defeated mob, so remove mob from map
            pygame.sprite.spritecollide(player, mob_sprites, True)
        # Recover HP at the end of combat
        player.set_stats({"HP": player.get_stats()["HP Max"]})

    # Player and Sword collision
    player_sword_collide = pygame.sprite.spritecollide(player, sword_sprite, False)
    if player_sword_collide:
        sword_ref = player_sword_collide[0]
        if sword_ref.verify() is None:
            # Player picks up the sword
            sword_ref.pickup(player)

    SCREEN.fill("#000000")
    game_sprites.draw(SCREEN)
    # update the display window...
    pygame.display.update()