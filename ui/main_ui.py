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
        {"label": "Enter map size:", "value": "", "type": "int"},
        {"label": "Enter pit probability:", "value": "", "type": "float"},
        {"label": "Enter number of Wumpus:", "value": "", "type": "int"},
    ]
    active_box = 0

    while True:
        showMenuBackground(screen)

        for i, box in enumerate(input_boxes):
            label_color = DARK_RED_COLOR if i == active_box else WHITE_COLOR
            label_surface = font.render(box["label"], True, label_color)
            value_surface = font.render(box["value"], True, WHITE_COLOR)

            y = 150 + i * 100
            screen.blit(label_surface, (100, y))
            screen.blit(value_surface, (100 + label_surface.get_width() + 20, y))

        small_font = pygame.font.SysFont(FONT_TYPE, FONT_MEDIUM)
        instructions = small_font.render("Up/Down: Navigate  |  Enter: Confirm  |  Esc: Back to Menu", True, WHITE_COLOR)
        screen.blit(instructions, (100, 500))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None  # Return None to indicate going back to menu

                elif event.key == pygame.K_UP:
                    active_box = (active_box - 1) % len(input_boxes)

                elif event.key == pygame.K_DOWN:
                    active_box = (active_box + 1) % len(input_boxes)

                elif event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["value"] = input_boxes[active_box]["value"][:-1]

                elif event.key == pygame.K_RETURN:
                    # Check if all fields are filled and valid
                    all_filled = all(box["value"].strip() for box in input_boxes)
                    if all_filled:
                        try:
                            size = int(input_boxes[0]["value"])
                            prob = float(input_boxes[1]["value"])
                            wumpus = int(input_boxes[2]["value"])
                            
                            return size, prob, wumpus
                        except:
                            pass

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
            result = inputForm()
            if result is not None:  # Only return if we got valid input
                return result
            # If result is None, continue the menu loop
        elif choose_option == 1:  # Quit
            pygame.quit()
            sys.exit()

        pygame.display.update()

def calculateScore(action, current_score=0, has_gold=False, died=False):
    """
    Calculate score based on Wumpus World scoring system:
    - Grab gold: +10
    - Move forward: -1
    - Turn left/right: -1
    - Shoot: -10
    - Die (fall in pit or eaten by wumpus): -1000
    - Climb out (with gold): +1000
    - Climb out (without gold): 0
    """
    if died:
        return -1000
    
    if action == 'Move Forward':
        return current_score - 1
    elif action in ['Turn Left', 'Turn Right']:
        return current_score - 1
    elif action == 'Grab Gold':
        return current_score + 10
    elif action == 'Shoot':
        return current_score - 10
    elif action == 'Climb':
        if has_gold:
            return current_score + 1000
        else:
            return current_score + 0
    else:
        return current_score

def showWumpusWorld(map_data):
    M1 = Map(screen, map_data)
    showGameBackground(screen, level=1)
    M1.showUnknownBoard()
    I1 = Info(screen, level=1)
    # Calculate map size from map_data
    map_size = len(map_data) if map_data else 4
    # Start with score = 0
    I1.showLeftBar(map_size, score=0)
    I1.showNoti(0)
    pygame.display.update()
    pygame.time.wait(2000)

def showAgentMove(_, path, maps_data, __):
    I2 = Info(screen, level=1)
    I2.showNoti(1)
    isMoving = True
    direction = 1
    current_score = 0  # Start with 0 score
    has_gold = False

    time_wait_1 = 50
    time_wait_2 = 100
    time_wait_3 = 300
    time_wait_4 = 1200

    # Convert maps_data to expected format
    maps = []
    for env_grid in maps_data:
        map_layer = []
        for row in env_grid:
            map_row = []
            for cell in row:
                # Create proper cell data with the right format
                cell_data = [
                    ('W' if getattr(cell, 'wumpus', False) else '') + 
                    ('P' if getattr(cell, 'pit', False) else '') + 
                    ('G' if getattr(cell, 'gold', False) else ''),
                    getattr(cell, 'stench', False),
                    getattr(cell, 'breeze', False),
                    False,  # whiff (not used in basic Wumpus)
                    getattr(cell, 'glitter', False),
                    False  # scream
                ]
                # If cell is empty, mark it as '-'
                if cell_data[0] == '':
                    cell_data[0] = '-'
                map_row.append(cell_data)
            map_layer.append(map_row)
        maps.append(map_layer)

    count_map = 0 if len(maps) > 0 else 1
    M2 = Map(screen, maps[0] if maps else [])
    
    # Calculate map size
    map_size = len(maps[0]) if maps and len(maps[0]) > 0 else 4
    
    # Track killed wumpus positions to ensure they remain invisible
    killed_wumpus_positions = set()

    while True:
        if isMoving:
            x_shoot, y_shoot = -1, -1
            for i in range(len(path)):
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == K_KP_ENTER):
                        return

                if i > 0:
                    # Get coordinates consistently as (x,y)
                    prev_x, prev_y = path[i - 1][0]
                    M2.showPath(prev_x, prev_y)

                x, y = path[i][0]  # x is column, y is row
                action = path[i][1]
                
                # Calculate score based on action
                if action == 'Grab Gold':
                    has_gold = True
                
                # Check if agent died
                died = False
                if len(path[i]) > 3:
                    died = path[i][3] == 0
                
                current_score = calculateScore(action, current_score, has_gold, died)

                # Show the path and agent at current position using x,y
                M2.showPath(x, y)
                M2.showAgent(y, x, M2.h)  # Note: showAgent uses y,x internally

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

                # Bảo thêm
                elif action == 'Shoot' or action == 'SHOOT_HIT' or action == 'SHOOT_MISS':
                    x_shoot, y_shoot = M2.agentShoot(path, i, direction)
                    pygame.display.flip()
                    pygame.time.wait(time_wait_3)
                    
                    # If it was a successful shot (SHOOT_HIT)
                    if action == 'SHOOT_HIT' or (len(maps) > count_map and y < len(maps[count_map]) and 
                             x < len(maps[count_map][y]) and maps[count_map][y][x][5]):
                        # Show scream animation
                        M2.showScream(y_shoot, x_shoot, M2.h)
                        pygame.display.flip()
                        pygame.time.wait(time_wait_4)
                        
                        # Mark this wumpus as killed
                        killed_wumpus_positions.add((x_shoot, y_shoot))
                        
                        # Update map to show wumpus is gone
                        if count_map + 1 < len(maps):
                            # Ensure wumpus is removed from all future maps
                            for future_map_idx in range(count_map + 1, len(maps)):
                                if y_shoot < len(maps[future_map_idx]) and x_shoot < len(maps[future_map_idx][y_shoot]):
                                    # Remove wumpus from cell content (first element)
                                    cell_content = maps[future_map_idx][y_shoot][x_shoot][0]
                                    maps[future_map_idx][y_shoot][x_shoot][0] = cell_content.replace('W', '')
                                    if maps[future_map_idx][y_shoot][x_shoot][0] == '':
                                        maps[future_map_idx][y_shoot][x_shoot][0] = '-'
                                    
                                    # Remove stench from neighboring cells
                                    for nx, ny in [(x_shoot+1, y_shoot), (x_shoot-1, y_shoot), 
                                                  (x_shoot, y_shoot+1), (x_shoot, y_shoot-1)]:
                                        if (0 <= nx < map_size and 0 <= ny < map_size and
                                            ny < len(maps[future_map_idx]) and nx < len(maps[future_map_idx][ny])):
                                            maps[future_map_idx][ny][nx][1] = False  # Set stench to False
                            
                            # Update the current display map
                            M2.updateMap(maps[count_map + 1])
                            count_map += 1
                    
                    # Ensure no wumpus is shown at killed positions
                    for kx, ky in killed_wumpus_positions:
                        if 0 <= kx < map_size and 0 <= ky < map_size:
                            M2.showEmpty(ky, kx, M2.h)

                # Show only score
                I2.showLeftBar(map_size, score=current_score)
                pygame.display.flip()
                pygame.time.wait(time_wait_1)

            # Final score calculation
            final_action = path[-1][1]
            final_died = len(path[-1]) > 3 and path[-1][3] == 0
            final_score = calculateScore(final_action, current_score, has_gold, final_died)

            if final_died:
                I2.showNoti(3)  # Death notification
            elif final_action == 'Climb':
                I2.showNoti(2)  # Success notification
                final_x, final_y = path[-1][0]
                M2.showPath(final_x, final_y)
            else:
                I2.showNoti(4)  # Other ending
                final_x, final_y = path[-1][0]
                M2.showPath(final_x, final_y)
                M2.showDie(final_y, final_x, M2.h)

            I2.showLeftBar(map_size, score=final_score)
            pygame.display.flip()
            isMoving = False

        elif len(path) == 0:
            isMoving = False
            I2.showNoti(4)
            I2.showLeftBar(4, score=0)  # Default to 4x4 if no path
            pygame.display.flip()

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == K_KP_ENTER):
                    return