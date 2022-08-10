# Control :
#       space_bar: pause the simulation
#       return_key: clear the screen
#       mouse_wheel: change the element in hand(STONE->EMPTY, EMPTY->SAND, SAND->WATER, WATER-STONE) 
#       mouse left_click: toggle the state of the cell(0->1 and 1->0)
#       escape_key: return to main menu


import app

import random
import pygame
from copy import deepcopy
import numpy as np
from numba import njit


def sand_water():
    RES = WIDTH, HEIGHT = 1500, 800
    TILE = 2
    W, H = WIDTH // TILE, HEIGHT // TILE 
    FPS = 60

    pygame.init()
    surface = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()

    row_max, col_max = RES[1] // TILE - 1, RES[0] // TILE - 1

    current_field = next_field = np.array([[3 if i == 0 or j == 0 or i == W - 1 or j == H - 1 else 0 for i in range (W)] for j in range(H)])

    num = 3

    brush_side = 10

    running = True

    generation = 0

    @njit(fastmath = True)
    def check_cells(current_field, next_field, rand):
        res_s = []
        res_w = []
        res_st = []
        for row,col in np.ndindex(current_field.shape):


            if current_field[row,col] == 1:

                if current_field[row + 1,col] == 0:
                    next_field[row+1,col] = 1
                    next_field[row,col] = 0
                    res_s.append((row+1,col))
                        
                elif current_field[row+1,col] == 2:
                    next_field[row+1,col] = 1
                    next_field[row,col] = 2
                    res_s.append((row+1,col))
                    res_w.append((row,col))
                    

                elif current_field[row+1,col-1]==0:
                    next_field[row+1,col-1] = 1
                    next_field[row,col] = 0
                    res_s.append((row+1,col-1))

                elif current_field[row+1,col-1]==2:
                    next_field[row,col] = 0
                    next_field[row,col-1] = 2
                    next_field[row+1,col -1] = 1
                    res_s.append((row+1,col-1))
                    res_s.append((row,col-1))
                            
                elif current_field[row+1,col+1]==0:
                    next_field[row+1,col+1] = 1
                    next_field[row,col] = 0
                    res_s.append((row+1,col+1))

                elif current_field[row+1,col+1]==2:
                    next_field[row,col] = 0
                    next_field[row,col +1] = 2
                    next_field[row+1,col+1] = 1
                    res_s.append((row+1,col+1))
                    res_s.append((row,col+1))
                    
                else:
                    next_field[row,col] = 1
                    res_s.append((row,col))


            elif current_field[row,col] == 2:
                if current_field[row+1,col] == 0 :
                    next_field[row+1,col] = 2
                    next_field[row,col] = 0
                    res_w.append((row+1,col))

                elif current_field[row+1,col-1]==0:
                    next_field[row+1,col -1] = 2
                    next_field[row,col] = 0
                    res_w.append((row+1,col-1))
                            
                elif current_field[row+1,col+1]==0:
                    next_field[row+1,col+1] = 2
                    next_field[row,col] = 0
                    res_w.append((row+1,col+1))

                elif current_field[row,col+1] == 0 and current_field[row,col-1] == 0 and next_field[row,col - 1] == 0 and next_field[row,col + 1] == 0:
                    next_field[row,col+ rand] = 2
                    next_field[row,col] = 0
                    res_w.append((row,col + rand))

                elif current_field[row,col+1] == 0 and next_field[row,col + 1] == 0:
                    next_field[row,col+1] = 2
                    next_field[row,col] = 0
                    res_w.append((row,col+1))

                elif current_field[row,col-1] == 0 and next_field[row,col - 1] == 0:
                    next_field[row,col-1] = 2
                    next_field[row,col] = 0
                    res_w.append((row,col-1))

                else:
                    next_field[row,col] = 2
                    res_w.append((row,col))

            elif current_field[row,col] == 3:
                next_field[row,col] = 3
                res_st.append((row,col))

        return next_field, res_s, res_w, res_st
                    

    while True:
        surface.fill(pygame.Color("black"))
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
                    current_field = next_field = np.array([[3 if i == 0 or j == 0 or i == W - 1 or j == H - 1 else 0 for i in range (W)] for j in range(H)])
                    pygame.display.flip()
                    pygame.display.set_caption("{}".format(generation))
                
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                if pos[1] // TILE <  row_max - brush_side  - 1 and pos[0] // TILE < col_max - brush_side - 1 and pos[1] // TILE > brush_side +1 and pos[0] // TILE > brush_side + 1:
                    if num != 3:
                        for i in range(-brush_side, brush_side):
                            for j in range(-brush_side,brush_side):
                                current_field[pos[1] // TILE + i, pos[0] // TILE + j] = random.choice((0,0,0,num))
                    else:
                        for i in range(-brush_side//2, brush_side//2):
                            for j in range(-brush_side//2,brush_side//2):
                                current_field[pos[1] // TILE + i, pos[0] // TILE + j] = 3

            if event.type == pygame.MOUSEWHEEL:
                if event.y == -1:
                    num = 0 if num == 1 else 1 if num == 2 else 2 if num == 3 else 3 
                else:
                    num = 1 if num == 0 else 2 if num == 1 else 3 if num == 2 else 0 

            
        if running:
            next_field, res_s, res_w, res_st = check_cells(current_field, next_field, rand = random.choice((-1,1)))
            [pygame.draw.rect(surface, pygame.Color('blue'), (y * TILE + 1 ,x * TILE + 1, TILE, TILE)) for x,y in res_w]
            [pygame.draw.rect(surface, pygame.Color('yellow'), (y * TILE + 1 ,x * TILE + 1, TILE, TILE)) for x,y in res_s]
            [pygame.draw.rect(surface, pygame.Color('grey'), (y * TILE + 1 ,x * TILE + 1, TILE, TILE)) for x,y in res_st]
                
            current_field = deepcopy(next_field)
            pygame.display.flip()

            generation += 1
            pygame.display.set_caption("{}".format(generation))

        clock.tick(FPS)


if __name__ == '__main__':
    sand_water()