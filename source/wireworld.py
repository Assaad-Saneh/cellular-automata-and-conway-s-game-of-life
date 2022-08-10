# Control :
#       space_bar: pause the simulation
#       return_key: clear the screen
#       mouse left_click: change the state of the cell(EMPTY->WIRE, WIRE->ELECTRON_HEAD, ELECTRON_HEAD->ELECTRON_TAIL, ELECTRON_TAIL->EMPTY)
#       Tab_key: change grid size
#       escape_key: return to main menu

import app

import pygame
import numpy as np
import sys


COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 75)
COLOR_WIRE = (255, 255, 10)
COLOR_ELECTRON_HEAD = (10, 10, 255)
COLOR_ELECTRON_TAIL = (255, 10, 10)
FPS = 30


def update(screen, cells, size, with_progress = False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        if cells[row,col] == 3:
            neiborhood = cells[row-1:row+2, col-1:col+2]
            alive = np.count_nonzero(neiborhood == 1)

        if cells[row, col] == 0:
            color = COLOR_BG   
        elif cells[row, col] == 1:
            color = COLOR_ELECTRON_HEAD
        elif cells[row, col] == 2:
            color = COLOR_ELECTRON_TAIL
        elif cells[row, col] == 3:
            color = COLOR_WIRE

        if cells[row, col] == 0:
            updated_cells[row, col] = 0

        elif cells[row,col] == 1:
            updated_cells[row,col] = 2
        
        elif cells[row,col] == 2:
            updated_cells[row,col] = 3
        
        elif cells[row,col] == 3:
            if alive == 1 or alive == 2:
                updated_cells[row,col] = 1
            else:
                updated_cells[row,col] = 3

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def wireworld():
    generation = 0
    pygame.init()
    screen = pygame.display.set_mode((1500, 800))
    clock = pygame.time.Clock()

    size = 10

    cells = np.zeros((800 // size, 1500 // size))
    screen.fill(COLOR_GRID)
    update(screen, cells, size)
    
    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    app.main()

                elif event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, size)
                    pygame.display.update()
                elif event.key == pygame.K_RETURN:
                    generation = 0
                    for row, col in np.ndindex(cells.shape):
                        cells[row, col] = 0
                    running = False
                    update(screen, cells, size)
                    pygame.display.update()
                    pygame.display.set_caption("{}".format(generation))
                elif event.key == pygame.K_TAB:
                    size = 20 if size == 10 else 10
                    for row, col in np.ndindex(cells.shape):
                        cells[row, col] = 0
                    running = False
                    update(screen, cells, size)
                    pygame.display.update()
                    
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if cells[pos[1] // size, pos[0] // size] == 0:
                    cells[pos[1] // size, pos[0] // size] = 3

                elif cells[pos[1] // size, pos[0] // size] == 1:
                    cells[pos[1] // size, pos[0] // size] = 2

                elif cells[pos[1] // size, pos[0] // size] == 2:
                    cells[pos[1] // size, pos[0] // size] = 0
                
                elif cells[pos[1] // size, pos[0] // size] == 3:
                    cells[pos[1] // size, pos[0] // size] = 1

                update(screen, cells, size)
                pygame.display.update()
        
        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, size, with_progress=True)
            pygame.display.update()
            generation += 1
            pygame.display.set_caption("{}".format(generation))

        clock.tick(FPS)

if __name__ == "__main__":
    wireworld()