# import pygame, sys
# from pygame.locals import *
# #from constants import *
# from ui.constants import *
# from ui.choice import *
# from ui.image import *

# pygame.init()
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# title = pygame.display.set_caption('WumPus Game')

# def showWumpusWorld(choose_map_result, map):
#     M1 = Map(screen, map)
#     showGameBackground(screen, level=choose_map_result)
#     M1.showUnknownBoard()
#     I1 = Info(screen, level=choose_map_result)
#     I1.showLeftBar(choose_map_result, point=10000, HP=100, H_Ps=0)
#     I1.showNoti(0)
#     pygame.display.update()

#     # Wait 2 seconds before starting agent movement
#     pygame.time.wait(2000)

# # def showAgentMove(choose_map_result, path, m, level):
# #     # path: (pos-y, pos-x), action, point, HP, Healing Potion(s)
# #     # maps: element, stench, breeze, whiff, glow, scream
# #     # element in maps: 'W', 'P', 'G', '-'
# #     I2 = Info(screen, level=level)
# #     I2.showNoti(1)
# #     isMoving = True
# #     drirection = 1 # mod = 0: right, 1: up, 2: left, 3: down
# #     time_wait_1 = 50
# #     time_wait_2 = 100
# #     time_wait_3 = 300
# #     time_wait_4 = 1200
# #     maps = []
# #     for _ in range(len(m)):
# #         maps.append([])
# #         for y in range(len(m[_])):
# #             maps[_].append([])
# #             for x in range(len(m[_][y])):
# #                 maps[_][y].append([m[_][y][x].element, m[_][y][x].is_stench, m[_][y][x].is_breeze, m[_][y][x].is_whiff, m[_][y][x].is_glow, m[_][y][x].is_scream])
# #     count_map = 1
# #     M2 = Map(screen, maps[0])
# #     while True:
# #         if isMoving:# and len(path) > 0:
# #             y_shoot, x_shoot = -1, -1
# #             for _ in range(len(path)):
# #                 for event in pygame.event.get():
# #                     if event.type == QUIT:
# #                         pygame.quit()
# #                         sys.exit()
# #                     if event.type == pygame.KEYDOWN:
# #                         if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
# #                             return
# #                 if _ > 0:
# #                     M2.showPath(path[_-1][0][0], path[_-1][0][1])
# #                 if path[_][1] == 'Turn Left':
# #                     M2.showPath(path[_][0][0], path[_][0][1])
# #                     M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
# #                     pygame.display.flip()
# #                     pygame.time.wait(time_wait_1)
# #                     drirection = M2.turnLeft(drirection)
# #                     M2.showPath(path[_][0][0], path[_][0][1])
# #                     M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
# #                     pygame.display.flip()
# #                     pygame.time.wait(time_wait_2)
# #                 elif path[_][1] == 'Turn Right':
# #                     M2.showPath(path[_][0][0], path[_][0][1])
# #                     M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
# #                     pygame.display.flip()
# #                     pygame.time.wait(time_wait_1)
# #                     drirection = M2.turnRight(drirection)
# #                     M2.showPath(path[_][0][0], path[_][0][1])
# #                     M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
# #                     pygame.display.flip()
# #                     pygame.time.wait(time_wait_2)
# #                 if path[_][1] == 'Grab Gold':
# #                     M2.showPath(path[_][0][0], path[_][0][1])
# #                     M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
# #                     M2.showGold(path[_][0][0], path[_][0][1], M2.h)
# #                     # I2.showPoint(path[_][2], is_gold=True)
# #                     pygame.display.flip()
# #                     pygame.time.wait(time_wait_4)
# #                     M2.updateMap(maps[count_map])
# #                     count_map += 1
# #                 if path[_][1] == 'Grab Heal':
# #                     M2.showPath(path[_][0][0], path[_][0][1])
# #                     M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
# #                     M2.showHealingPotion(path[_][0][0], path[_][0][1], M2.h)
# #                     pygame.display.flip()
# #                     pygame.time.wait(time_wait_4)
# #                     M2.updateMap(maps[count_map])
# #                     count_map += 1
# #                 for __ in range(_+1):
# #                     M2.showPath(path[__][0][0], path[__][0][1])
# #                 M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
# #                 if path[_][1] == 'Shoot':
# #                     M2.showPath(path[_][0][0], path[_][0][1])
# #                     M2.showAgent(path[_][0][0], path[_][0][1], M2.h)
# #                     y_shoot, x_shoot = M2.agentShoot(path, _, drirection)
# #                     if M2.map_data[path[_][0][0]][path[_][0][1]][5]:
# #                         M2.showScream(path[_][0][0], path[_][0][1], M2.h)
# #                         pygame.display.flip()
# #                         pygame.time.wait(time_wait_4)
# #                     else:
# #                         pygame.display.flip()
# #                         pygame.time.wait(time_wait_3)
# #                     M2.updateMap(maps[count_map])
# #                     count_map += 1
# #                 if _ > 0 and path[_][1] != 'Shoot' and path[_-1][1] == 'Shoot':
# #                     M2.showUnknown(y_shoot, x_shoot, M2.h)
# #                 # if _ > 0 or (_ == 0 and path[0][3] < 100):
# #                 #     if path[_][3] > path[_-1][3]:
# #                 #         I2.showHP(path[_-1][3], is_heal=True)
# #                 #         pygame.display.flip()
# #                 #         pygame.time.wait(time_wait_4)
# #                 #     elif path[_][3] < path[_-1][3]:
# #                 #         I2.showHP(path[_-1][3], is_damaged=True)
# #                 #         pygame.display.flip()
# #                 #         pygame.time.wait(time_wait_4)
# #                 #     elif _ == 0 and path[0][3] < 100:
# #                 #         I2.showHP(path[_][3], is_damaged=True)
# #                 #         pygame.display.flip()
# #                 #         pygame.time.wait(time_wait_4)
# #                 I2.showLeftBar(choose_map_result, path[_][2], path[_][3], path[_][4])
# #                 pygame.display.flip()
# #                 pygame.time.wait(time_wait_1)
# #             if path[-1][3] == 0:
# #                 I2.showNoti(3)
# #             elif path[-1][1] == 'Climb':
# #                 I2.showNoti(2)
# #                 M2.showPath(path[-1][0][0], path[-1][0][1])
# #             elif path[-1][1] != 'Climb':
# #                 I2.showNoti(4)
# #                 M2.showPath(path[-1][0][0], path[-1][0][1])
# #                 M2.showDie(path[_][0][0], path[_][0][1], M2.h)
# #             I2.showLeftBar(choose_map_result, path[-1][2], path[-1][3], path[-1][4])
# #             pygame.display.flip()
# #             isMoving = False
# #         elif len(path) == 0:
# #             isMoving = False
# #             I2.showNoti(4)
# #             I2.showLeftBar(choose_map_result)
# #             pygame.display.flip()
# #         else:
# #             for event in pygame.event.get():
# #                 if event.type == QUIT:
# #                     pygame.quit()
# #                     sys.exit()
# #                 if event.type == pygame.KEYDOWN:
# #                     if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
# #                         return
# # Kiệt
# def showAgentMove(choose_map_result, path, m, level):
#     # path: (pos-y, pos-x), action, point, HP, Healing Potion(s)
#     # maps: element, stench, breeze, whiff, glow, scream
#     # element in maps: 'W', 'P', 'G', '-'
#     I2 = Info(screen, level=level)
#     I2.showNoti(1)
#     isMoving = True
#     direction = 1  # 0: right, 1: up, 2: left, 3: down

#     time_wait_1 = 50
#     time_wait_2 = 100
#     time_wait_3 = 300
#     time_wait_4 = 1200

#     maps = [
#         [[
#             [cell.element, cell.is_stench, cell.is_breeze, cell.is_whiff, cell.is_glow, cell.is_scream]
#             for cell in row
#         ] for row in layer] for layer in m
#     ]

#     count_map = 1
#     M2 = Map(screen, maps[0])

#     while True:
#         if isMoving:
#             y_shoot, x_shoot = -1, -1
#             for i in range(len(path)):
#                 for event in pygame.event.get():
#                     if event.type == QUIT:
#                         pygame.quit()
#                         sys.exit()
#                     if event.type == pygame.KEYDOWN:
#                         if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
#                             return

#                 if i > 0:
#                     M2.showPath(path[i - 1][0][0], path[i - 1][0][1])

#                 y, x = path[i][0]
#                 action = path[i][1]
#                 point = path[i][2] if len(path[i]) > 2 else 0
#                 hp = path[i][3] if len(path[i]) > 3 else 0
#                 potion = path[i][4] if len(path[i]) > 4 else 0

#                 M2.showPath(y, x)
#                 M2.showAgent(y, x, M2.h)

#                 if action == 'Turn Left':
#                     pygame.display.flip()
#                     pygame.time.wait(time_wait_1)
#                     direction = M2.turnLeft(direction)
#                     M2.showAgent(y, x, M2.h)
#                     pygame.display.flip()
#                     pygame.time.wait(time_wait_2)

#                 elif action == 'Turn Right':
#                     pygame.display.flip()
#                     pygame.time.wait(time_wait_1)
#                     direction = M2.turnRight(direction)
#                     M2.showAgent(y, x, M2.h)
#                     pygame.display.flip()
#                     pygame.time.wait(time_wait_2)

#                 elif action == 'Grab Gold':
#                     M2.showGold(y, x, M2.h)
#                     pygame.display.flip()
#                     pygame.time.wait(time_wait_4)
#                     M2.updateMap(maps[count_map])
#                     count_map += 1

#                 elif action == 'Shoot':
#                     y_shoot, x_shoot = M2.agentShoot(path, i, direction)
#                     if M2.map_data[y][x][5]:
#                         M2.showScream(y, x, M2.h)
#                         pygame.display.flip()
#                         pygame.time.wait(time_wait_4)
#                     else:
#                         pygame.display.flip()
#                         pygame.time.wait(time_wait_3)
#                     M2.updateMap(maps[count_map])
#                     count_map += 1

#                 if i > 0 and action != 'Shoot' and path[i - 1][1] == 'Shoot':
#                     M2.showUnknown(y_shoot, x_shoot, M2.h)

#                 I2.showLeftBar(choose_map_result, point, hp, potion)
#                 pygame.display.flip()
#                 pygame.time.wait(time_wait_1)

#             # End notification
#             final_action = path[-1][1]
#             final_hp = path[-1][3] if len(path[-1]) > 3 else 0
#             final_point = path[-1][2] if len(path[-1]) > 2 else 0
#             final_potion = path[-1][4] if len(path[-1]) > 4 else 0

#             if final_hp == 0:
#                 I2.showNoti(3)
#             elif final_action == 'Climb':
#                 I2.showNoti(2)
#                 M2.showPath(path[-1][0][0], path[-1][0][1])
#             else:
#                 I2.showNoti(4)
#                 M2.showPath(path[-1][0][0], path[-1][0][1])
#                 M2.showDie(path[-1][0][0], path[-1][0][1], M2.h)

#             I2.showLeftBar(choose_map_result, final_point, final_hp, final_potion)
#             pygame.display.flip()
#             isMoving = False

#         elif len(path) == 0:
#             isMoving = False
#             I2.showNoti(4)
#             I2.showLeftBar(choose_map_result)
#             pygame.display.flip()

#         else:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
#                         return

# def showMenu():
#     showMenuBackground(screen)
#     choose_option = None
#     menuChoice = ['Play', 'Quit']
#     menu = Choice(screen, menuChoice, 'WumPus Game')
#     map_choose_option = None
#     mapChoice = ['Map 01', 'Map 02', 'Map 03', 'Map 04', 'Map 05']
#     mapMenu = Choice(screen, mapChoice, '')
#     mapChoice_2 = ['Map 06', 'Map 07', 'Map 08', 'Map 09', 'Map 10']
#     mapMenu_2 = Choice(screen, mapChoice_2, '')

#     while True:
#         is_up = False
#         is_down = False
#         is_left = False
#         is_right = False
#         is_enter = False

#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_DOWN and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
#                     is_down = True
#                 elif event.key == pygame.K_UP and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
#                     is_up = True
#                 elif event.key == pygame.K_LEFT and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
#                     is_left = True
#                 elif event.key == pygame.K_RIGHT and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
#                     is_right = True
#                 elif (event.key == pygame.K_RETURN or event.key == K_KP_ENTER) and is_down == False and is_up == False and is_left == False and is_right == False and is_enter == False:
#                     is_enter = True
        
#         if choose_option is None:
#             menu.display_option(is_up, is_down, is_left, is_right, is_enter)
#             choose_option = menu.get_option_result()
#         else:
#             if choose_option == 0:
#                 if map_choose_option is None:                    
#                     mapMenu.display_option(is_up, is_down, is_left, is_right, is_enter)
#                     map_choose_option = mapMenu.get_option_result()
#                 else:
#                     return map_choose_option
#                 if is_left:
#                     choose_option = mapMenu.get_back_to(None, 0)
#                 if is_right:
#                     choose_option = mapMenu.get_next_to(-1, 0)
#             if choose_option == 1:
#                 pygame.quit()
#                 sys.exit()
#             if choose_option == -1: # input page 2
#                 if map_choose_option is None:                    
#                     mapMenu_2.display_option(is_up, is_down, is_left, is_right, is_enter, can_next=False)
#                     map_choose_option = mapMenu_2.get_option_result()
#                 else:
#                     return map_choose_option + 5
#                 if is_left:
#                     choose_option = mapMenu_2.get_back_to(0, -1)
#         pygame.display.update()

# #(base) D:\HCMUS\Co so AI\CSC14003 - Introduction to AI\Proj2\Project-2-Logical-Agent\Source>
# #day la main ui, chua ket noi voi main toan chuong trinh
# #[element, stench, breeze, whiff, glow, scream]
# # [ ['-'] True True False False ] [ ['W', 'P', 'G'] False False False False ] [ ['-'] True True False False ] [ ['-'] False False False False ]
# # [ ['-'] False False False False ] [ ['G'] True True False False ] [ ['P'] False False False False ] [ ['-'] False True False False ]
# # [ ['-'] False False False False ] [ ['-'] False False False False ] [ ['-'] False True False False ] [ ['-'] False True False False ]
# # [ ['-'] False False False False ] [ ['-'] False False False False ] [ ['-'] False True False False ] [ ['P'] False False False False ]

# Bảo thêm
import pygame, sys
from pygame.locals import *
from ui.constants import *
from ui.choice import *
from ui.image import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('WumPus Game')

def inputForm():
    pygame.font.init()
    font = pygame.font.SysFont(FONT_TYPE, FONT_LARGE, bold=True)
    clock = pygame.time.Clock()


    input_boxes = [
        {"label": "Enter map size (4-20):", "value": "", "type": "int"},
        {"label": "Enter pit probability (0.0 - 1.0):", "value": "", "type": "float"},
        {"label": "Enter number of Wumpus (1-10):", "value": "", "type": "int"},
    ]
    active_box = 0

    while True:
        showMenuBackground(screen)

        for i, box in enumerate(input_boxes):
            label_color = DARK_BLUE_COLOR if i == active_box else LIGHT_BLUE_COLOR
            label_surface = font.render(box["label"], True, label_color)
            value_surface = font.render(box["value"], True, LIGHT_BLUE_COLOR)

            y = 150 + i * 100
            screen.blit(label_surface, (100, y))
            screen.blit(value_surface, (100 + label_surface.get_width() + 20, y))  # value bên phải label

        instructions = font.render("Enter: Next  |  Backspace: Delete  |  Esc: Exit", True, LIGHT_BLUE_COLOR)
        screen.blit(instructions, (100, 500))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["value"] = input_boxes[active_box]["value"][:-1]

                elif event.key == pygame.K_RETURN:
                    if active_box < len(input_boxes) - 1:
                        active_box += 1
                    else:
                        try:
                            size = int(input_boxes[0]["value"])
                            prob = float(input_boxes[1]["value"])
                            wumpus = int(input_boxes[2]["value"])
                            if 4 <= size <= 20 and 0.0 <= prob <= 1.0 and 1 <= wumpus <= 10:
                                return size, prob, wumpus
                        except:
                            pass  # Ignore invalid input

                else:
                    if event.unicode.isprintable():
                        input_boxes[active_box]["value"] += event.unicode



def showMenu():
    showMenuBackground(screen)
    menuChoice = ['Play', 'Quit']
    menu = Choice(screen, menuChoice, 'WumPus Game')

    while True:
        is_up = is_down = is_left = is_right = is_enter = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    is_down = True
                elif event.key == pygame.K_UP:
                    is_up = True
                elif event.key == pygame.K_LEFT:
                    is_left = True
                elif event.key == pygame.K_RIGHT:
                    is_right = True
                elif event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                    is_enter = True

        menu.display_option(is_up, is_down, is_left, is_right, is_enter)
        choose_option = menu.get_option_result()

        if choose_option == 0:  # Play
            return inputForm()  # Nhập thông tin bản đồ
        elif choose_option == 1:  # Quit
            pygame.quit()
            sys.exit()

        pygame.display.update()

def showWumpusWorld(map_data):
    M1 = Map(screen, map_data)
    showGameBackground(screen, level=1)
    M1.showUnknownBoard()
    I1 = Info(screen, level=1)
    I1.showLeftBar(1, point=10000, HP=100, H_Ps=0)
    I1.showNoti(0)
    pygame.display.update()
    pygame.time.wait(2000)

def showAgentMove(_, path, maps_data, __):
    I2 = Info(screen, level=1)
    I2.showNoti(1)
    isMoving = True
    direction = 1

    time_wait_1 = 50
    time_wait_2 = 100
    time_wait_3 = 300
    time_wait_4 = 1200

    # Use the maps_data directly since it's already a list of grids
    maps = []
    for env_grid in maps_data:
        map_layer = []
        for row in env_grid:
            map_row = []
            for cell in row:
                # Convert cell object to the expected format
                map_row.append([
                    'W' if cell.wumpus else 'P' if cell.pit else 'G' if cell.gold else '-',
                    cell.stench,
                    cell.breeze,
                    cell.pit,
                    cell.glitter,
                    False  # scream - you may need to adjust this based on your environment
                ])
            map_layer.append(map_row)
        maps.append(map_layer)

    count_map = 0 if len(maps) > 0 else 1
    M2 = Map(screen, maps[0] if maps else [])

    while True:
        if isMoving:
            y_shoot, x_shoot = -1, -1
            for i in range(len(path)):
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == K_KP_ENTER):
                        return

                if i > 0:
                    M2.showPath(path[i - 1][0][0], path[i - 1][0][1])

                y, x = path[i][0]
                action = path[i][1]
                point = path[i][2] if len(path[i]) > 2 else 0
                hp = path[i][3] if len(path[i]) > 3 else 0
                potion = path[i][4] if len(path[i]) > 4 else 0

                M2.showPath(y, x)
                M2.showAgent(y, x, M2.h)

                if action == 'Turn Left':
                    pygame.display.flip()
                    pygame.time.wait(time_wait_1)
                    direction = M2.turnLeft(direction)
                    M2.showAgent(y, x, M2.h)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_2)

                elif action == 'Turn Right':
                    pygame.display.flip()
                    pygame.time.wait(time_wait_1)
                    direction = M2.turnRight(direction)
                    M2.showAgent(y, x, M2.h)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_2)

                elif action == 'Grab Gold':
                    M2.showGold(y, x, M2.h)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_4)
                    if count_map + 1 < len(maps):
                        M2.updateMap(maps[count_map + 1])
                        count_map += 1

                elif action == 'Shoot':
                    y_shoot, x_shoot = M2.agentShoot(path, i, direction)
                    if M2.map_data[y][x][5]:
                        M2.showScream(y, x, M2.h)
                        pygame.display.flip()
                        pygame.time.wait(time_wait_4)
                    else:
                        pygame.display.flip()
                        pygame.time.wait(time_wait_3)
                    if count_map + 1 < len(maps):
                        M2.updateMap(maps[count_map + 1])
                        count_map += 1

                if i > 0 and action != 'Shoot' and path[i - 1][1] == 'Shoot':
                    M2.showUnknown(y_shoot, x_shoot, M2.h)

                I2.showLeftBar(1, point, hp, potion)
                pygame.display.flip()
                pygame.time.wait(time_wait_1)

            final_action = path[-1][1]
            final_hp = path[-1][3] if len(path[-1]) > 3 else 0
            final_point = path[-1][2] if len(path[-1]) > 2 else 0
            final_potion = path[-1][4] if len(path[-1]) > 4 else 0

            if final_hp == 0:
                I2.showNoti(3)
            elif final_action == 'Climb':
                I2.showNoti(2)
                M2.showPath(path[-1][0][0], path[-1][0][1])
            else:
                I2.showNoti(4)
                M2.showPath(path[-1][0][0], path[-1][0][1])
                M2.showDie(path[-1][0][0], path[-1][0][1], M2.h)

            I2.showLeftBar(1, final_point, final_hp, final_potion)
            pygame.display.flip()
            isMoving = False

        elif len(path) == 0:
            isMoving = False
            I2.showNoti(4)
            I2.showLeftBar(1)
            pygame.display.flip()

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == K_KP_ENTER):
                    return