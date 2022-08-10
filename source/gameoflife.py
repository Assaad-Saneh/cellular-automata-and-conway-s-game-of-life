# Control :
#       numbers 1,2,3,4,5,6 : different starting patterns
#       space_bar: pause the simulation
#       return_key: clear the screen
#       number 0: custom playground where you deploy different ships and oscilators in a space themed background
#       mouse left_click: deploy random spaceship when in the custom playground
#       escape_key: return to main menu


import app

import pygame
from copy import deepcopy
import numpy as np
from numba import njit
import random



def game_of_life():
    RES = WIDTH, HEIGHT = 1500, 800
    TILE = 2
    W, H = WIDTH // TILE, HEIGHT // TILE 
    FPS = 30

    copperhead = np.array([[0,1,1,0,0,1,1,0],
                           [0,0,0,1,1,0,0,0],
                           [0,0,0,1,1,0,0,0],
                           [1,0,1,0,0,1,0,1],
                           [1,0,0,0,0,0,0,1],
                           [0,0,0,0,0,0,0,0],
                           [1,0,0,0,0,0,0,1],
                           [0,1,1,0,0,1,1,0],
                           [0,0,1,1,1,1,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,1,1,0,0,0],
                           [0,0,0,1,1,0,0,0]])

    oscillaing_pattern = np.array([[0,0,1,1,1,0,0,0,1,1,1,0,0],
                                   [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                   [1,0,0,0,0,1,0,1,0,0,0,0,1],
                                   [1,0,0,0,0,1,0,1,0,0,0,0,1],
                                   [1,0,0,0,0,1,0,1,0,0,0,0,1],
                                   [0,0,1,1,1,0,0,0,1,1,1,0,0],
                                   [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                   [0,0,1,1,1,0,0,0,1,1,1,0,0],
                                   [1,0,0,0,0,1,0,1,0,0,0,0,1],
                                   [1,0,0,0,0,1,0,1,0,0,0,0,1],
                                   [1,0,0,0,0,1,0,1,0,0,0,0,1],
                                   [0,0,0,0,0,0,0,0,0,0,0,0,0],
                                   [0,0,1,1,1,0,0,0,1,1,1,0,0],])

    doo_dah = np.array([[0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0],
                       [1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0],
                       [1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
                       [0,0,1,1,1,0,0,1,0,0,1,0,0,1,1,1,0,0],
                       [0,0,0,1,1,0,1,1,0,0,1,1,0,1,1,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0],
                       [0,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
                       [0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0],
                       [0,0,0,1,0,1,0,1,0,0,1,0,1,0,1,0,0,0],
                       [0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
                       [1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1],
                       [1,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,1],
                       [0,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,1,0]])

    schick_engine = np.array([[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                             [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
                             [1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
                             [0,1,0,0,1,0,0,1,1,0,0,0,0,0,1,1,1,0],
                             [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1],
                             [0,1,0,0,1,0,0,1,1,0,0,0,0,0,1,1,1,0],
                             [1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
                             [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
                             [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    glider_gun = np.array([[0,0,1,1,0,0,0,0,0],
                           [0,0,1,1,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [1,1,0,0,0,1,1,0,0],
                           [0,0,1,1,1,0,0,0,0],
                           [0,1,0,0,0,1,0,0,0],
                           [0,0,1,0,1,0,0,0,0],
                           [0,0,0,1,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,1,1,1,0,0],
                           [0,0,0,0,1,1,1,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,1,1,0,0,0,1,1],
                           [0,0,0,1,1,1,1,1,0],
                           [0,0,0,0,1,1,1,0,0],
                           [0,0,0,0,0,1,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,1,1,0,0,0],
                           [0,0,0,0,1,1,0,0,0]])
    
    spaceship = np.array([[0,1,1,0,0,0,0,1,1],
                          [1,0,0,1,1,0,1,1,1],
                          [0,1,0,1,0,0,0,0,0],
                          [0,0,1,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,1],
                          [0,0,0,0,0,0,1,1,1],
                          [0,0,0,0,0,1,0,0,0],
                          [0,0,0,0,0,0,1,1,0],
                          [0,0,0,0,0,0,0,1,0]])

    pygame.init()
    surface = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()

    running = True
    
    color = 'green'
    img = pygame.image.load('assets\\62eaa7741e8ee.jpg')
    img = pygame.transform.scale(img, (WIDTH,HEIGHT))

    ships = False

    next_field = np.array([[0 for i in range(W)] for j in range(H)])

    current_field = np.array([[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)])

    generation = 0

    @njit(fastmath = True)
    def check_cells(current_field, next_field):
        res = []
        for y in range(W - TILE):
            for x in range(H - TILE):
                count = np.sum(current_field[x-1:x+2, y-1:y+2]) - current_field[x, y]
                    
                if current_field[x][y] == 1:
                    if count == 2 or count == 3:
                        next_field[x][y] = 1
                        res.append((x,y))
                    else:
                        next_field[x][y] = 0
                else:
                    if count == 3:
                        next_field[x][y] = 1
                        res.append((x,y))
                    else:
                        next_field[x][y] = 0
        
        return next_field, res

    while True:
        if not ships:
            surface.fill(pygame.Color("black"))
        else:
            surface.blit(img, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit()
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app.main()

                elif event.key == pygame.K_SPACE:
                    running = not running
                elif event.key == pygame.K_RETURN:
                    generation = 0
                    current_field = np.zeros((H,W))
                    next_field = np.zeros((H,W))
                    pygame.display.flip()
                    running = False
                    pygame.display.set_caption("{}".format(generation))

                elif event.key == pygame.K_0:
                    surface.blit(img, (0,0))
                    generation = 0
                    current_field = np.zeros((H,W))
                    next_field = np.zeros((H,W))
                    pygame.display.flip()
                    pygame.display.set_caption("{}".format(generation))
                    
                    running = False
                    ships = True

                elif event.key == pygame.K_1:
                    generation = 0
                    ships = False
                    current_field = np.zeros((H,W))
                    next_field = np.zeros((H,W))
                    pygame.display.flip()
                    running = False

                    current_field = np.array([[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)])
                    next_field, res = check_cells(current_field, next_field)
                    pygame.display.set_caption("{}".format(generation))
                    
                    color = 'green'

                    running = True

                elif event.key == pygame.K_2:
                    generation = 0
                    ships = False
                    current_field = np.zeros((H,W))
                    next_field = np.zeros((H,W))
                    pygame.display.flip()
                    running = False
                    
                    current_field = np.array([[0 for i in range(W)] for j in range(H)])
                    for i in range(H):
                        current_field[i][i + (W - H) // 2] = 1
                        current_field[H - i - 1][i + (W - H) // 2] = 1
                    next_field, res = check_cells(current_field, next_field)
                    pygame.display.set_caption("{}".format(generation))
                    
                    color = 'gold1'

                    running = True

                elif event.key == pygame.K_3:
                    generation = 0
                    ships = False
                    current_field = np.zeros((H,W))
                    next_field = np.zeros((H,W))
                    pygame.display.flip()
                    running = False

                    current_field = np.array([[1 if not (i * j) % 22 else 0 for i in range(W)] for j in range(H)])
                    next_field, res = check_cells(current_field, next_field)
                    pygame.display.set_caption("{}".format(generation))

                    color = 'firebrick1'

                    running = True

                elif event.key == pygame.K_4:
                    generation = 0
                    ships = False
                    current_field = np.zeros((H,W))
                    next_field = np.zeros((H,W))
                    pygame.display.flip()
                    running = False

                    current_field = np.array([[1 if not i % 9 else 0 for i in range(W)] for j in range(H)])
                    next_field, res = check_cells(current_field, next_field)
                    pygame.display.set_caption("{}".format(generation))

                    color = 'chartreuse'
                    
                    running = True

                elif event.key == pygame.K_5:
                    generation = 0
                    ships = False
                    current_field = np.zeros((H,W))
                    next_field = np.zeros((H,W))
                    pygame.display.flip()
                    running = False

                    current_field = np.array([[1 if not (2 * i + j) % 4 else 0 for i in range(W - TILE)] for j in range(H - TILE)])
                    next_field, res = check_cells(current_field, next_field)
                    pygame.display.set_caption("{}".format(generation))

                    color = 'cyan'
                    
                    running = True

            if pygame.mouse.get_pressed()[0] and ships:
                    running = True
                    pos = pygame.mouse.get_pos()

                    rand = random.choice((0,1,2,3,4,5))

                    if rand == 0:
                        rand_ship = copperhead
                    elif rand == 1:
                        rand_ship = oscillaing_pattern
                    elif rand == 2:
                        rand_ship = doo_dah
                    elif rand == 3:
                        rand_ship = schick_engine
                    elif rand == 4:
                        rand_ship = glider_gun
                    elif rand == 5:
                        rand_ship = spaceship
                    

                    if RES[1] - pos[1] // TILE > np.shape(rand_ship)[0] and RES[0] - pos[0] // TILE > np.shape(rand_ship)[1]:
                        for row in range(len(rand_ship)):
                            for col  in range(len(rand_ship[0])):
                                current_field[pos[1] // TILE + row, pos[0] // TILE + col] = rand_ship[row,col]
                        
                        next_field, res = check_cells(current_field, next_field)
                        color = 'gold'

                    running = True

                

        #draw life
        if running:
            next_field, res = check_cells(current_field, next_field)
            [pygame.draw.rect(surface, pygame.Color(color), (y * TILE + 1 ,x * TILE + 1, TILE - 1, TILE - 1)) for x,y in res]
            current_field = deepcopy(next_field)
            pygame.display.flip()
            generation += 1
            pygame.display.set_caption("{}".format(generation))

        clock.tick(FPS)

if __name__ == '__main__':
    game_of_life()