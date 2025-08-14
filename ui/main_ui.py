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
    font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM)    
    clock = pygame.time.Clock()

    mode_labels = ["Normal", "Advanced"]
    agent_labels = ["Single Agent", "Double Agent"]

    input_boxes = [
        {"label": "Enter map size (default: 8):", "value": "", "type": "int", "default": "8"},
        {"label": "Enter pit probability (default: 0.2):", "value": "", "type": "float", "default": "0.2"},
        {"label": "Enter number of Wumpus (default: 2):", "value": "", "type": "int", "default": "2"},
    ]

    # State
    game_mode = 0
    agent_mode = 0
    active_box = 0  # 0: mode, 1: agent, 2+: input_boxes

    total_lines = 2 + len(input_boxes)  # 2 lựa chọn + 3 input

    while True:
        showMenuBackground(screen)

        y_start = 120
        y_step = 70

        # Draw game mode line
        label_color = DARK_RED_COLOR if active_box == 0 else WHITE_COLOR
        label_surface = font.render("Game Mode:", True, label_color)
        screen.blit(label_surface, (100, y_start))
        # Draw buttons
        for i, mode in enumerate(mode_labels):
            btn_color = DARK_RED_COLOR if game_mode == i else WHITE_COLOR
            btn_rect = pygame.Rect(410 + i*260, y_start, 240, 50)
            pygame.draw.rect(screen, btn_color, btn_rect, 2)
            btn_text = font.render(mode, True, btn_color)
            text_rect = btn_text.get_rect(center=btn_rect.center)
            screen.blit(btn_text, text_rect)

        label_color = DARK_RED_COLOR if active_box == 1 else WHITE_COLOR
        label_surface = font.render("Agent Mode:", True, label_color)
        screen.blit(label_surface, (100, y_start + y_step))
        for i, agent in enumerate(agent_labels):
            btn_color = DARK_RED_COLOR if agent_mode == i else WHITE_COLOR
            btn_rect = pygame.Rect(410 + i*360, y_start + y_step, 350, 50)
            pygame.draw.rect(screen, btn_color, btn_rect, 2)
            btn_text = font.render(agent, True, btn_color)
            text_rect = btn_text.get_rect(center=btn_rect.center)
            screen.blit(btn_text, text_rect)

        # Draw input boxes
        for i, box in enumerate(input_boxes):
            idx = i + 2
            label_color = DARK_RED_COLOR if active_box == idx else WHITE_COLOR
            label_surface = font.render(box["label"], True, label_color)
            display_value = box["value"] if box["value"] else f"[{box['default']}]"
            value_color = label_color if box["value"] else (128, 128, 128)
            value_surface = font.render(display_value, True, value_color)
            y = y_start + y_step * (idx)
            screen.blit(label_surface, (100, y))
            screen.blit(value_surface, (100 + label_surface.get_width() + 20, y))

        # Instructions
        small_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)
        instructions = small_font.render(
            "Up/down: Move | Left/right: Change | Enter: Confirm | Esc: Back", True, WHITE_COLOR
        )
        screen.blit(instructions, (100, 550))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

                elif event.key == pygame.K_UP:
                    active_box = (active_box - 1) % total_lines

                elif event.key == pygame.K_DOWN:
                    active_box = (active_box + 1) % total_lines

                elif event.key == pygame.K_LEFT:
                    if active_box == 0:
                        game_mode = (game_mode - 1) % len(mode_labels)
                    elif active_box == 1:
                        agent_mode = (agent_mode - 1) % len(agent_labels)

                elif event.key == pygame.K_RIGHT:
                    if active_box == 0:
                        game_mode = (game_mode + 1) % len(mode_labels)
                    elif active_box == 1:
                        agent_mode = (agent_mode + 1) % len(agent_labels)

                elif event.key == pygame.K_BACKSPACE:
                    if active_box >= 2:
                        box = input_boxes[active_box - 2]
                        box["value"] = box["value"][:-1]

                elif event.key == pygame.K_RETURN:
                    if active_box < 2:
                        # Không làm gì khi Enter ở dòng chọn chế độ
                        continue
                    try:
                        size_str = input_boxes[0]["value"] if input_boxes[0]["value"].strip() else input_boxes[0]["default"]
                        prob_str = input_boxes[1]["value"] if input_boxes[1]["value"].strip() else input_boxes[1]["default"]
                        wumpus_str = input_boxes[2]["value"] if input_boxes[2]["value"].strip() else input_boxes[2]["default"]

                        size = int(size_str)
                        prob = float(prob_str)
                        wumpus = int(wumpus_str)

                        if size < 4 or size > 20:
                            continue
                        if prob < 0.0 or prob > 1.0:
                            continue
                        if wumpus < 1 or wumpus > size * size // 4:
                            continue

                        print(f"[INPUT] Using values: Size={size}, Pit Probability={prob}, Wumpus={wumpus}, Mode={game_mode}, Agent={agent_mode}")
                        return size, prob, wumpus, game_mode, agent_mode

                    except ValueError:
                        continue

                else:
                    if active_box >= 2 and event.unicode.isprintable():
                        box = input_boxes[active_box - 2]
                        box["value"] += event.unicode

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
        
        elif choose_option == 1:  # Quit
            pygame.quit()
            sys.exit()

        pygame.display.update()

def showWumpusWorld(map_data):
    M1 = Map(screen, map_data)
    showGameBackground(screen)
    M1.showUnknownBoard()
    M1.showPath(0, 0)
    I1 = Info(screen, level=1)
    map_size = len(map_data) if map_data else 4
    I1.showLeftBar(map_size, score=0)
    pygame.display.update()

def showAgentMove(_, path, maps_data, __, list_env, agent_mode, agent_index=0):
    I2 = Info(screen, level=1)
    current_direction = "EAST"
    direction = 1
    current_score = 0
    has_gold = False
    current_step = 0
    auto_play = False
    auto_play_timer = 0
    selected_button = 0
    current_action = "START"
    index_env = 0
    count_action = 0
    
    # Lưu trữ lịch sử vị trí của agent
    visited_positions = set([(0, 0)])  # Bắt đầu từ vị trí (0,0)
    agent_died = False  # Thêm biến để theo dõi trạng thái chết của agent


    # Button setup
    button_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)
    button_width = 120
    button_height = 40
    button_margin = 10
    
    base_x = 870
    base_y = 280
    
    auto_button_rect = pygame.Rect(base_x, base_y, button_width, button_height)
    step_button_rect = pygame.Rect(base_x, base_y + button_height + button_margin, button_width, button_height)
    reset_button_rect = pygame.Rect(base_x, base_y + (button_height + button_margin) * 2, button_width, button_height)
    exit_button_rect = pygame.Rect(base_x, base_y + (button_height + button_margin) * 3, button_width, button_height)
    
    # Convert maps_data to expected format
    maps = []
    for env_grid in maps_data:
        map_layer = []
        for row in env_grid:
            map_row = []
            for cell in row:
                has_wumpus = getattr(cell, 'wumpus', False)
                has_pit = getattr(cell, 'pit', False) 
                has_gold = getattr(cell, 'gold', False)
                
                element = ''
                if has_wumpus:
                    element += 'W'
                if has_pit:
                    element += 'P'
                if has_gold:
                    element += 'G'
                if element == '':
                    element = '-'
                
                stench = getattr(cell, 'stench', False)
                breeze = getattr(cell, 'breeze', False)
                
                cell_data = [
                    element,
                    stench,
                    breeze,
                    False,
                    getattr(cell, 'glitter', False),
                    False
                ]
                map_row.append(cell_data)
            map_layer.append(map_row)
        maps.append(map_layer)

    # Convert list_env to expected format (nếu list_env không rỗng)
    env_maps = []
    if list_env:
        for env_grid in list_env:
            env_layer = []
            for row in env_grid:
                env_row = []
                for cell in row:
                    has_wumpus = getattr(cell, 'wumpus', False)
                    has_pit = getattr(cell, 'pit', False) 
                    has_gold = getattr(cell, 'gold', False)
                    
                    element = ''
                    if has_wumpus:
                        element += 'W'
                    if has_pit:
                        element += 'P'
                    if has_gold:
                        element += 'G'
                    if element == '':
                        element = '-'
                    
                    stench = getattr(cell, 'stench', False)
                    breeze = getattr(cell, 'breeze', False)
                    
                    cell_data = [
                        element,
                        stench,
                        breeze,
                        False,
                        getattr(cell, 'glitter', False),
                        False
                    ]
                    env_row.append(cell_data)
                env_layer.append(env_row)
            env_maps.append(env_layer)

    # Store original maps for reset functionality
    original_maps = []
    for map_layer in maps:
        original_map = []
        for row in map_layer:
            original_row = []
            for cell in row:
                original_cell = [cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]]
                original_row.append(original_cell)
            original_map.append(original_row)
        original_maps.append(original_map)
        
    count_map = 0 if len(maps) > 0 else 1
    M2 = Map(screen, maps[0] if maps else [])
    map_size = len(maps[0]) if maps and len(maps[0]) > 0 else 4
    killed_wumpus_positions = set()

    # Initialize display
    showGameBackground(screen)
    M2.showUnknownBoard()
    M2.showPath(0, 0)
    M2.showAgent(0, 0, M2.h)
    I2.showLeftBar(map_size, score=0)

    def draw_action_info(agent_index):
        """Hiển thị thông tin action hiện tại và direction"""
        action_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)
        
        action_x = 860
        action_y = 150
        
        if agent_mode == 1:
            agent_type = "A*" if agent_index == 0 else "DFS"
            agent_text = f"Agent: {agent_type}"
            agent_surface = action_font.render(agent_text, True, DARK_RED_COLOR)
            screen.blit(agent_surface, (40, WINDOW_HEIGHT - 60))
        
        # Hiển thị current action - màu đỏ
        action_text = f"Action: {current_action}"
        action_surface = action_font.render(action_text, True, DARK_RED_COLOR)
        screen.blit(action_surface, (action_x, action_y))
        
        # Hiển thị current direction - màu đỏ
        direction_text = f"Facing: {current_direction}"
        direction_surface = action_font.render(direction_text, True, DARK_RED_COLOR)
        screen.blit(direction_surface, (action_x, action_y + 30))
        
        # Hiển thị thông tin về gold - màu đỏ
        gold_status = "YES" if has_gold else "NO"
        gold_text = f"Has Gold: {gold_status}"
        gold_surface = action_font.render(gold_text, True, DARK_RED_COLOR)
        screen.blit(gold_surface, (action_x, action_y + 60))
        
        # Show current step info above buttons
        step_info = button_font.render(f"Step: {current_step}/{len(path)}", True, DARK_RED_COLOR)
        screen.blit(step_info, (action_x, action_y + 90))
        
    def draw_buttons():
        # Auto Play button
        auto_color = WHITE_COLOR if selected_button == 0 else DARK_RED_COLOR
        pygame.draw.rect(screen, auto_color, auto_button_rect, 2)
        auto_text = button_font.render("Play", True, auto_color)
        text_rect = auto_text.get_rect(center=auto_button_rect.center)
        screen.blit(auto_text, text_rect)

        # Step button
        step_color = WHITE_COLOR if selected_button == 1 else DARK_RED_COLOR
        pygame.draw.rect(screen, step_color, step_button_rect, 2)
        step_text = button_font.render("Step", True, step_color)
        text_rect = step_text.get_rect(center=step_button_rect.center)
        screen.blit(step_text, text_rect)

        # Reset button
        reset_color = WHITE_COLOR if selected_button == 2 else DARK_RED_COLOR
        pygame.draw.rect(screen, reset_color, reset_button_rect, 2)
        reset_text = button_font.render("Reset", True, reset_color)
        text_rect = reset_text.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text, text_rect)

        # Exit button
        exit_color = WHITE_COLOR if selected_button == 3 else DARK_RED_COLOR
        pygame.draw.rect(screen, exit_color, exit_button_rect, 2)
        exit_text = button_font.render("Exit", True, exit_color)
        text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, text_rect)

    def execute_step():
        nonlocal current_step, direction, current_score, count_map, killed_wumpus_positions, current_direction, current_action, has_gold, count_action, index_env, agent_died

        if current_step >= len(path):
            return False
            
        i = current_step
        
        # Clear agent from previous position
        if i > 0:
            prev_x, prev_y = path[i - 1][0]
            M2.showPath(prev_x, prev_y)
        else:
            M2.showPath(0, 0)

        if list_env and index_env < len(env_maps):
            print(f"[ENV UPDATE] Loading new environment map at index {index_env}")
    
            # Store previous Wumpus positions before updating
            previous_wumpus_positions = set()
            for row_idx, row in enumerate(maps[count_map]):
                for col_idx, cell in enumerate(row):
                    if isinstance(cell, list) and 'W' in cell[0]:
                        previous_wumpus_positions.add((col_idx, row_idx))
                    elif hasattr(cell, 'wumpus') and cell.wumpus:
                        previous_wumpus_positions.add((col_idx, row_idx))
            
            # Update map with new environment
            maps[count_map] = env_maps[index_env]
            index_env += 1
            
            # Update killed_wumpus_positions to reflect new reality
            updated_killed_positions = set()
            for kx, ky in killed_wumpus_positions:
                # If this was a position where a Wumpus was killed,
                # keep it marked as killed even if Wumpus moved
                if (kx, ky) in previous_wumpus_positions:
                    updated_killed_positions.add((kx, ky))
            
            killed_wumpus_positions = updated_killed_positions
            
            # Update the map symbols for Wumpus
            for row in range(map_size):
                for col in range(map_size):
                    cell = maps[count_map][row][col]
                    # If this position previously had a killed Wumpus, 
                    # make sure it's still marked as empty
                    if (col, row) in killed_wumpus_positions:
                        if isinstance(cell, list):
                            cell[0] = cell[0].replace('W', '')
                            if cell[0] == '':
                                cell[0] = '-'
                        elif hasattr(cell, 'wumpus'):
                            cell.wumpus = False
                    # Otherwise update as normal
                    elif getattr(cell, 'wumpus', False) or (isinstance(cell, list) and 'W' in cell[0]):
                        if isinstance(cell, list):
                            if 'W' not in cell[0]:
                                cell[0] = cell[0].replace('-', '') + 'W'
                    else:
                        if isinstance(cell, list):
                            cell[0] = cell[0].replace('W', '')
                            if cell[0] == '':
                                cell[0] = '-'
        x, y = path[i][0]
        action = path[i][1]
        current_action = action
        
        # Cập nhật tập hợp các vị trí đã đi qua
        visited_positions.add((x, y))
        
        if len(path[i]) > 2:
            current_score = path[i][2]

        if action == 'Grab Gold' or action == 'GRAB':
            has_gold = True
        
        died = False
        if len(path[i]) > 3:
            died = path[i][3] == 0
            agent_died = died 

        if not agent_died and not (action in ['Climb', 'CLIMB'] and x == 0 and y == 0):
            M2.showPath(x, y)
            M2.showAgent(y, x, M2.h)

        if action == 'Turn Left' or action == 'TURN_LEFT':
            count_action += 1
            current_action = "TURN LEFT"
            direction = M2.turnLeft(direction)
            dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
            idx = dirs.index(current_direction)
            current_direction = dirs[(idx + 1) % 4]
            # M2.showAgent(y, x, M2.h)
            if not agent_died and not (action in ['Climb', 'CLIMB'] and x == 0 and y == 0):
                M2.showAgent(y, x, M2.h)

        elif action == 'Turn Right' or action == 'TURN_RIGHT':
            count_action += 1
            current_action = "TURN RIGHT"
            direction = M2.turnRight(direction)
            dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
            idx = dirs.index(current_direction)
            current_direction = dirs[(idx + 1) % 4]
            # M2.showAgent(y, x, M2.h)
            if not agent_died and not (action in ['Climb', 'CLIMB'] and x == 0 and y == 0):
                M2.showAgent(y, x, M2.h)

        elif action == 'Move' or action == 'MOVE':
            count_action += 1
            current_action = "MOVE FORWARD"

        elif action == 'Grab Gold' or action == 'GRAB':
            count_action += 1
            current_action = "GRAB GOLD"
            has_gold = True
            M2.showGold(y, x, M2.h)

        elif action == 'Climb' or action == 'CLIMB':
            count_action += 1
            current_action = "CLIMB OUT"
            if x == 0 and y == 0:
                M2.showPath(y, x) 
                agent_died = True
                # Có thể thêm hiệu ứng climb out ở đây nếu cần
                pygame.display.flip()
                pygame.time.wait(500)

        elif action == 'Shoot' or action == 'SHOOT_HIT' or action == 'SHOOT_MISS':
            count_action += 1
            if action == 'SHOOT_HIT':
                current_action = "SHOOT (HIT)"
            elif action == 'SHOOT_MISS':
                current_action = "SHOOT (MISS)"
            else:
                current_action = "SHOOT ARROW"
            
            # Calculate shoot direction
            dx, dy = {
                "NORTH": (0, 1),
                "EAST": (1, 0),
                "SOUTH": (0, -1),
                "WEST": (-1, 0)
            }.get(current_direction, (1, 0))
            
            # Track visited cells up to current step
            arrow_x, arrow_y = x, y
            hit_target = False
            arrow_path = []
            # Đối với SHOOT_HIT, trước tiên tìm vị trí Wumpus đầu tiên trên đường đi
            target_x, target_y = None, None
            if action == 'SHOOT_HIT':
                temp_x, temp_y = x, y
                while True:
                    temp_x += dx
                    temp_y += dy
                    
                    if temp_x < 0 or temp_x >= map_size or temp_y < 0 or temp_y >= map_size:
                        break
                        
                    arrow_path.append((temp_x, temp_y))
                    # Đây sẽ là vị trí Wumpus đầu tiên trên đường đi của mũi tên
                    target_x, target_y = temp_x, temp_y
                    break
            
            # Tiếp tục xử lý animation bắn tên
            while True:
                arrow_x += dx
                arrow_y += dy
                
                if arrow_x < 0 or arrow_x >= map_size or arrow_y < 0 or arrow_y >= map_size:
                    break
                
                if action == 'SHOOT_HIT' and arrow_x == target_x and arrow_y == target_y:
                    hit_target = True
                    M2.showShoot(arrow_y, arrow_x, M2.h)
                    pygame.display.flip()
                    pygame.time.wait(200)
                    break
                    
                arrow_path.append((arrow_x, arrow_y))
                
                M2.showShoot(arrow_y, arrow_x, M2.h)
                pygame.display.flip()
                pygame.time.wait(200)
                
                if (arrow_y < len(maps[count_map]) and 
                    arrow_x < len(maps[count_map][arrow_y])):
                    
                    cell_data = maps[count_map][arrow_y][arrow_x]
                    if isinstance(cell_data, list):
                        has_wumpus = 'W' in cell_data[0]
                    else:
                        has_wumpus = getattr(cell_data, 'wumpus', False)
                    
                    if has_wumpus:
                        hit_target = True
                        break
                
                if (arrow_x, arrow_y) in visited_positions:
                    M2.showPath(arrow_x, arrow_y)
                else:
                    if (arrow_y < len(maps[count_map]) and 
                        arrow_x < len(maps[count_map][arrow_y])):
                        M2.showUnknownWithOverlay(arrow_y, arrow_x, M2.h, maps[count_map][arrow_y][arrow_x])
                    else:
                        M2.showUnknown(arrow_y, arrow_x, M2.h)
            
            # Handle hit result
            if hit_target and action == 'SHOOT_HIT':
                M2.showScream(arrow_y, arrow_x, M2.h)
                pygame.display.flip()
                pygame.time.wait(500)
                
                killed_wumpus_positions.add((arrow_x, arrow_y))
                
                # Remove Wumpus from maps
                for map_idx in range(count_map, len(maps)):
                    if (0 <= arrow_y < len(maps[map_idx]) and 
                        0 <= arrow_x < len(maps[map_idx][arrow_y])):
                        
                        if isinstance(maps[map_idx][arrow_y][arrow_x], list):
                            cell_content = maps[map_idx][arrow_y][arrow_x][0]
                            maps[map_idx][arrow_y][arrow_x][0] = cell_content.replace('W', '')
                            if maps[map_idx][arrow_y][arrow_x][0] == '':
                                maps[map_idx][arrow_y][arrow_x][0] = '-'
                        else:
                            maps[map_idx][arrow_y][arrow_x].wumpus = False
                        
                        # Remove stench from adjacent cells
                        for dx2, dy2 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            adj_x, adj_y = arrow_x + dx2, arrow_y + dy2
                            if (0 <= adj_x < map_size and 0 <= adj_y < map_size and
                                adj_y < len(maps[map_idx]) and adj_x < len(maps[map_idx][adj_y])):
                                
                                other_wumpus_nearby = False
                                for dx3, dy3 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                                    check_x, check_y = adj_x + dx3, adj_y + dy3
                                    if (0 <= check_x < map_size and 0 <= check_y < map_size and
                                        check_y < len(maps[map_idx]) and check_x < len(maps[map_idx][check_y]) and
                                        (check_x, check_y) not in killed_wumpus_positions):
                                        
                                        if isinstance(maps[map_idx][check_y][check_x], list):
                                            if 'W' in maps[map_idx][check_y][check_x][0]:
                                                other_wumpus_nearby = True
                                                break
                                        else:
                                            if getattr(maps[map_idx][check_y][check_x], 'wumpus', False):
                                                other_wumpus_nearby = True
                                                break
                                
                                if not other_wumpus_nearby:
                                    if isinstance(maps[map_idx][adj_y][adj_x], list):
                                        maps[map_idx][adj_y][adj_x][1] = False
                                    else:
                                        maps[map_idx][adj_y][adj_x].stench = False
                # Store previous Wumpus positions before updating
                previous_wumpus_positions = set()
                for row_idx, row in enumerate(maps[count_map]):
                    for col_idx, cell in enumerate(row):
                        if isinstance(cell, list) and 'W' in cell[0]:
                            previous_wumpus_positions.add((col_idx, row_idx))
                        elif hasattr(cell, 'wumpus') and cell.wumpus:
                            previous_wumpus_positions.add((col_idx, row_idx))
            
                # Update map with new environment
                maps[count_map - 1] = env_maps[index_env + 1]
                
                
                if count_map + 1 < len(maps):
                    M2.updateMap(maps[count_map + 1])
                    count_map += 1
                else:
                    M2.updateMap(maps[count_map])
                
                showGameBackground(screen)
                M2.showUnknownBoard()
                
                for pos_x, pos_y in visited_positions:
                    M2.showPath(pos_x, pos_y)
                
                # M2.showAgent(y, x, M2.h)
                if not agent_died:
                    M2.showAgent(y, x, M2.h)
                
                for kx, ky in killed_wumpus_positions:
                    if 0 <= kx < map_size and 0 <= ky < map_size:
                        M2.showEmpty(ky, kx, M2.h)
                
                pygame.display.flip()
            
            else:
                for arr_x, arr_y in arrow_path:
                    if (arr_x, arr_y) in visited_positions:
                        M2.showPath(arr_x, arr_y)
                    else:
                        if (arr_y < len(maps[count_map]) and 
                            arr_x < len(maps[count_map][arr_y])):
                            M2.showUnknownWithOverlay(arr_y, arr_x, M2.h, maps[count_map][arr_y][arr_x])
                        else:
                            M2.showUnknown(arr_y, arr_x, M2.h)
                pygame.time.wait(200)

        elif action == 'DIE':
            count_action += 1
            current_action = "DIED"
            # M2.showDie(y, x, M2.h)
            agent_died = True
            M2.showPath(y, x)  # Hiển thị ô đường đi
            M2.showDie(y, x, M2.h)  # Hiển thị mộ
        
        if died and action != 'DIE':
            agent_died = True
            current_action = "DIED"
            M2.showPath(y, x)
            M2.showDie(y, x, M2.h)  # Hiển thị mộ
            
        # Handle final step
        if current_step >= len(path):
            final_action = path[-1][1]
            final_died = len(path[-1]) > 3 and path[-1][3] == 0
            final_x, final_y = path[-1][0]

            if final_died:
                M2.showPath(final_x, final_y)
                M2.showDie(final_y, final_x, M2.h)
            elif final_action == 'Climb' and final_x == 0 and final_y == 0:
                M2.showPath(final_x, final_y)
            else:
                M2.showPath(final_x, final_y)
                if not agent_died:
                    M2.showAgent(final_y, final_x, M2.h)
        
        # Kiểm tra cập nhật môi trường từ list_env

        

        M2.updateMap(maps[count_map])
        showGameBackground(screen)
        M2.showUnknownBoard()
        for pos_x, pos_y in visited_positions:
            M2.showPath(pos_x, pos_y)
        for kx, ky in killed_wumpus_positions:
            if 0 <= kx < map_size and 0 <= ky < map_size:
                M2.showEmpty(ky, kx, M2.h)
        # M2.showAgent(y, x, M2.h)
        
        # # Chỉ hiển thị agent nếu chưa chết và không climb out
        # if not agent_died:
        #     M2.showAgent(y, x, M2.h)
        # elif agent_died and action == 'DIE':
        #     M2.showDie(y, x, M2.h)  # Hiển thị mộ nếu agent chết
        if not agent_died:
        # Chỉ hiển thị agent nếu không ở trạng thái CLIMB tại (0,0)
            if not (action in ['Climb', 'CLIMB'] and x == 0 and y == 0):
                M2.showAgent(y, x, M2.h)
        elif agent_died and (action == 'DIE' or died):
            M2.showDie(y, x, M2.h)
            
        I2.showLeftBar(map_size, score=current_score)
        current_step += 1
        
        return True

    # Main game loop
    clock = pygame.time.Clock()
    
    # ...existing code...
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Nếu là chế độ Double Agent, đang ở Auto Play hoặc Step, và nhấn Enter lần nữa thì dừng
                if agent_mode == 1 and selected_button in [0, 1]:
                    if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                        # Nếu đã hết path hoặc auto_play vừa kết thúc thì dừng luôn
                        if (selected_button == 0 and (not auto_play) and current_step >= len(path)) or \
                        (selected_button == 1 and current_step >= len(path)):
                            return
                        # Nếu chưa auto_play thì vẫn thực hiện như thường
                        if selected_button == 0:  # Auto Play button
                            auto_play = not auto_play
                            auto_play_timer = 0
                        elif selected_button == 1:  # Step button
                            if not auto_play and current_step < len(path):
                                execute_step()
                        continue

                # Các nút khác vẫn xử lý như cũ
                if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                    if selected_button == 0:  # Auto Play button
                        auto_play = not auto_play
                        auto_play_timer = 0
                    elif selected_button == 1:  # Step button
                        if not auto_play and current_step < len(path):
                            execute_step()
                    elif selected_button == 2:  # Reset button
                        current_step = 0
                        auto_play = False
                        direction = 1
                        current_direction = "EAST"
                        current_action = "START"
                        current_score = 0
                        has_gold = False
                        count_map = 0
                        index_env = 0
                        count_action = 0
                        agent_died = False
                        killed_wumpus_positions.clear()
                        visited_positions = set([(0, 0)])  # Reset visited positions
                        
                        maps = []
                        for map_layer in original_maps:
                            restored_map = []
                            for row in map_layer:
                                restored_row = []
                                for cell in row:
                                    restored_cell = [cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]]
                                    restored_row.append(restored_cell)
                                restored_map.append(restored_row)
                            maps.append(restored_map)
                        
                        showGameBackground(screen)
                        M2 = Map(screen, maps[0] if maps else [])
                        M2.showUnknownBoard()
                        M2.showPath(0, 0)
                        M2.showAgent(0, 0, M2.h)
                        I2.showLeftBar(map_size, score=0)
                    elif selected_button == 3:  # Exit button
                        return
                elif event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % 4
                elif event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % 4

        # Auto play logic
        if auto_play and current_step < len(path):
            auto_play_timer += clock.get_time()
            if auto_play_timer >= 500:
                execute_step()
                auto_play_timer = 0
                if current_step >= len(path):
                    auto_play = False
        # Draw everything
        draw_action_info(agent_index)
        draw_buttons()
        if agent_mode == 1 and current_step >= len(path)  and agent_index == 0:
            hint_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)
            hint_text = "Press play or step again to move to the next agent."
            hint_surface = hint_font.render(hint_text, True, (255, 215, 0))
            text_width = hint_surface.get_width()
            screen.blit(hint_surface, (WINDOW_WIDTH - text_width - 40, WINDOW_HEIGHT - 40))
        elif agent_mode == 1 and current_step >= len(path) and agent_index == 1:
            hint_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)
            hint_text = "Press play or step or exit to exit."
            hint_surface = hint_font.render(hint_text, True, (255, 215, 0))
            text_width = hint_surface.get_width()
            screen.blit(hint_surface, (WINDOW_WIDTH - text_width - 40, WINDOW_HEIGHT - 40))
        pygame.display.flip()
        clock.tick(60)