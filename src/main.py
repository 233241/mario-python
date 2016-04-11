import pygame
import time
from Database import Database
from Set_graphics import Set_graphics
from Set_sounds import Set_sounds
from Sounds import Sounds
from Grid import Grid

pygame.mixer.init(44100, 16, 2, 4096)
pygame.init()

# ustawienia ekranu
caption = "Mario"
resolution = (1680, 1050)
flags = pygame.FULLSCREEN
colors = 32

frames_per_second = 60

# muzyka
ilosc_stopni_glosnosci = 35
default_music_volume = 0
default_sound_effects_volume = 1

music_folder_path = 'Music/'
sound_effect_folder_path = 'Sound effects/'

set_sounds = Set_sounds(music_folder_path, sound_effect_folder_path)

# wiazanie plikow muzycznych
game_music_file = set_sounds.set_music_path('Game music.mp3')
menu_music_file = set_sounds.set_music_path('Menu music.mp3')

# wiazanie plikow dzwiekowych
jump_sound_effect = set_sounds.set_sound('Jump.ogg')
get_coin_sound_effect = set_sounds.set_sound('Get coin.ogg')
player_shot_sound_effect = set_sounds.set_sound('Player shot.ogg')
player_trafil_strzalem_sound_effect = set_sounds.set_sound('Player trafil strzalem.ogg')
level_completed_sound_effect = set_sounds.set_sound('Level completed.ogg')
player_traci_serduszko_sound_effect = set_sounds.set_sound('Player traci serduszko.ogg')
player_traci_zycie_sound_effect = set_sounds.set_sound('Player traci zycie.ogg')
game_over_sound_effect = set_sounds.set_sound('Game over.ogg')
example_sound_effect = set_sounds.set_sound('Example.ogg')
button_click_sound_effect = set_sounds.set_sound('Button click.ogg')

# ustawienia muzyki i dzwikow
sounds = Sounds(default_sound_effects_volume, ilosc_stopni_glosnosci)
for s in [jump_sound_effect, get_coin_sound_effect, player_shot_sound_effect, player_trafil_strzalem_sound_effect, level_completed_sound_effect, player_traci_serduszko_sound_effect, player_traci_zycie_sound_effect, game_over_sound_effect, example_sound_effect, button_click_sound_effect]:
    sounds.add_sound(s)

music = Sounds(default_music_volume, ilosc_stopni_glosnosci)
music.add_sound(pygame.mixer.music)

def set_display_parameters(caption, resolution, flags, colors):
    pygame.display.set_caption(caption)
    return pygame.display.set_mode(resolution, flags, colors)

display = set_display_parameters(caption, resolution, flags, colors)

# kolory
white = (255, 255, 255)
black = (0, 0, 0)

board_size = (15000, 1050)

options_file_path = 'Settings.db'
options_sound_effects_key = 'sound_effects_key'
options_music_key = 'music_key'
high_scores_file_path = 'High_scores.db'
high_scores_key = 'key'
levels_folder = 'Levels/'
level_key = 'key'

# przyciski myszy
LEWY_PRZYCISK_MYSZY = 0
SRODKOWY_PRZYCISK_MYSZY = 1
PRAWY_PRZYCISK_MYSZY = 2

# czcionki
button_font = pygame.font.SysFont("arial", 27)
typed_font = pygame.font.SysFont("arial", 20)
game_info_font = pygame.font.SysFont('arial', 50)

class Drawer(object):
    def __init__(self):
        self.graphics_number = 0
    def set_graphics_number(self, graphics_number):
        self.graphics_number = graphics_number
    @classmethod
    def set_graphics(cls, graphics):
        cls.graphics = graphics
    def get_graphics_size(self):
        return type(self).graphics[self.graphics_number].get_size()
    def draw(self, display, x, y, dx, dy):
        graphics = type(self).graphics[self.graphics_number]
        display.blit(graphics, (x + dx, y + dy))

class Drawable_game_object(Game_object, Drawer):
    def __init__(self, x, y):
        Drawer.__init__(self)
        (w, h) = self.get_graphics_size()
        Game_object.__init__(self, x, y, w, h)
    def draw(self, display, dx, dy):
        Drawer.draw(self, display, self.x, self.y, dx, dy)

class Button(Drawable_game_object):
    def __init__(self, x, y, text, mozna_podswietlic):
        Drawable_game_object.__init__(self, x, y)
        self.left_click_wyzwalacze = []
        self.right_click_wyzwalacze = []
        self.textSurface = button_font.render(text, True, white)
        self.mozna_podswietlic = mozna_podswietlic
    def zapal(self):
        self.set_graphics_number(1)
    def zgas(self):
        self.set_graphics_number(0)
    def namierz(self):
        if self.mozna_podswietlic:
            self.zapal()
    def click(self, lista_wyzwalaczy):
        button_click_sound_effect.play()
        for w in lista_wyzwalaczy:
            w(0)
    def left_click(self):
        self.click(self.left_click_wyzwalacze)
    def right_click(self):
        self.click(self.right_click_wyzwalacze)
    def clear_wyzwalacze(self):
        self.left_click_wyzwalacze = []
        self.right_click_wyzwalacze = []
    def add_left_click_wyzwalacz(self, wyzwalacz):
        self.left_click_wyzwalacze.append(wyzwalacz)
    def add_right_click_wyzwalacz(self, wyzwalacz):
        self.right_click_wyzwalacze.append(wyzwalacz)
    def draw(self, display, dx, dy):
        Drawable_game_object.draw(self, display, dx, dy)
        textRectangle = self.textSurface.get_rect()
        textRectangle.center = (self.x + self.w / 2, self.y + self.h / 2)
        display.blit(self.textSurface, textRectangle)

class Podswietlany_button(Button):
    def __init__(self, x, y, text):
        Button.__init__(self, x, y, text, True)

class Nie_podswietlany_button(Button):
    def __init__(self, x, y, text):
        Button.__init__(self, x, y, text, False)
        
class Volume_button(Podswietlany_button):
    pass

class Short_button(Nie_podswietlany_button):
    def __init__(self, x, y):
        Nie_podswietlany_button.__init__(self, x, y, '')

def obsluz_buttons(buttons):
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if inside(pos, button.wymiary()):
            button.namierz()
            if pygame.mouse.get_pressed()[LEWY_PRZYCISK_MYSZY]:
                button.left_click()
            if pygame.mouse.get_pressed()[PRAWY_PRZYCISK_MYSZY]:
                button.right_click()

class Coin(Drawable_game_object):
    def __init__(self, x, y):
        Drawable_game_object.__init__(self, x, y)
        self.value = 10

class Wall(Drawable_game_object):
    pass

class Invisible_wall(Game_object):
    def __init__(self, x, y, w, h):
        Game_object.__init__(self, x, y, w, h)
    def draw(self, display, dx, dy):
        pass

class End_game_door(Drawable_game_object):
    pass

class Chodzacy_w_poziomie(object):
    def __init__(self, w_unit):
        self.running = False
        self.v_w = 0
        self.w_unit = w_unit
        self.direction = LEFT_DIRECTION
    def go_left(self):
        self.v_w = -self.w_unit
        self.direction = LEFT_DIRECTION
    def go_right(self):
        self.v_w = self.w_unit
        self.direction = RIGHT_DIRECTION
    def is_left(self):
        return self.v_w < 0
    def get_left_vector(self):
        return Game_object(self.x + self.v_w * (1 + self.running), self.y, self.v_w * (1 + self.running) + self.w, self.h)
    def is_right(self):
        return self.v_w > 0
    def get_right_vector(self):
        return Game_object(self.x, self.y, self.v_w * (1 + self.running) + self.w, self.h)
    def update_poziome_velocities(self):
        self.running = False
        self.v_w = 0

class Chodzacy_w_pionie(object):
    def __init__(self, h_unit):
        self.v_h = 0
        self.h_unit = h_unit
    def go_up(self):
        self.v_h = -self.h_unit
    def go_down(self):
        self.v_h = self.h_unit
    def is_down(self):
        return self.v_h > 0
    def get_down_vector(self):
        return Game_object(self.x, self.y, self.w, self.v_h + self.h)
    def is_up(self):
        return self.v_h < 0
    def get_up_vector(self):
        return Game_object(self.x, self.y + self.v_h, self.w, - self.v_h + self.h)

class Samochodzacy_w_poziomie(Chodzacy_w_poziomie):
    def __init__(self, w_unit):
        Chodzacy_w_poziomie.__init__(self, w_unit)
    def go(self):
        if self.direction == LEFT_DIRECTION:
            self.go_left()
        elif self.direction == RIGHT_DIRECTION:
            self.go_right()

class Samochodzacy_w_pionie(Chodzacy_w_pionie):
    def __init__(self, h_unit):
        Chodzacy_w_pionie.__init__(self, h_unit)
    def go(self):
        if self.direction == UP_DIRECTION:
            self.go_up()
        elif self.direction == DOWN_DIRECTION:
            self.go_down()

class Przyciagany(object):
    def __init__(self, a_h):
        self.a_h = a_h
        self.on_ground = False
    def update_przyciaganie(self):
        if self.on_ground:
            self.v_h = 0
        else:
            self.v_h += self.a_h

class Strzelajacy():
    def shot(self, direction):
        shot = Shot(self, 30, 10, 0, 0, direction)
        shot.set_graphics_number(direction)
        (shot_w, shot_h) = shot.get_graphics_size()
        if direction == UP_DIRECTION:
            x = self.x + self.w / 2 - shot_w / 2
            y = self.y - 10 - shot_h
        elif direction == DOWN_DIRECTION:
            x = self.x + self.w / 2 - shot_w / 2
            y = self.y + self.h + 10
        elif direction == LEFT_DIRECTION:
            x = self.x - 10 - shot_w
            y = self.y + self.h / 2 - shot_h / 2
        elif direction == RIGHT_DIRECTION:
            x = self.x + self.w + 10
            y = self.y + self.h / 2 - shot_h / 2
        shot.go_to(x, y)
        return shot

LEFT_DIRECTION = 0
RIGHT_DIRECTION = 1
UP_DIRECTION = 2
DOWN_DIRECTION = 3


class Shot(Drawable_game_object, Samochodzacy_w_poziomie, Samochodzacy_w_pionie):
    def __init__(self, owner, v, duration, x, y, direction):
        Drawable_game_object.__init__(self, x, y)
        Samochodzacy_w_poziomie.__init__(self, v)
        Samochodzacy_w_pionie.__init__(self, v)
        self.owner = owner
        self.duration = duration
        self.direction = direction
    def time_flows(self):
        if self.duration > 0:
            self.duration -= 1
    def collide(self, direction):
        self.duration = 0
    def go(self):
        Samochodzacy_w_pionie.go(self)
        Samochodzacy_w_poziomie.go(self)
    def go_to(self, new_x, new_y):
        self.x, self.y = new_x, new_y
    def draw(self, display, dx, dy):
        self.set_graphics_number(self.direction)
        Drawable_game_object.draw(self, display, dx, dy)

class Static_monster(Drawable_game_object, Chodzacy_w_pionie, Przyciagany, Strzelajacy):
    def __init__(self, x, y):
        Drawable_game_object.__init__(self, x, y)
        Chodzacy_w_pionie.__init__(self, 30)
        Przyciagany.__init__(self, 2)
        self.ready_to_shot = True
    def go_to(self, new_x, new_y):
        self.x, self.y = new_x, new_y
    def collide(self, direction):
        pass

class Dynamic_monster(Drawable_game_object, Samochodzacy_w_poziomie, Chodzacy_w_pionie, Przyciagany):
    def __init__(self, x, y):
        Drawable_game_object.__init__(self, x, y)
        Samochodzacy_w_poziomie.__init__(self, 2)
        Chodzacy_w_pionie.__init__(self, 30)
        Przyciagany.__init__(self, 2)
    def get_podstawe(self):
        return Game_object(self.x, self.y + self.h + 1, self.w, 0)
    def collide(self, direction):
        if direction == UP_DIRECTION:
            self.v_h = 0
        elif direction == DOWN_DIRECTION:
            self.on_ground = True
        elif direction == LEFT_DIRECTION:
            self.direction = RIGHT_DIRECTION
        elif direction == RIGHT_DIRECTION:
            self.direction = LEFT_DIRECTION
        return Game_object(self.x, self.y + self.h + 1, self.w, 0)
    def go_to(self, new_x, new_y):
        self.x, self.y = new_x, new_y
    def zawroc(self):
        if self.direction == LEFT_DIRECTION:
            self.direction = RIGHT_DIRECTION
        elif self.direction == RIGHT_DIRECTION:
            self.direction = LEFT_DIRECTION
    def draw(self, display, dx, dy):
        self.set_graphics_number(self.direction)
        Drawable_game_object.draw(self, display, dx, dy)

sila_skoku = -30

class Punkt_startowy(Drawable_game_object):
    pass

max_liczba_serduszek = 3

class Player(Drawable_game_object, Chodzacy_w_poziomie, Chodzacy_w_pionie, Przyciagany, Strzelajacy):
    def __init__(self, x, y):
        Drawable_game_object.__init__(self, x, y)
        Chodzacy_w_poziomie.__init__(self, 6)
        Chodzacy_w_pionie.__init__(self, 30)
        Przyciagany.__init__(self, 2)
        self.zycia = 3
        self.regenerate_serduszka()
        self.pozostaly_czas_niesmiertelnosci = 0
    def regenerate_serduszka(self):
        self.serduszka = max_liczba_serduszek
    def zmniejsz_czas_niesmiertelnosci(self, value):
        if self.pozostaly_czas_niesmiertelnosci > 0:
            self.pozostaly_czas_niesmiertelnosci = max(0, self.pozostaly_czas_niesmiertelnosci - value)
    def strac_serduszko(self):
        if self.serduszka == 1:
            self.strac_zycie()
            return True
        else:
            player_traci_serduszko_sound_effect.play()
            self.serduszka -= 1
            self.pozostaly_czas_niesmiertelnosci = 2000
            return False
    def strac_zycie(self):
        player_traci_zycie_sound_effect.play()
        self.zycia -= 1
        self.regenerate_serduszka()
    def jump(self):
        if self.on_ground:
            jump_sound_effect.play()
            self.on_ground = False
            self.v_h = sila_skoku
    def collide(self, direction):
        if direction == UP_DIRECTION:
            self.v_h = 0
        elif direction == DOWN_DIRECTION:
            self.on_ground = True
        elif direction == LEFT_DIRECTION:
            pass
        elif direction == RIGHT_DIRECTION:
            pass
    def go_to(self, new_x, new_y):
        self.x, self.y = new_x, new_y
    def get_podstawe(self):
        return Game_object(self.x, self.y + self.h + 1, self.w, 0)
    def get_visible_screen(self, board_width):
        y_val = 0
        if self.x - resolution[0] / 2.0 < 0:
            x_val = 0
        elif self.x + resolution[0] / 2.0 > board_width:
            x_val = board_width - resolution[0]
        else:
            x_val = self.x - resolution[0] / 2.0
        return Game_object(x_val, y_val, resolution[0], resolution[1])
    def draw(self, display, dx, dy):
        number = self.direction + 2 * (self.pozostaly_czas_niesmiertelnosci > 0)
        self.set_graphics_number(number)
        Drawable_game_object.draw(self, display, dx, dy)

class Background(Drawable_game_object):
    def __init__(self):
        Drawable_game_object.__init__(self, 0, 0)
class Menu_background(Background):
    pass
class Game_background(Background):
    pass
class Editor_background(Background):
    pass
class High_scores_background(Background):
    pass
class Wpisywanie_background(Background):
    pass
class Options_background(Background):
    pass
class Side_panel_background(Background):
    pass

graphics_folder_path = 'Graphics/'
graphics_ustalator = Set_graphics(graphics_folder_path)

drawable_objects = [Wall, Coin, End_game_door, Player, Static_monster, Dynamic_monster, Button, Volume_button, Short_button, Menu_background, Game_background, Editor_background, High_scores_background, Wpisywanie_background, Options_background, Side_panel_background, Punkt_startowy, Shot]
names = [['Wall.png'],['Coin.png'],['End_game_door.png'],['Player left.png', 'Player right.png', 'Player left immortal.png', 'Player right immortal.png'],['Static monster.png'],['Dynamic monster left.png', 'Dynamic monster right.png'],['Button.png', 'Button podswietlony.png'],['Volume button.png', 'Volume button podswietlony.png'],['Short button.png', 'Short button podswietlony.png'], ['Menu background.png'], ['Game background.png'], ['Editor background.png'], ['High scores background.png'], ['Wpisywanie wynikow background.png'], ['Options background.png'], ['Side panel_background.png'], ['Punkt startowy.png'], ['Left shot.png', 'Right shot.png', 'Up shot.png', 'Down shot.png']]

for i in range(len(drawable_objects)):
    graphics_ustalator.set_graphics(drawable_objects[i], names[i])

# BUTTONS
BUTTON_MENU_NEW_GAME = Podswietlany_button(120, 900, 'NEW GAME')
BUTTON_MENU_EDITOR = Podswietlany_button(410, 900, 'EDITOR')
BUTTON_MENU_OPTIONS = Podswietlany_button(720, 900, 'OPTIONS')
BUTTON_MENU_HIGH_SCORES = Podswietlany_button(1030, 900, 'HIGH SCORES')
BUTTON_MENU_QUIT = Podswietlany_button(1340, 900, 'QUIT')

BUTTON_EDITOR_NEW = Podswietlany_button(50, 50, 'NEW')
BUTTON_EDITOR_SAVE = Podswietlany_button(50, 140, 'SAVE')
BUTTON_EDITOR_LOAD = Podswietlany_button(50, 230, 'LOAD')
BUTTON_EDITOR_EXIT = Podswietlany_button(50, 320, 'EXIT')

BUTTON_EDITOR_WALL = Nie_podswietlany_button(50, 520, 'WALL')
BUTTON_EDITOR_COIN = Nie_podswietlany_button(50, 610, 'COIN')
BUTTON_EDITOR_PLAYER = Nie_podswietlany_button(50, 700, 'PLAYER')
BUTTON_EDITOR_END_GAME_DOOR = Nie_podswietlany_button(50, 790, 'END GAME_DOOR')
BUTTON_EDITOR_STATIC_MONSTER = Nie_podswietlany_button(50, 880, 'STATIC_MONSTER')
BUTTON_EDITOR_DYNAMIC_MONSTER = Nie_podswietlany_button(50, 970, 'DYNAMIC_MONSTER')

szer_sb = 30
szer_vb = 70
szer_przerwy_m = 10
szer_przerwy_m_d = 30
d_x = (resolution[0] - ilosc_stopni_glosnosci * szer_sb - (ilosc_stopni_glosnosci - 1) * szer_przerwy_m - 2 * szer_przerwy_m_d - 2 * szer_vb) / 2
BUTTON_OPTIONS_DOWN_SOUNDS_VOLUME = Volume_button(d_x, 200, '-')
BUTTON_OPTIONS_UP_SOUNDS_VOLUME = Volume_button(resolution[0] - d_x - szer_vb, 200, '+')
BUTTON_OPTIONS_DOWN_MUSIC_VOLUME = Volume_button(d_x, 500, '-')
BUTTON_OPTIONS_UP_MUSIC_VOLUME = Volume_button(resolution[0] - d_x - szer_vb, 500, '+')
BUTTONS_OPTIONS_SOUND_VOLUMES = []
BUTTONS_OPTIONS_MUSIC_VOLUMES = []
for i in range(ilosc_stopni_glosnosci):
    BUTTONS_OPTIONS_SOUND_VOLUMES.append(Short_button(d_x + szer_vb + szer_przerwy_m_d + i*(szer_sb + szer_przerwy_m), 200))
    BUTTONS_OPTIONS_MUSIC_VOLUMES.append(Short_button(d_x + szer_vb + szer_przerwy_m_d + i*(szer_sb + szer_przerwy_m), 500))
BUTTON_OPTIONS_BACK = Podswietlany_button(740, 800, 'BACK')

BUTTON_HIGH_SCORES_BACK = Podswietlany_button(740, 800, 'BACK')

BUTTON_WPISYWANIE_WYNIKOW_ZAPISZ = Podswietlany_button(780, 950, 'ZAPISZ')

menu_buttons = [BUTTON_MENU_NEW_GAME, BUTTON_MENU_EDITOR, BUTTON_MENU_OPTIONS, BUTTON_MENU_HIGH_SCORES, BUTTON_MENU_QUIT]

tick_buttons = [BUTTON_EDITOR_WALL, BUTTON_EDITOR_COIN, BUTTON_EDITOR_PLAYER, BUTTON_EDITOR_END_GAME_DOOR, BUTTON_EDITOR_STATIC_MONSTER, BUTTON_EDITOR_DYNAMIC_MONSTER]
tick_buttons_objects = [Wall, Coin, Punkt_startowy, End_game_door, Static_monster, Dynamic_monster]
editor_buttons = [BUTTON_EDITOR_NEW, BUTTON_EDITOR_SAVE, BUTTON_EDITOR_LOAD, BUTTON_EDITOR_EXIT] + tick_buttons
jednorazowe = [BUTTON_EDITOR_PLAYER, BUTTON_EDITOR_END_GAME_DOOR]

option_buttons = [BUTTON_OPTIONS_BACK, BUTTON_OPTIONS_DOWN_SOUNDS_VOLUME, BUTTON_OPTIONS_UP_SOUNDS_VOLUME, BUTTON_OPTIONS_DOWN_MUSIC_VOLUME, BUTTON_OPTIONS_UP_MUSIC_VOLUME] + BUTTONS_OPTIONS_SOUND_VOLUMES + BUTTONS_OPTIONS_MUSIC_VOLUMES

high_scores_buttons = [BUTTON_HIGH_SCORES_BACK]

wpisywanie_wynikow_buttons = [BUTTON_WPISYWANIE_WYNIKOW_ZAPISZ]

max_name_length = 20

life_graphics = pygame.image.load(graphics_folder_path + 'Life.png').convert_alpha()
heart_graphics = pygame.image.load(graphics_folder_path + 'Heart.png').convert_alpha()
scores_graphics = pygame.image.load(graphics_folder_path + 'Scores.png').convert_alpha()
clock_1_graphics = pygame.image.load(graphics_folder_path + 'Clock 1.png').convert_alpha()
clock_2_graphics = pygame.image.load(graphics_folder_path + 'Clock 2.png').convert_alpha()

class View(object):
    def __init__(self, display):
        self.display = display
    def draw_text(self, text, pos, size, color):
        font = pygame.font.SysFont('Arial', size)
        rendered_text = font.render(str(text), True, color)
        self.display.blit(rendered_text, pos)
    def draw_table(self, high_scores):
        self.draw_text('HIGH SCORES', (600, 30), 60, black)
        self.draw_text('POSITION', (50, 200), 30, black)
        self.draw_text('SCORES', (400, 200), 30, black)
        self.draw_text('NAME', (1000, 200), 30, black)
        for i in range(len(high_scores)):
            (scores, name) = high_scores[i]
            self.draw_text(str(i), (50, 200 + (i + 1) * 50), 20, black)
            self.draw_text(str(scores), (400, 200 + (i + 1) * 50), 20, black)
            self.draw_text(name, (1000, 200 + (i + 1) * 50), 20, black)
    def draw_component(self, component, dx, dy, clean):
        component.draw(self.display, dx, dy)
        if clean:
            component.set_graphics_number(0)
    def draw_components(self, components, dx, dy, clean):
        for component in components:
            self.draw_component(component, dx, dy, clean)
    def draw_board(self, board, player, dx, dy, state):
        self.draw_components(board.walls, dx, dy, False)
        if board.end_game_door:
            self.draw_component(board.end_game_door, dx, dy, False)
        self.draw_components(board.coins, dx, dy, False)
        if board.punkt_startowy:
            if state == EDITOR_STATE:
                self.draw_component(board.punkt_startowy, dx, dy, False)
            elif state == GAME_STATE:
                self.draw_component(player, dx, dy, False)
        self.draw_components(board.static_monsters, dx, dy, False)
        self.draw_components(board.dynamic_monsters, dx, dy, False)
        self.draw_components(board.player_shots, dx, dy, False)
        self.draw_components(board.monster_shots, dx, dy, False)
    def draw_wpisywanie_wynikow(self, scores, name):
        rendered_text_1 = button_font.render(scores, True, black)
        rendered_text_2 = button_font.render(name, True, black)
        pygame.draw.rect(display, black, [200, 200, 300, 30], 1)
        display.blit(rendered_text_1, (100, 100))
        display.blit(rendered_text_2, (200, 200))
    def draw_game_info(self, life, hearts, scores, remaining_level_time, remaining_bonus_time):
        max_width = max(life_graphics.get_width(), heart_graphics.get_width(), scores_graphics.get_width(), clock_1_graphics.get_width(), clock_2_graphics.get_width())
        dy = 10
        for (graphics, data) in [(life_graphics, life), (heart_graphics, hearts), (scores_graphics, scores), (clock_1_graphics, remaining_level_time)]:
            self.display.blit(graphics, (10 + max_width / 2 - graphics.get_width() / 2, dy))
            self.display.blit(game_info_font.render(str(data), True, black) ,(30 + max_width, dy))
            dy += 10 + graphics.get_height()
        if remaining_bonus_time:
            self.display.blit(clock_2_graphics, (10 + max_width / 2 - clock_2_graphics.get_width() / 2, dy))
            self.display.blit(game_info_font.render(str(remaining_bonus_time), True, black) ,(30 + max_width, dy))

def quit_application():
    pygame.quit()
    quit()

class Board(Game_object):
    def __init__(self, w, h):
        Game_object.__init__(self, 0, 0, w, h)
        self.punkt_startowy = None
        self.end_game_door = None
        self.invisible_walls = []
        self.walls = []
        self.walls_grid = Grid(50, 50, w, h + 200)
        self.coins = []
        self.static_monsters = []
        self.static_monsters_grid = Grid(50, 50, w, h + 200)
        self.dynamic_monsters = []
        self.dynamic_monsters_grid = Grid(50, 50, w, h + 200)
        self.player_shots = []
        self.monster_shots = []
        self.add_otaczajace_mury()
    def add_otaczajace_mury(self):
        self.invisible_walls.append(Invisible_wall(-100, 0, 100, self.h))
        self.invisible_walls.append(Invisible_wall(self.w, 0, 100, self.h))
        self.invisible_walls.append(Invisible_wall(0, -100, self.w, 100))    
    def can_add_object(self, obj):
        objects_on_board = self.invisible_walls + self.coins
        if self.punkt_startowy:
            objects_on_board.append(self.punkt_startowy)
        if self.end_game_door:
            objects_on_board.append(self.end_game_door)
        return not collision_with_many(obj, objects_on_board) and not self.walls_grid.check(obj) and not self.static_monsters_grid.check(obj) and not self.dynamic_monsters_grid.check(obj) and not obj.y + obj.h > self.h
    def add_wall(self, wall):
        self.walls_grid.add(wall)
        self.walls.append(wall)
    def add_coin(self, coin):
        self.coins.append(coin)
    def add_punkt_startowy(self, punkt_startowy):
        self.punkt_startowy = punkt_startowy
    def add_end_game_door(self, door):
        self.end_game_door = door
    def add_static_monster(self, monster):
        self.static_monsters_grid.add(monster)
        self.static_monsters.append(monster)
    def add_dynamic_monster(self, monster):
        self.dynamic_monsters_grid.add(monster)
        self.dynamic_monsters.append(monster)
    def add_player_shot(self, shot):
        self.player_shots.append(shot)
    def add_monster_shot(self, shot):
        self.monster_shots.append(shot)

# EDITOR

menu_width = 300
editor_board_width = resolution[0] - menu_width
editor_board_height = resolution[1]
editor_visible_board = Game_object(menu_width, 0, editor_board_width, editor_board_height)
alignment = 10

def e_to_b(x, p_x):
    return x - 300 + p_x

def b_to_e(x, p_x):
    return x + 300 - p_x

class State(object):
    def __init__(self, view, controller, buttons, background):
        self.view = view
        self.controller = controller
        self.buttons = buttons
        self.background = background
        self.czysc_wyzwalacze()
        self.set_wyzwalacze()
    def set_wyzwalacze(self):
        pass
    def czysc_wyzwalacze(self):
        for button in self.buttons:
            button.clear_wyzwalacze()
    def update(self):
        self.view.draw_component(self.background, 0, 0, False)
        self.view.draw_components(self.buttons, 0, 0, True)
    def handle(self, event):
        pass


max_name_board_length = 15

class Editor_state(State):
    def __init__(self, view, controller, buttons, background):
        State.__init__(self, view, controller, buttons, background)
        self.board_name = ""
        self.wykorzystane = []
        self.choosen_button = None
        self.dx, self.dy = (0, 0)
        self.side_panel_background = Side_panel_background()
        self.new_controller()
    def set_wyzwalacze(self):
        BUTTON_EDITOR_NEW.add_left_click_wyzwalacz(lambda _: self.new_controller())
        BUTTON_EDITOR_SAVE.add_left_click_wyzwalacz(lambda _: self.save_controller())
        BUTTON_EDITOR_LOAD.add_left_click_wyzwalacz(lambda _: self.load_controller())
        BUTTON_EDITOR_EXIT.add_left_click_wyzwalacz(lambda _: self.exit_controller())
    def update(self):
        self.view.draw_component(self.background, 0, 0, False)
        self.view.draw_board(self.actual_board, None, menu_width - self.dx, self.dy, EDITOR_STATE)
        self.view.draw_component(self.side_panel_background, 0, 0, False)
        self.view.draw_components(editor_buttons, 0, 0, True)
##
        pygame.draw.rect(display, black, [10, 440, 280, 30], 1)
        rendered_text = button_font.render(self.board_name, True, black)
        display.blit(rendered_text, (15, 440))

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.dx = max(0, self.dx - alignment)
        elif pressed_keys[pygame.K_RIGHT]:
            self.dx = min(self.dx + alignment, board_size[0] - editor_board_width)
        obsluz_buttons(editor_buttons)

# do refaktoryzacji
        pos = pygame.mouse.get_pos()
        for button in tick_buttons:
            if inside(pos, button.wymiary()):
                if pygame.mouse.get_pressed()[LEWY_PRZYCISK_MYSZY]:
                    return self.select_button(button)
                elif pygame.mouse.get_pressed()[PRAWY_PRZYCISK_MYSZY]:
                    return self.unselect_button(button)

        pos = pygame.mouse.get_pos()
        if inside(pos, editor_visible_board.wymiary()):
            for i in range(len(tick_buttons)):
                button = tick_buttons[i]
                if self.choosen_button == button:
                    obj = tick_buttons_objects[i](e_to_b(alignment * (pos[0] / alignment), self.dx), alignment * (pos[1] / alignment))
                    if self.actual_board.can_add_object(obj):
                        self.view.draw_component(obj, menu_width - self.dx, self.dy, False)
                        if pygame.mouse.get_pressed()[LEWY_PRZYCISK_MYSZY]:
                            self.add_object(obj)
                            if button in jednorazowe:
                                self.wykorzystane.append(button)
                                self.choosen_button = None
        if self.choosen_button:
            self.choosen_button.zapal()
    def select_button(self, button):
        if not button in self.wykorzystane:
            self.choosen_button = button
    def unselect_button(self, button):
        if self.choosen_button == button:
            self.choosen_button = None
    def actualize_wykorzystane(self):
        self.wykorzystane = []
        if self.actual_board.punkt_startowy:
            self.wykorzystane.append(BUTTON_EDITOR_PLAYER)
        if self.actual_board.end_game_door:
            self.wykorzystane.append(BUTTON_EDITOR_END_GAME_DOOR)
    def new_controller(self):
        self.actual_board = Board(board_size[0], board_size[1])
        self.actualize_wykorzystane()
    def save_controller(self):
        path = levels_folder + self.board_name + '.db'
        Database.save(path, level_key, self.actual_board)
    def load_controller(self):
        path = levels_folder + self.board_name + '.db'
        loaded = Database.load(path, level_key)
        if loaded:
            self.actual_board = loaded
            self.actualize_wykorzystane()
    def exit_controller(self):
        self.controller.change_state(MENU_STATE)
    def add_object(self, obj):
        if type(obj) == Wall:
            self.actual_board.add_wall(obj)
        elif type(obj) == Coin:
            self.actual_board.add_coin(obj)
        elif type(obj) == Punkt_startowy:
            self.actual_board.add_punkt_startowy(obj)
        elif type(obj) == End_game_door:
            self.actual_board.add_end_game_door(obj)
        elif type(obj) == Static_monster:
            self.actual_board.add_static_monster(obj)
        elif type(obj) == Dynamic_monster:
            self.actual_board.add_dynamic_monster(obj)
    def handle(self, event):
        State.handle(self, event)
        if event.type == pygame.KEYDOWN:
            if len(self.board_name) <= max_name_board_length and (pygame.K_0 <= event.key <= pygame.K_z or event.key == pygame.K_SPACE):
                character = chr(event.key)
                self.board_name += str(character)
            elif event.key == pygame.K_BACKSPACE:
                self.board_name = self.board_name[:-1]

MENU_STATE = 0
GAME_STATE = 1
EDITOR_STATE = 2
OPTIONS_STATE = 3
HIGH_SCORES_STATE = 4
WPISZ_WYNIKI_STATE = 5
WPISZ_ZAPISZ_PLANSZE_STATE = 6
WPISZ_WCZYTAJ_PLANSZE_STATE = 7


class Controller(object):
    def __init__(self, view):
        self.view = view
        self.change_state(MENU_STATE)
        self.changed_state = True
    def update(self):
        if self.changed_state:
            self.go_state()
            self.changed_state = False
        self.state.update()
    def handle(self, event):
        if event.type == pygame.QUIT:
            quit_application()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit_application()
        else:
            self.state.handle(event)
    def change_state(self, state):
        self.state_name = state
        self.changed_state = True
    def go_state(self):
        if self.state_name == MENU_STATE:
            self.go_menu_state()
        elif self.state_name == GAME_STATE:
            self.go_game_state()
        elif self.state_name == EDITOR_STATE:
            self.go_editor_state()
        elif self.state_name == OPTIONS_STATE:
            self.go_options_state()
        elif self.state_name == HIGH_SCORES_STATE:
            self.go_high_scores()
        elif self.state_name == WPISZ_WYNIKI_STATE:
            self.go_wpisywanie_wynikow(self.scores)         
    def go_menu_state(self):
        self.state = Menu_state(self.view, self, menu_buttons, Menu_background())
    def go_game_state(self):
        self.state = Game_state(self.view, self, [], Game_background())
    def go_editor_state(self):
            self.state = Editor_state(self.view, self, editor_buttons, Editor_background())
    def go_options_state(self):
        self.state = Options_state(self.view, self, option_buttons, Options_background())
    def go_high_scores(self):
        self.state = High_scores_state(self.view, self, high_scores_buttons, High_scores_background())
    def go_wpisywanie_wynikow(self, scores):
        self.state = Wpisywanie_wynikow_state(self.view, self, wpisywanie_wynikow_buttons, Wpisywanie_background(), scores)

class Options_state(State):
    def __init__(self, view, controller, buttons, background):
        State.__init__(self, view, controller, buttons, background)
    def set_wyzwalacze(self):
        BUTTON_OPTIONS_BACK.add_left_click_wyzwalacz(lambda _: self.controller.change_state(MENU_STATE))
        BUTTON_OPTIONS_DOWN_SOUNDS_VOLUME.add_left_click_wyzwalacz(lambda _: sounds.set_down_volume())
        BUTTON_OPTIONS_DOWN_SOUNDS_VOLUME.add_left_click_wyzwalacz(lambda _: example_sound_effect.play())
        BUTTON_OPTIONS_UP_SOUNDS_VOLUME.add_left_click_wyzwalacz(lambda _: sounds.set_up_volume())
        BUTTON_OPTIONS_UP_SOUNDS_VOLUME.add_left_click_wyzwalacz(lambda _: example_sound_effect.play())
        BUTTON_OPTIONS_DOWN_MUSIC_VOLUME.add_left_click_wyzwalacz(lambda _: music.set_down_volume())
        BUTTON_OPTIONS_UP_MUSIC_VOLUME.add_left_click_wyzwalacz(lambda _: music.set_up_volume())
    def update(self):
        obsluz_buttons(self.buttons)

        for i in range(sounds.get_volume()):
            BUTTONS_OPTIONS_SOUND_VOLUMES[i].zapal()

        for i in range(music.get_volume()):
            BUTTONS_OPTIONS_MUSIC_VOLUMES[i].zapal()

        State.update(self)
        self.view.draw_text('SOUND EFFECTS', (600, 50), 60, black)
        self.view.draw_text('MUSIC', (750, 350), 60, black)

class High_scores_state(State):
    def __init__(self, view, controller, buttons, background):
        State.__init__(self, view, controller, buttons, background)
        self.scores = Database.load(high_scores_file_path, high_scores_key)
        self.scores.reverse()
    def set_wyzwalacze(self):
        BUTTON_HIGH_SCORES_BACK.add_left_click_wyzwalacz(lambda _: self.controller.go_menu_state())
    def update(self):
        obsluz_buttons(high_scores_buttons)
        State.update(self)
        self.view.draw_table(self.scores)

class Wpisywanie_wynikow_state(State):
    def __init__(self, view, controller, buttons, background, scores):
        State.__init__(self, view, controller, buttons, background)
        self.name = ""
        self.scores = str(scores)
    def set_wyzwalacze(self):
        BUTTON_WPISYWANIE_WYNIKOW_ZAPISZ.add_left_click_wyzwalacz(lambda _: self.zapisz_controller())
    def zapisz(self):
        high_scores = Database.load(high_scores_file_path, high_scores_key)
        high_scores.append((self.scores, self.name))
        # uwaga gdy int(x) rzuci wyjatek !!!
        high_scores = map(lambda (s, n): (int(s), n), high_scores)
        high_scores.sort()
        high_scores = high_scores[-10:]
        Database.save(high_scores_file_path, high_scores_key, high_scores)
    def zapisz_controller(self):
        self.zapisz()
        self.controller.change_state(HIGH_SCORES_STATE)
    def update(self):
        obsluz_buttons(wpisywanie_wynikow_buttons)
        State.update(self)
        self.view.draw_wpisywanie_wynikow(self.scores, self.name)
    def handle(self, event):
        State.handle(self, event)
        if event.type == pygame.KEYDOWN:
            if len(self.name) <= max_name_length and (pygame.K_a <= event.key <= pygame.K_z or event.key == pygame.K_SPACE):
                character = chr(event.key)
                self.name += str(character)
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]

class Menu_state(State):
    def __init__(self, view, controller, buttons, background):
        State.__init__(self, view, controller, buttons, background)
        pygame.mixer.music.load(menu_music_file)
        pygame.mixer.music.play(-1)
    def set_wyzwalacze(self):
        BUTTON_MENU_NEW_GAME.add_left_click_wyzwalacz(lambda _: self.controller.change_state(GAME_STATE))
        BUTTON_MENU_EDITOR.add_left_click_wyzwalacz(lambda _: self.controller.change_state(EDITOR_STATE))
        BUTTON_MENU_OPTIONS.add_left_click_wyzwalacz(lambda _: self.controller.change_state(OPTIONS_STATE))
        BUTTON_MENU_HIGH_SCORES.add_left_click_wyzwalacz(lambda _: self.controller.change_state(HIGH_SCORES_STATE))
        BUTTON_MENU_QUIT.add_left_click_wyzwalacz(lambda _: quit_application())
    def update(self):
        State.update(self)
        obsluz_buttons(menu_buttons)

GAME = 0
GAME_OVER = 1
LEVEL_COMPLETED = 2

AKTUALIZUJ_CZAS = pygame.USEREVENT + 0
MINELA_SEKUNDA_EVENT = pygame.USEREVENT + 1
SKONCZYL_SIE_CZAS_EVENT = pygame.USEREVENT + 2

"""
User events should be between:
pygame.USEREVENT: 24
pygame.NUMEVENTS: 32

wylaczanie : set_timer(arg = 0)

1. aktualizuj czas co 0.01 sekundy (zmniejsz czas_lv, zmniejsz czas_bonus)
2. aktualizuj co sekunde (strzelanie potworow)
3. skonczyl sie czas_lv (MOZNA WYELIMINOWAC)

"""

def rusz_sie_poziom(obj, walls_grid, invisible_walls, result_vector):
    if obj.is_left():
        move_vector = obj.get_left_vector()
        collision_area = add(area_sum(walls_grid.check(move_vector)) ,collision_with_many(move_vector, invisible_walls))
        if collision_area:
            #
            result_vector = add(obj, Game_object(min(move_vector.x + move_vector.w - obj.w, collision_area.x + collision_area.w), obj.y, obj.w, obj.h))
            obj.go_to(collision_area.x + collision_area.w, obj.y)
            obj.collide(LEFT_DIRECTION)
        else:
            result_vector = add(obj, Game_object(move_vector.x, move_vector.y, obj.w, obj.h))
            obj.go_to(move_vector.x, move_vector.y)
    if obj.is_right():
        move_vector = obj.get_right_vector()
        collision_area = add(area_sum(walls_grid.check(move_vector)) ,collision_with_many(move_vector, invisible_walls))
        if collision_area:
            result_vector = add(obj, Game_object(max(move_vector.x, collision_area.x - obj.w), obj.y, obj.w, obj.h))
            obj.go_to(collision_area.x - obj.w, obj.y)
            obj.collide(RIGHT_DIRECTION)
        else:
            result_vector = add(obj, Game_object(move_vector.x + move_vector.w - obj.w, move_vector.y, obj.w, obj.h))
            obj.go_to(move_vector.x + move_vector.w - obj.w, move_vector.y)
    return result_vector

def rusz_sie_pion(obj, walls_grid, invisible_walls, result_vector):
    if obj.is_down():
        move_vector = obj.get_down_vector()
        collision_area = add(area_sum(walls_grid.check(move_vector)) ,collision_with_many(move_vector, invisible_walls))
        if collision_area:
            result_vector = add(obj, Game_object(obj.x, max(move_vector.h, collision_area.y - obj.h), obj.w, obj.h))
            obj.go_to(obj.x, collision_area.y - obj.h)
            obj.collide(DOWN_DIRECTION)
        else:
            result_vector = add(obj, Game_object(obj.x, move_vector.y + move_vector.h - obj.h, obj.w, obj.h))
            obj.go_to(obj.x, move_vector.y + move_vector.h - obj.h) 
    if obj.is_up():
        move_vector = obj.get_up_vector()
        collision_area = add(area_sum(walls_grid.check(move_vector)) ,collision_with_many(move_vector, invisible_walls))
        if collision_area:
            result_vector = add(obj, Game_object(obj.x, min(move_vector.y + move_vector.h - obj.h, collision_area.y + collision_area.h), obj.w, obj.h))
            obj.go_to(obj.x, collision_area.y + collision_area.h)
            obj.collide(UP_DIRECTION)
        else:
            result_vector = add(obj, Game_object(move_vector.x, move_vector.y, obj.w, obj.h))
            obj.go_to(move_vector.x, move_vector.y)

    return result_vector
 
LEVEL_TIME = 70000
BONUS_TIME = 10000

import threading
dynamic_monster_list_lock = threading.Lock()
dynamic_monsters_grid_lock = threading.Lock()

class Dynamic_monster_move(threading.Thread):
    @staticmethod
    def set_objects(walls_grid, invisible_walls, dynamic_monsters_grid, dynamic_monster_list, ground_level):
        Dynamic_monster_move.walls_grid = walls_grid
        Dynamic_monster_move.invisible_walls = invisible_walls
        Dynamic_monster_move.dynamic_monsters_grid = dynamic_monsters_grid
        Dynamic_monster_move.dynamic_monster_list = dynamic_monster_list
        Dynamic_monster_move.ground_level = ground_level
        
    def __init__(self, monster):
        self.monster = monster
        threading.Thread.__init__(self)
    def run(self):
        global dynamic_monsters_grid_lock
        global dynamic_monster_list_lock
        self.monster.go()
        
        dynamic_monsters_grid_lock.acquire()
        Dynamic_monster_move.dynamic_monsters_grid.remove(self.monster)
        dynamic_monsters_grid_lock.release()

        collides_bottom = area_sum(Dynamic_monster_move.walls_grid.check(self.monster.get_podstawe()))
        if collides_bottom and ((self.monster.is_left() and collides_bottom.x > self.monster.x) or (self.monster.is_right() and collides_bottom.x + collides_bottom.w < self.monster.x + self.monster.w)):
            self.monster.zawroc()

        self.monster.update_przyciaganie()
        new_move_vector = rusz_sie_pion(self.monster, Dynamic_monster_move.walls_grid, Dynamic_monster_move.invisible_walls, self.monster)

        new_move_vector = rusz_sie_poziom(self.monster, Dynamic_monster_move.walls_grid, Dynamic_monster_move.invisible_walls, new_move_vector)
        self.monster.update_poziome_velocities()
        
        dynamic_monsters_grid_lock.acquire()
        Dynamic_monster_move.dynamic_monsters_grid.add(self.monster)
        dynamic_monsters_grid_lock.release()

        if self.monster.y > Dynamic_monster_move.ground_level:
            dynamic_monsters_grid_lock.acquire()
            Dynamic_monster_move.dynamic_monsters_grid.remove(self.monster)
            dynamic_monsters_grid_lock.release()
            dynamic_monster_list_lock.acquire()
            Dynamic_monster_move.dynamic_monster_list.remove(self.monster)
            dynamic_monster_list_lock.release()

levels = ['level1.db', 'level2.db', 'level3.db', 'level4.db']

class Game_state(State):
    def __init__(self, view, controller, buttons, background):
        State.__init__(self, view, controller, buttons, background)
        self.actual_level = 0
        self.levels = map(lambda path: Database.load(levels_folder + path, level_key), levels)
        self.player = Player(0, 0)
        self.scores = 0
        pygame.mixer.music.load(game_music_file)
        pygame.mixer.music.play(-1)
        self.frames = 0
        self.fps = 0
        self.show_fps = False
        # zabezpieczyc time_level i times_bonu_przed watkami
        self.set_level()
        self.respawn()
    def set_level(self):
        self.board = self.levels[self.actual_level]
        Dynamic_monster_move.set_objects(self.board.walls_grid, self.board.invisible_walls, self.board.dynamic_monsters_grid, self.board.dynamic_monsters, resolution[1])
    def next_level(self):
        if self.actual_level == len(self.levels) - 1:
            return False
        else:
            self.actual_level += 1
            self.set_level()
            self.player.regenerate_serduszka()
            self.respawn()
            return True
    def zmniejsz_czas_level(self, value):
        if self.remaining_level_time > 0:
            self.remaining_level_time = max(0, self.remaining_level_time -value)
    def zmniejsz_czas_bonus(self, value):
        if self.remaining_bonus_time > 0:
            self.remaining_bonus_time = max(0, self.remaining_bonus_time - value)
        else:
            self.remaining_bonus_time = None
    def respawn(self):
        self.remaining_level_time = LEVEL_TIME
        self.remaining_bonus_time = None
        pygame.time.set_timer(AKTUALIZUJ_CZAS, 10)
        pygame.time.set_timer(MINELA_SEKUNDA_EVENT, 1000)
        pygame.time.set_timer(SKONCZYL_SIE_CZAS_EVENT, LEVEL_TIME)
        self.start_time = time.time()
        (x, y) = (self.board.punkt_startowy.x, self.board.punkt_startowy.y)
        self.player.go_to(x, y)
    def game_over(self):
        scores_list = Database.load(high_scores_file_path, high_scores_key)
        lowest_score = scores_list[0][0]
        if self.scores > lowest_score:
            self.controller.go_wpisywanie_wynikow(self.scores)
        else:
            self.controller.go_high_scores()
    def level_completed(self):
        game_over_sound_effect.play()
        time.sleep(2)
        if not self.next_level():
            self.game_over()
    def add_scores(self, value):
        new_scores = self.scores + value
        if self.scores / 500 != new_scores / 500:
            self.on_bonus()
        self.scores = new_scores
    def on_bonus(self):
        self.remaining_bonus_time = BONUS_TIME
    def actualize_fps(self):
        self.fps = self.frames
        self.frames = 0
    def update(self):
        self.frames += 1
        
        # RUCH SHOT
        for shot in self.board.player_shots:
            if shot.duration == 0 or collision_with_many(shot, self.board.invisible_walls) or self.board.walls_grid.check(shot):
                self.board.player_shots.remove(shot)
            else:
                shot.duration -= 1
                shot.go()
                new_move_vector = rusz_sie_pion(shot, self.board.walls_grid, self.board.invisible_walls, shot)
                new_move_vector = rusz_sie_poziom(shot, self.board.walls_grid, self.board.invisible_walls, new_move_vector)
                
                for monster in self.board.dynamic_monsters_grid.check(new_move_vector):
                    self.add_scores(10)
                    player_trafil_strzalem_sound_effect.play()
                    self.board.dynamic_monsters.remove(monster)
                    self.board.dynamic_monsters_grid.remove(monster)
                
                for monster in self.board.static_monsters_grid.check(new_move_vector):
                    self.add_scores(10)
                    player_trafil_strzalem_sound_effect.play()
                    self.board.static_monsters.remove(monster)
                    self.board.static_monsters_grid.remove(monster)
                

        for shot in self.board.monster_shots:
            if shot.duration == 0 or collision_with_many(shot, self.board.invisible_walls) or self.board.walls_grid.check(shot):
                self.board.monster_shots.remove(shot)
            else:
                shot.duration -= 1
                shot.go()
                new_move_vector = rusz_sie_pion(shot, self.board.walls_grid, self.board.invisible_walls, shot)
                new_move_vector = rusz_sie_poziom(shot, self.board.walls_grid, self.board.invisible_walls, new_move_vector)
                if collision(new_move_vector, self.player) and self.player.pozostaly_czas_niesmiertelnosci == 0:
                    if self.player.strac_serduszko():
                        self.respawn()

        # RUCH DYNAMIC
        for monster in self.board.dynamic_monsters:
            thread = Dynamic_monster_move(monster)
            thread.start()
            thread.join()

        # RUCH STATIC
        for monster in self.board.static_monsters:
            if monster.ready_to_shot:
                monster.ready_to_shot = False
                self.board.monster_shots.append(monster.shot(UP_DIRECTION))
            self.board.static_monsters_grid.remove(monster)
            monster.update_przyciaganie()
            rusz_sie_pion(monster, self.board.walls_grid, self.board.invisible_walls, monster)
            self.board.static_monsters_grid.add(monster)

            if monster.y > resolution[1]:
                self.board.static_monsters_grid.remove(monster)
                self.board.static_monsters.remove(monster)

        # RUCH PLAYER
        # spadniecie gracza
        if self.player.y > resolution[1]:
            self.player.strac_zycie()
            self.respawn()

        self.player.update_poziome_velocities()
        self.player.update_przyciaganie()

        pressed_keys = pygame.key.get_pressed()
        # ustaw bieganie jesli to mozliwe
        self.player.running = pressed_keys[pygame.K_LSHIFT]
        # ustaw poruszanie w lewo jesli to mozliwe
        if pressed_keys[pygame.K_LEFT] and not pressed_keys[pygame.K_RIGHT]:
            self.player.go_left()
        # ustaw poruszanie w prawo jesli to mozliwe
        elif not pressed_keys[pygame.K_LEFT] and pressed_keys[pygame.K_RIGHT]:
            self.player.go_right()
        # ustaw skok jesli to mozliwe
        if pressed_keys[pygame.K_UP]:
            self.player.jump()

        new_move_vector = rusz_sie_poziom(self.player, self.board.walls_grid, self.board.invisible_walls, self.player)
        new_move_vector = rusz_sie_pion(self.player, self.board.walls_grid, self.board.invisible_walls, new_move_vector)

        # kolizja z monetami
        for c in self.board.coins:
            if collision(new_move_vector, c):
                self.add_scores(c.value)
                get_coin_sound_effect.play()
                self.board.coins.remove(c)
            
        # kolizje z potworami
        #if self.player.pozostaly_czas_niesmiertelnosci == 0 and collision_with_many(self.player, self.board.static_monsters + self.board.dynamic_monsters):
        if self.player.pozostaly_czas_niesmiertelnosci == 0 and (self.board.static_monsters_grid.check(self.player) or self.board.dynamic_monsters_grid.check(self.player)):            
            if self.player.strac_serduszko():
                self.respawn()

        # kolizja z end_door
        if self.board.end_game_door and collision(self.player, self.board.end_game_door):
            self.level_completed()
            level_completed_sound_effect.play()

        # gdy wyjdziemy za podloze
        if not self.board.walls_grid.check(self.player.get_podstawe()):
            self.player.on_ground = False

        visible_screen = self.player.get_visible_screen(self.board.w)
        (dx, dy) = ( - visible_screen.x, - visible_screen.y)

        if self.player.zycia == 0:
            self.game_over()
        State.update(self)
        self.view.draw_board(self.board, self.player, dx, dy, GAME_STATE)

        remaining_level_time_text = str(self.remaining_level_time / 1000) + ' : ' + str((self.remaining_level_time / 10) % 100)
        remaining_bonus_time_text = None
        if self.remaining_bonus_time:
            remaining_bonus_time_text = str(self.remaining_bonus_time / 1000) + ' : ' + str((self.remaining_bonus_time / 10) % 100)
        self.view.draw_game_info(self.player.zycia, self.player.serduszka, self.scores, remaining_level_time_text, remaining_bonus_time_text)
        if self.show_fps:
            self.view.draw_text(self.fps, (1600, 50), 40, black)
    def handle(self, event):
        State.handle(self, event)
        if event.type == AKTUALIZUJ_CZAS:
            self.zmniejsz_czas_level(10)
            self.zmniejsz_czas_bonus(10)
            self.player.zmniejsz_czas_niesmiertelnosci(10)
        elif event.type == MINELA_SEKUNDA_EVENT:
            for static_monster in self.board.static_monsters:
                static_monster.ready_to_shot = True
            self.actualize_fps()
        elif event.type == SKONCZYL_SIE_CZAS_EVENT:
            self.player.strac_zycie()
            self.respawn()
        # to delete
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            self.remaining_bonus_time = BONUS_TIME
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_z and self.remaining_bonus_time:
            self.board.player_shots.append(self.player.shot(self.player.direction))
            player_shot_sound_effect.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.show_fps = not self.show_fps
        # do delete
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            self.add_scores(1000)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.controller.change_state(MENU_STATE)
            
view = View(display)
controller = Controller(view)
clock = pygame.time.Clock()

while True:
    controller.update()
    for event in pygame.event.get():
        controller.handle(event)
    pygame.display.update()
    clock.tick(frames_per_second)
