import pygame, sys, os, game_window as WIN
from button import Button
import pygame.event as EVENTS
import entity_classes as ENTITY

pygame.init()
SCREEN = pygame.display.set_mode(WIN.window_size())
pygame.display.set_caption("Battle")


class Battle:
    def __init__(self, player=ENTITY.Player(), mobs=[ENTITY.Mob()]):
        self.player = player
        self.mobs = mobs

    def combat_screen(self):
        in_combat = True
        mobs_living = True
        player_living = True
        while in_combat:
            PLAY_MOUSE_POSITION = pygame.mouse.get_pos()
            SCREEN.fill("black")

            # Button pressed to "FIGHT"
            BATTLE_FIGHT = Button(image=None, pos=(320, 460),
                                  text_input="FIGHT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            fight_displayed = False
            # Button pressed to "RUN"
            BATTLE_RUN = Button(image=None, pos=(960, 460),
                                text_input="RUN", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            run_displayed = False
            # Button pressed to exit combat menu after finishing the fight
            BATTLE_NEXT = Button(image=None, pos=(960, 460),
                                 text_input="NEXT", font=WIN.get_font(75), base_color="#FFFFFF", hovering_color="#A90505")
            next_displayed = False

            if mobs_living:
                # Mobs are displayed as living
                # TODO Put visuals for mobs here
                PLAY_TEXT = WIN.get_font(45).render("This is where the magic will happen.", True, "White")
                PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
                mob_hp_color = "Green"
                # The battle is ongoing. Show FIGHT and RUN buttons
                BATTLE_FIGHT.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_FIGHT.update(SCREEN)
                fight_displayed = True
                BATTLE_RUN.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_RUN.update(SCREEN)
                run_displayed = True
            else:
                # Mobs are displayed as dead, the battle has ended.
                PLAY_TEXT = WIN.get_font(45).render("The wraith is dead. :)", True, "Red")
                PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
                mob_hp_color = "Red"
                # Display exit button that appears as "NEXT"
                BATTLE_NEXT.changeColor(PLAY_MOUSE_POSITION)
                BATTLE_NEXT.update(SCREEN)
                next_displayed = True
            SCREEN.blit(PLAY_TEXT, PLAY_RECT)

            self.display_hp(mob_hp_color)

            # Determine what happens for each event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WIN.game_exit()
                if event.type == pygame.KEYDOWN:
                    # Escape Key
                    if event.key == pygame.K_ESCAPE:
                        WIN.game_exit()
                    if next_displayed and event.key == pygame.K_SPACE:
                        # "NEXT" Button Shortcut
                        in_combat = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if fight_displayed and BATTLE_FIGHT.checkForInput(PLAY_MOUSE_POSITION):
                        # "FIGHT" Button
                        damage_inflicted = self.mobs[0].get_stats()["DEF"] - self.player.get_stats()["ATK"]
                        if damage_inflicted > 0:
                            damage_inflicted = 0
                        # Calculate Mob HP after damage
                        self.mobs[0].hp_update(damage_inflicted)
                        if self.mobs[0].get_stats()["HP"] <= 0:
                            # Mob is dead
                            mobs_living = False
                        else:
                            # Enemy attacks
                            self.player.hp_update(self.enemy_turn())
                            if self.player.get_stats()["HP"] <= 0:
                                # Player is dead
                                in_combat = False
                                player_living = False
                    if run_displayed and BATTLE_RUN.checkForInput(PLAY_MOUSE_POSITION):
                        # "RUN" Button: flee from fight without killing the mobs
                        in_combat = self.run_state()
                    if next_displayed and BATTLE_NEXT.checkForInput(PLAY_MOUSE_POSITION):
                        # "NEXT" Button: click to leave combat after killing the mobs
                        in_combat = False
            pygame.display.update()
        return mobs_living

    def fight_state(self):
        # Clicked FIGHT Button
        # TODO finish
        self.player_turn()
        self.enemy_turn()
        return 0

    def run_state(self):
        # Clicked RUN Button
        # TODO calculate RUN % chance
        success = True
        return not success

    def player_turn(self):
        # TODO Put player attack in here probably? instead of in display code
        return 0

    def enemy_turn(self):
        damage_inflicted = self.player.get_stats()["DEF"] - self.mobs[0].get_stats()["ATK"]
        if damage_inflicted > 0:
            damage_inflicted = 0
        # self.player.hp_update(damage_inflicted)
        return damage_inflicted

    def display_hp(self, mob_hp_color):
        # Mob HP display
        mob_hp_text = WIN.get_font(30).render(str(self.mobs[0].get_stats()["HP"]) + "/" +
                                              str(self.mobs[0].get_stats()["HP Max"]), True, mob_hp_color)
        mob_hp_rect = mob_hp_text.get_rect(center=(640, 360))
        SCREEN.blit(mob_hp_text, mob_hp_rect)

        # Player HP display
        player_hp_text = WIN.get_font(30).render(str(self.player.get_stats()["HP"]) + "/" +
                                                 str(self.player.get_stats()["HP Max"]), True, "Green")
        player_hp_rect = mob_hp_text.get_rect(center=(30, 30))
        SCREEN.blit(player_hp_text, player_hp_rect)


