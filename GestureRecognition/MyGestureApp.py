import pygame, sys, os
from pygame.locals import *
import numpy as np

#SETUP CONST
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
FPS = 40

#INIT
pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('MyGestureApp')
timer_event_id = pygame.USEREVENT + 1
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

#VARIABLES
pos_to_draw = []
mouse_clicked = False

gesture_code = []
prev_mnem = ''
mnem = ""
A = -1
B = -1


def DirectionRecognition(A, B, mnem):
    '''Recognize the direction of the gesture'''
    if (A[0] > B[0] + 100) and (A[1] > B[1] + 100):
        mnem = "UL"
    elif (A[0] > B[0] + 100) and (A[1] < B[1] - 100):
        mnem = "DL"
    elif (A[0] < B[0] - 100) and (A[1] > B[1] + 100):
        mnem = "UR"
    elif (A[0] < B[0] - 100) and (A[1] < B[1] - 100):
        mnem = "DR"
    elif A[0] > B[0] + 100:
        mnem = "L"
    elif A[0] < B[0] - 100:
        mnem = "R"
    elif A[1] < B[1] - 100:
        mnem = "D"
    elif A[1] > B[1] + 100:
        mnem = "U"
    return mnem


while True:
    for event in pygame.event.get():
        #QUIT IN CASE OF PRESSING RED X IN WINDOW OR ESC
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        
        #CHECK CURRENT POSITION OF MOUSE CURSOR
        pos = list(pygame.mouse.get_pos())
        
        ##MANAGE MOUSEUP AND MOUSEDOWN
        if event.type == MOUSEBUTTONDOWN:
            mouse_clicked = True
            if A == -1:
                A = pos
            else:
                A = B

        ##RESET PARAMETERS (opcjonalnie można przekazać je do jakiejś dalszej struktury w celu obróbki, analizy)
        if event.type == MOUSEBUTTONUP:
            mouse_clicked = False
            pygame.time.set_timer(timer_event_id, 0)
            mnem = ""
            B = -1
            A = -1
            prev_mnem = ""
            gesture_code.clear()
            pos_to_draw.clear()
            windowSurface.fill((0,0,0))

        #DRAW LINES
        if mouse_clicked == True:
            pos_to_draw.append(pos)
            if A == -1:
                A = pos
            else:
                if B != -1:
                    A = B
            pygame.time.set_timer(timer_event_id, 7)

        if len(pos_to_draw) > 2:
            for i in range(len(pos_to_draw)-1):
                pygame.draw.line(windowSurface, 'white', pos_to_draw[i], pos_to_draw[i+1], 1)

        #CHECK DIRECTION
        if event.type == timer_event_id:
            B = pos
            mnem = DirectionRecognition(A, B, mnem)

            if mnem != prev_mnem:
                gesture_code.append(mnem)
                prev_mnem = mnem
        
        ##SHOW RESULT
        g_code = ",".join(gesture_code)
        text_surface = my_font.render(g_code, False, (155,255,255))
        windowSurface.blit(text_surface,(0,0))

    pygame.display.update()