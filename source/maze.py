# Control :
#       space_bar: pause the simulation
#       return_key: clear the screen
#       mouse left_click: toggle the state of the cell(0->1 and 1->0)
#       Tab_key: change grid size
#       escape_key: return to main menu

import app

import pygame
import numpy as np
import sys

COLOR_BG = (255, 255, 255)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (70, 70, 70)
COLOR_ALIVE_NEXT = (10, 10, 10)
FPS = 30


def update(screen, cells, size, with_progress = False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 1 or alive > 5:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 1 <= alive <= 5 :
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def maze():
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
                    cells[pos[1] // size, pos[0] // size] = 1
                else:
                    cells[pos[1] // size, pos[0] // size] = 0
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
    maze()