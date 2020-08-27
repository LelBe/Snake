import pygame
from pygame.locals import *
import random

GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
WIDTH = 600
HEIGHT = 600


class Game:
    
    def __init__(self, screen):
        
        self.screen = screen
        self.is_running = False
        self.menu_is_running = True
        self.score = 0
        self.best_score = 0
        self.user = ""

        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.font_score = pygame.font.Font('freesansbold.ttf', 22)
        

    def update_screen(self, snake, apple):
        
        #On actualise le jeu
        pygame.Surface.fill(self.screen, (0,0,0))
        snake.update(self)
        apple.update(self)

        #On actualise le score board
        score_text = self.font_score.render(str(self.score), True, WHITE)
        best_score_text = self.font_score.render("Best : " + str(self.best_score), True, WHITE)
        self.screen.blit(score_text, (10,20))
        self.screen.blit(best_score_text, (10, 60))
        
        #On actualise pygame
        pygame.display.flip()

    def start(self):
        self.is_running = True
        self.menu_is_running = False

    def restart(self, snake, apple):
        self.is_running = False
        self.menu_is_running = True

        snake.reset()
        apple.reset()
        self.score = 0

    def read_data(self, fichier):
        score = {}
        with open(fichier, "r") as mon_fichier:
            fichier_score = mon_fichier.readlines()

            for lines in fichier_score:
                lines = lines.strip("\n")
                lines = lines.split(":")
                score[lines[0]] = lines[1]

            for data in score.values():
                data = int(data) 
                if data > self.best_score:
                    self.best_score = data

    def write_data(self, fichier):

        with open(fichier, "a") as mon_fichier :
            mon_fichier.write(self.user + ":" + str(self.score) + "\n")
        
                   

class Apple:

    def __init__(self):
        self.apple_image = pygame.image.load("ressources\\images\\pomme.png")
        self.apple_image = pygame.transform.scale(self.apple_image, (10,10))
        self.apple_rect = self.apple_image.get_rect()
        self.apple_pos_x = 300
        self.apple_pos_y = 200
        self.apple_rect.x = self.apple_pos_x
        self.apple_rect.y = self.apple_pos_y

    def create_apple(self):
        self.apple_pos_x = random.randrange(0, 600, 10)
        self.apple_pos_y = random.randrange(0, 600, 10)
        self.apple_rect.x = self.apple_pos_x
        self.apple_rect.y = self.apple_pos_y

    def update(self, ecran):
        ecran.screen.blit(self.apple_image, self.apple_rect)

    def reset(self):
        self.apple_pos_x = 300
        self.apple_pos_y = 200
        self.apple_rect.x = self.apple_pos_x
        self.apple_rect.y = self.apple_pos_y

class Snake:

    def __init__(self):
        self.eat_sound = pygame.mixer.Sound("ressources\\sound\\croc.wav")
        self.position_x = 300
        self.position_y = 500
        self.direction_x = 0
        self.direction_y = -10
        self.length = 4
        self.body = []
        self.is_alive = True

    def direction(self, direction):

        if direction == "avance":
            self.direction_x = 0
            self.direction_y = -10
        elif direction == "droite":
            self.direction_x = 10
            self.direction_y = 0
        elif direction == "recul":
            self.direction_x = 0
            self.direction_y = 10
        elif direction == "gauche":
            self.direction_x = -10
            self.direction_y = 0
        
    def avance(self):
        self.position_x += self.direction_x
        self.position_y += self.direction_y 

        if self.position_x > WIDTH :
            self.position_x = 0
        elif self.position_x < 0:
            self.position_x = WIDTH 
        elif self.position_y > HEIGHT :
            self.position_y = 0
        elif self.position_y < 0:
            self.position_y = HEIGHT

    def record_position(self):
        pos_tete = [self.position_x, self.position_y]
        self.body.append(pos_tete)
        
        if len(self.body) > self.length:
            del self.body[0]

    def eat(self, apple):
        self.eat_sound.play()
        apple.create_apple()
        self.length += 4

    def update(self, ecran):

        for i in range(0, len(self.body)):
            snake_refresh = pygame.draw.rect(ecran.screen, (0,0,0), Rect(self.body[i][0], self.body[i][1], 10, 10))
            snake_refresh_block = pygame.draw.rect(ecran.screen, (0,255,0), Rect(self.body[i][0] + 2, self.body[i][1] + 2, 8, 8))

    def reset(self):
        self.position_x = 300
        self.position_y = 500
        self.direction_x = 0
        self.direction_y = -10
        self.length = 4
        self.body = []
        self.is_alive = True


class Menu:

    def __init__(self):
        self.play_button = pygame.image.load("ressources\\images\\play_button.png").convert_alpha()
        self.quit_button = pygame.image.load("ressources\\images\\quit_button.png").convert_alpha()
        self.banner = pygame.image.load("ressources\\images\\snake.png").convert_alpha()

        self.banner = pygame.transform.scale(self.banner, (422,99))
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.x = 95
        self.banner_rect.y = 95

        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = 220
        self.play_button_rect.y = 250

        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_button_rect.x = 218
        self.quit_button_rect.y = 350
