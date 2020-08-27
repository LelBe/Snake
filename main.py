from models import *
import sys


##--MAIN--##

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Snake Game by LelBy')

fichier = "save\\score.txt"

game = Game(screen)
snake = Snake()
apple = Apple()
menu = Menu()

#game.user = input("Entrez votre nom :")

clock = pygame.time.Clock()
game.read_data(fichier)


#Boucle principale
continuer = True

while continuer:
    
    while game.menu_is_running:

        pygame.Surface.fill(screen, (0,0,0))
        screen.blit(menu.banner, (menu.banner_rect))
        screen.blit(menu.play_button,(menu.play_button_rect))
        screen.blit(menu.quit_button,(menu.quit_button_rect))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu.play_button_rect.collidepoint(event.pos):
                    game.start()
                elif menu.quit_button_rect.collidepoint(event.pos):
                    sys.exit()
        
    last_key = "w"
    while game.is_running:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == pygame.K_w:
                if last_key == "s":
                    pass
                else:
                    snake.direction("avance")
                    last_key = "w"
            elif event.type == KEYDOWN and event.key == pygame.K_d:
                if last_key == "a":
                    pass
                else:
                    snake.direction("droite")   
                    last_key = "d"
            elif event.type == KEYDOWN and event.key == pygame.K_s:
                if last_key == "w":
                    pass
                else:
                    snake.direction("recul")   
                    last_key = "s" 
            elif event.type == KEYDOWN and event.key == pygame.K_a:
                if last_key == "d":
                    pass
                else:
                    snake.direction("gauche")   
                    last_key = "a"
            
        #On avance snake d'une certaine vitesse
        snake.avance()

        #On enregistre les positions de la tête
        snake.record_position()

        #On vérifie si la pomme est mangée
        if snake.position_x == apple.apple_pos_x:
            if snake.position_y == apple.apple_pos_y:
                snake.eat(apple)
                game.score += 1

        #On vérifie si le serpent se mort la queue
        for i in range(0, len(snake.body)-1):
            if snake.position_x == snake.body[i][0]:
                if snake.position_y == snake.body[i][1]:
                    snake.is_alive = False    
        
        game.update_screen(snake, apple)
        
        #On vérifie si Snake est en vie
        if snake.is_alive is False:
            if game.score > game.best_score:
                game.best_score = game.score
                game.write_data(fichier)

            game.restart(snake, apple)
            pygame.time.wait(300)
        
        clock.tick(30)
       
        
pygame.quit()