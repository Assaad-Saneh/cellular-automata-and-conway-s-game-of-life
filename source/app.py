import gol_play
import wireworld
import brianbrain
import gameoflife
import sand_water
import maze

import pygame
import sys

def main():
    pygame.display.set_caption("Cellular Automata And Coneway's Game of Life")

    pygame.font.init()

    bg_img = pygame.image.load('assets\mrbiggles-ca-internal-1.jpg')
    bg_img = pygame.transform.scale(bg_img, (1500,800))

    dark_filter = pygame.Surface((1500,800))
    dark_filter.set_alpha(100)
    dark_filter.fill((10,10,10))

    dark_section = pygame.Surface((500,800))
    dark_section.set_alpha(200)
    dark_section.fill((10,10,10))


    font = pygame.font.Font("font.otf", 25)
    title = font.render("Cellular Automata and Game of life", False, (255,255,255))
    credit1 = font.render("Assaad Saneh (1966)", False,(255,255,255))


    button_1 = pygame.Rect(100, 150, 300, 75)
    box1 = pygame.Rect(105,155,290,65)
    text1 = font.render("Game Of Life", False,(255,255,255))

    button_2 = pygame.Rect(100, 375, 300, 75)
    box2 = pygame.Rect(105,380,290,65)
    text2 = font.render("Wire World", False,(255,255,255))

    button_3 = pygame.Rect(100, 600, 300, 75)
    box3 = pygame.Rect(105,605,290,65)
    text3 = font.render("Brian's Brain", False,(255,255,255))

    button_4 = pygame.Rect(1100, 150, 300, 75)
    box4 = pygame.Rect(1105,155,290,65)
    text4 = font.render("GOL Hardcore", False,(255,255,255))

    button_5 = pygame.Rect(1100, 375, 300, 75)
    box5 = pygame.Rect(1105,380,290,65)
    text5 = font.render("Sand & Water", False,(255,255,255))

    button_6 = pygame.Rect(1100, 600, 300, 75)
    box6 = pygame.Rect(1105,605,290,65)
    text6 = font.render("Maze generation", False,(255,255,255))


    click = False
    pygame.init()

    screen = pygame.display.set_mode((1500, 800))
    clock = pygame.time.Clock()

    while True:

        screen.blit(bg_img,(0,0))
        screen.blit(dark_filter,(0,0))
        screen.blit(dark_section,(0,0))
        screen.blit(dark_section,(1000,0))
        screen.blit(title, (510,150))
        screen.blit(credit1, (610,370))

        pygame.draw.rect(screen, (255,255,255), button_1)
        pygame.draw.rect(screen, (10,10,10), box1)
        screen.blit(text1, (160,175))

        pygame.draw.rect(screen, (255,255,255), button_2)
        pygame.draw.rect(screen, (10,10,10), box2)
        screen.blit(text2, (175,400))

        pygame.draw.rect(screen, (255,255,255), button_3)
        pygame.draw.rect(screen, (10,10,10), box3)
        screen.blit(text3, (160,625))

        pygame.draw.rect(screen, (255,255,255), button_4)
        pygame.draw.rect(screen, (10,10,10), box4)
        screen.blit(text4, (1155,175))
        
        pygame.draw.rect(screen, (255,255,255), button_5)
        pygame.draw.rect(screen, (10,10,10), box5)
        screen.blit(text5, (1160,400))

        pygame.draw.rect(screen, (255,255,255), button_6)
        pygame.draw.rect(screen, (10,10,10), box6)
        screen.blit(text6, (1135,625))

        pygame.display.flip()
        pygame.display.update()


        mx, my = pygame.mouse.get_pos()

        if button_1.collidepoint((mx,my)):
            if click:
                gol_play.gol_play()
            else:
                pass
        
        if button_2.collidepoint((mx,my)):
            if click:
                wireworld.wireworld()
            else:
                pass

        if button_3.collidepoint((mx,my)):
            if click:
                brianbrain.brianbrain()
            else:
                pass
        
        if button_4.collidepoint((mx,my)):
            if click:
                gameoflife.game_of_life()
            else:
                pass

        if button_5.collidepoint((mx,my)):
            if click:
                sand_water.sand_water()
            else:
                pass

        if button_6.collidepoint((mx,my)):
            if click:
                maze.maze()
            else:
                pass
        
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

if __name__ == '__main__':
    main()