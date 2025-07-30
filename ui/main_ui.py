import pygame, sys
from pygame.locals import *
#from constants import *
from ui.constants import *
from ui.choice import *
from ui.image import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
title = pygame.display.set_caption('WumPus Game')

def showWumpusWorld(choose_map_result, map):
    M1 = Map(screen, map)
    showGameBackground(screen, level=choose_map_result)
    M1.showUnknownBoard()
    I1 = Info(screen, level=choose_map_result)
    I1.showLeftBar(choose_map_result, point=10000, HP=100, H_Ps=0)
    I1.showNoti(0)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                    return
        pygame.display.update()

def showAgentMove(choose_map_result, path, m, level):
    # path: (pos-y, pos-x), action, point, HP, Healing Potion(s)
    # maps: element, stench, breeze, whiff, glow, scream
    # element in maps: 'W', 'P', 'G', '-'
    I2 = Info(screen, level=level)
    I2.showNoti(1)
    isMoving = True
    drirection = 1 # mod = 0: right, 1: up, 2: left, 3: down
    time_wait_1 = 50
    time_wait_2 = 100
    time_wait_3 = 300
    time_wait_4 = 1200
    maps = []
    for _ in range(len(m)):
        maps.append([])
        for y in range(len(m[_])):
            maps[_].append([])
            for x in range(len(m[_][y])):
                maps[_][y].append([m[_][y][x].element, m[_][y][x].is_stench, m[_][y][x].is_breeze, m[_][y][x].is_whiff, m[_][y][x].is_glow, m[_][y][x].is_scream])
    count_map = 1
    M2 = Map(screen, maps[0])
    while True:
        if isMoving:# and len(path) > 0:
            y_shoot, x_shoot = -1, -1
            for _ in range(len(path)):
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                            return
                if _ > 0:
                    M2.showPath(path[_-1][0][0], path[_-1][0][1])
                if path[_][1] == 'Turn Left':
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_1)
                    drirection = M2.turnLeft(drirection)
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_2)
                elif path[_][1] == 'Turn Right':
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_1)
                    drirection = M2.turnRight(drirection)
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_2)
                if path[_][1] == 'Grab Gold':
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
                    M2.showGold(path[_][0][0], path[_][0][1], M2.h)
                    # I2.showPoint(path[_][2], is_gold=True)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_4)
                    M2.updateMap(maps[count_map])
                    count_map += 1
                if path[_][1] == 'Grab Heal':
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
                    M2.showHealingPotion(path[_][0][0], path[_][0][1], M2.h)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_4)
                    M2.updateMap(maps[count_map])
                    count_map += 1
                for __ in range(_+1):
                    M2.showPath(path[__][0][0], path[__][0][1])
                M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
                if path[_][1] == 'Shoot':
                    M2.showPath(path[_][0][0], path[_][0][1])
                    M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
                    y_shoot, x_shoot = M2.agentShoot(path, _, drirection)
                    if M2.map_data[path[_][0][0]][path[_][0][1]][5]:
                        M2.showScream(path[_][0][0], path[_][0][1], M2.h)
                        pygame.display.flip()
                        pygame.time.wait(time_wait_4)
                    else:
                        pygame.display.flip()
                        pygame.time.wait(time_wait_3)
                    M2.updateMap(maps[count_map])
                    count_map += 1
                if _ > 0 and path[_][1] != 'Shoot' and path[_-1][1] == 'Shoot':
                    M2.showUnknown(y_shoot, x_shoot, M2.h)
                # if _ > 0 or (_ == 0 and path[0][3] < 100):
                #     if path[_][3] > path[_-1][3]:
                #         I2.showHP(path[_-1][3], is_heal=True)
                #         pygame.display.flip()
                #         pygame.time.wait(time_wait_4)
                #     elif path[_][3] < path[_-1][3]:
                #         I2.showHP(path[_-1][3], is_damaged=True)
                #         pygame.display.flip()
                #         pygame.time.wait(time_wait_4)
                #     elif _ == 0 and path[0][3] < 100:
                #         I2.showHP(path[_][3], is_damaged=True)
                #         pygame.display.flip()
                #         pygame.time.wait(time_wait_4)
                I2.showLeftBar(choose_map_result, path[_][2], path[_][3], path[_][4])
                pygame.display.flip()
                pygame.time.wait(time_wait_1)
            if path[-1][3] == 0:
                I2.showNoti(3)
            elif path[-1][1] == 'Climb':
                I2.showNoti(2)
                M2.showPath(path[-1][0][0], path[-1][0][1])
            elif path[-1][1] != 'Climb':
                I2.showNoti(4)
                M2.showPath(path[-1][0][0], path[-1][0][1])
                M2.showDie(path[_][0][0], path[_][0][1], M2.h)
            I2.showLeftBar(choose_map_result, path[-1][2], path[-1][3], path[-1][4])
            pygame.display.flip()
            isMoving = False
        elif len(path) == 0:
            isMoving = False
            I2.showNoti(4)
            I2.showLeftBar(choose_map_result)
            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                        return


def showMenu():
    showMenuBackground(screen)
    choose_option = None
    menuChoice = ['Play', 'Quit']
    menu = Choice(screen, menuChoice, 'WumPus Game')
    map_choose_option = None
    mapChoice = ['Map 01', 'Map 02', 'Map 03', 'Map 04', 'Map 05']
    mapMenu = Choice(screen, mapChoice, '')
    mapChoice_2 = ['Map 06', 'Map 07', 'Map 08', 'Map 09', 'Map 10']
    mapMenu_2 = Choice(screen, mapChoice_2, '')

    while True:
        is_up = False
        is_down = False
        is_left = False
        is_right = False
        is_enter = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_down = True
                elif event.key == pygame.K_UP and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_up = True
                elif event.key == pygame.K_LEFT and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_left = True
                elif event.key == pygame.K_RIGHT and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_right = True
                elif (event.key == pygame.K_RETURN or event.key == K_KP_ENTER) and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
                    is_enter = True
        
        if choose_option is None:
            menu.display_option(is_up, is_down, is_left, is_right, is_enter)
            choose_option = menu.get_option_result()
        else:
            if choose_option == 0:
                if map_choose_option is None:                    
                    mapMenu.display_option(is_up, is_down, is_left, is_right, is_enter)
                    map_choose_option = mapMenu.get_option_result()
                else:
                    return map_choose_option
                if is_left:
                    choose_option = mapMenu.get_back_to(None, 0)
                if is_right:
                    choose_option = mapMenu.get_next_to(-1, 0)
            if choose_option == 1:
                pygame.quit()
                sys.exit()
            if choose_option == -1: # input page 2
                if map_choose_option is None:                    
                    mapMenu_2.display_option(is_up, is_down, is_left, is_right, is_enter, can_next=False)
                    map_choose_option = mapMenu_2.get_option_result()
                else:
                    return map_choose_option + 5
                if is_left:
                    choose_option = mapMenu_2.get_back_to(0, -1)
        pygame.display.update()

#(base) D:\HCMUS\Co so AI\CSC14003 - Introduction to AI\Proj2\Project-2-Logical-Agent\Source>
#day la main ui, chua ket noi voi main toan chuong trinh
#[element, stench, breeze, whiff, glow, scream]
# [ ['-'] True True False False ] [ ['W', 'P', 'G'] False False False False ] [ ['-'] True True False False ] [ ['-'] False False False False ]
# [ ['-'] False False False False ] [ ['G'] True True False False ] [ ['P'] False False False False ] [ ['-'] False True False False ]
# [ ['-'] False False False False ] [ ['-'] False False False False ] [ ['-'] False True False False ] [ ['-'] False True False False ]
# [ ['-'] False False False False ] [ ['-'] False False False False ] [ ['-'] False True False False ] [ ['P'] False False False False ]