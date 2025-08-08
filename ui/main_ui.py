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
            ##############################################
            # If result is None, continue the menu loop
        elif choose_option == 1:  # Quit
            pygame.quit()
            sys.exit()

        pygame.display.update()



def showWumpusWorld(map_data):
    M1 = Map(screen, map_data)
    showGameBackground(screen, level=1)
    M1.showUnknownBoard()  # This now shows faded overlays
    # Reveal starting position (0,0) and show agent there
    M1.showPath(0, 0)  # Reveal the starting cell
    I1 = Info(screen, level=1)
    # Calculate map size from map_data
    map_size = len(map_data) if map_data else 4
    # Start with score = 0
    I1.showLeftBar(map_size, score=0)
    pygame.display.update()
    # Removed pygame.time.wait(2000)

def showAgentMove(_, path, maps_data, __, agent_point):
    I2 = Info(screen, level=1)
    direction = 1
    current_score = 0
    has_gold = False
    current_step = 0
    auto_play = False
    auto_play_timer = 0
    selected_button = 0  # 0: Auto Play, 1: Step, 2: Reset, 3: Exit

    # Button setup - positioned below the left bar area
    button_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)
    button_width = 120
    button_height = 40
    button_margin = 10
    
    # Position buttons below the showLeftBar area (around y=200)
    base_x = 870  # Align with left bar content
    base_y = 200  # Start below the score display
    
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
                # Create proper cell data with the right format
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
                
                # Only show stench/breeze as effects if the cell doesn't have main elements
                stench = getattr(cell, 'stench', False) and not (has_wumpus or has_pit or has_gold)
                breeze = getattr(cell, 'breeze', False) and not (has_wumpus or has_pit or has_gold)
                
                cell_data = [
                    element,
                    stench,
                    breeze,
                    False,  # whiff (not used in basic Wumpus)
                    getattr(cell, 'glitter', False),
                    False  # scream
                ]
                map_row.append(cell_data)
            map_layer.append(map_row)
        maps.append(map_layer)

    count_map = 0 if len(maps) > 0 else 1
    M2 = Map(screen, maps[0] if maps else [])
    map_size = len(maps[0]) if maps and len(maps[0]) > 0 else 4
    killed_wumpus_positions = set()

    # Initialize display - show starting position with agent
    showGameBackground(screen, level=1)
    M2.showUnknownBoard()
    M2.showPath(0, 0)  # Reveal the starting cell
    M2.showAgent(0, 0, M2.h)  # Show agent at starting position
    I2.showLeftBar(map_size, score=0)

    # Draw control buttons
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
                
        # Show current step info above buttons
        step_info = button_font.render(f"Step: {current_step}/{len(path)}", True, DARK_RED_COLOR)
        screen.blit(step_info, (base_x, base_y - 30))

    def execute_step():
        nonlocal current_step, direction, current_score, count_map, killed_wumpus_positions
        
        if current_step >= len(path):
            return False
            
        i = current_step
        
        # Clear agent from previous position
        if i > 0:
            prev_x, prev_y = path[i - 1][0]
            M2.showPath(prev_x, prev_y)  # This removes agent and shows cell content only
        else:
            # For first step, clear agent from starting position (0,0)
            M2.showPath(0, 0)

        x, y = path[i][0]
        action = path[i][1]
        
        if len(path[i]) > 2:
            current_score = path[i][2]
        
        if action == 'Grab Gold':
            has_gold = True
        
        died = False
        if len(path[i]) > 3:
            died = path[i][3] == 0

        M2.showPath(x, y)
        M2.showAgent(y, x, M2.h)

        if action == 'Turn Left':
            direction = M2.turnLeft(direction)
            M2.showAgent(y, x, M2.h)

        elif action == 'Turn Right':
            direction = M2.turnRight(direction)
            M2.showAgent(y, x, M2.h)

        elif action == 'Grab Gold':
            M2.showGold(y, x, M2.h)
            if count_map + 1 < len(maps):
                M2.updateMap(maps[count_map + 1])
                count_map += 1

        elif action == 'Shoot' or action == 'SHOOT_HIT' or action == 'SHOOT_MISS':
            x_shoot, y_shoot = M2.agentShoot(path, i, direction)
            
            # Check if shot hit a Wumpus
            shot_hit = False
            if action == 'SHOOT_HIT':
                shot_hit = True
            elif len(maps) > count_map and 0 <= y_shoot < len(maps[count_map]) and 0 <= x_shoot < len(maps[count_map][y_shoot]):
                # Check if there's a Wumpus at the shot location
                cell_data = maps[count_map][y_shoot][x_shoot]
                if isinstance(cell_data, list):
                    shot_hit = 'W' in cell_data[0]
                else:
                    shot_hit = getattr(cell_data, 'wumpus', False)
            
            if shot_hit:
                # Show scream immediately and update display
                M2.showScream(y_shoot, x_shoot, M2.h)
                pygame.display.flip()
                pygame.time.wait(500)  # Show scream for 0.5 seconds
                
                killed_wumpus_positions.add((x_shoot, y_shoot))
                
                # Remove Wumpus from current and all future maps
                for map_idx in range(count_map, len(maps)):
                    if (0 <= y_shoot < len(maps[map_idx]) and 
                        0 <= x_shoot < len(maps[map_idx][y_shoot])):
                        
                        # Remove Wumpus from cell
                        if isinstance(maps[map_idx][y_shoot][x_shoot], list):
                            cell_content = maps[map_idx][y_shoot][x_shoot][0]
                            maps[map_idx][y_shoot][x_shoot][0] = cell_content.replace('W', '')
                            if maps[map_idx][y_shoot][x_shoot][0] == '':
                                maps[map_idx][y_shoot][x_shoot][0] = '-'
                        else:
                            maps[map_idx][y_shoot][x_shoot].wumpus = False
                        
                        # Remove stench from adjacent cells
                        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            adj_x, adj_y = x_shoot + dx, y_shoot + dy
                            if (0 <= adj_x < map_size and 0 <= adj_y < map_size and
                                adj_y < len(maps[map_idx]) and adj_x < len(maps[map_idx][adj_y])):
                                
                                # Check if there are other Wumpuses nearby before removing stench
                                other_wumpus_nearby = False
                                for dx2, dy2 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                                    check_x, check_y = adj_x + dx2, adj_y + dy2
                                    if (0 <= check_x < map_size and 0 <= check_y < map_size and
                                        check_y < len(maps[map_idx]) and check_x < len(maps[map_idx][check_y])):
                                        
                                        if isinstance(maps[map_idx][check_y][check_x], list):
                                            if 'W' in maps[map_idx][check_y][check_x][0]:
                                                other_wumpus_nearby = True
                                                break
                                        else:
                                            if getattr(maps[map_idx][check_y][check_x], 'wumpus', False):
                                                other_wumpus_nearby = True
                                                break
                                
                                # Only remove stench if no other Wumpus nearby
                                if not other_wumpus_nearby:
                                    if isinstance(maps[map_idx][adj_y][adj_x], list):
                                        maps[map_idx][adj_y][adj_x][1] = False  # Remove stench
                                    else:
                                        maps[map_idx][adj_y][adj_x].stench = False
                
                # Update to next map if available
                if count_map + 1 < len(maps):
                    M2.updateMap(maps[count_map + 1])
                    count_map += 1
                else:
                    # If no next map, update current map display
                    M2.updateMap(maps[count_map])
                
                # Refresh the entire board to show updated map without Wumpus and stench
                showGameBackground(screen, level=1)
                M2.showUnknownBoard()
                
                # Re-reveal all previously visited cells
                for step_idx in range(current_step):
                    step_x, step_y = path[step_idx][0]
                    M2.showPath(step_x, step_y)
                
                # Show current position with agent
                M2.showPath(x, y)
                M2.showAgent(y, x, M2.h)
                
                # Always refresh killed Wumpus positions display (show as empty)
                for kx, ky in killed_wumpus_positions:
                    if 0 <= kx < map_size and 0 <= ky < map_size:
                        M2.showEmpty(ky, kx, M2.h)
                
                # Update display immediately
                pygame.display.flip()
            
            else:
                # Miss - just show the arrow
                pygame.time.wait(200)  # Brief pause to show arrow

        I2.showLeftBar(map_size, score=current_score)
        current_step += 1
        
        # Handle final step
        if current_step >= len(path):
            final_action = path[-1][1]
            final_died = len(path[-1]) > 3 and path[-1][3] == 0
            final_x, final_y = path[-1][0]

            if final_died:
                # Agent died from Wumpus or Pit
                M2.showPath(final_x, final_y)
                M2.showDie(final_y, final_x, M2.h)
            elif final_action == 'Climb' and final_x == 0 and final_y == 0:
                # Agent successfully climbed out at (0,0) with gold
                M2.showPath(final_x, final_y)
            else:
                # Agent ran out of moves or couldn't complete the mission
                M2.showPath(final_x, final_y)
        
        return True

    # Main game loop
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
                    if selected_button == 0:  # Auto Play button
                        auto_play = not auto_play
                        auto_play_timer = 0
                    elif selected_button == 1:  # Step button
                        if not auto_play and current_step < len(path):
                            execute_step()
                    elif selected_button == 2:  # Reset button
                        # Reset simulation
                        current_step = 0
                        auto_play = False
                        direction = 1
                        current_score = 0
                        count_map = 0
                        killed_wumpus_positions.clear()
                        # Reset map display
                        showGameBackground(screen, level=1)
                        M2 = Map(screen, maps[0] if maps else [])
                        M2.showUnknownBoard()
                        M2.showPath(0, 0)  # Reveal starting cell
                        M2.showAgent(0, 0, M2.h)  # Show agent at starting position
                        I2.showLeftBar(map_size, score=0)
                    elif selected_button == 3:  # Exit button
                        return  # Return to menu
                elif event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % 4
                elif event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % 4

        # Auto play logic
        if auto_play and current_step < len(path):
            auto_play_timer += clock.get_time()
            if auto_play_timer >= 500:  # 500ms between steps
                execute_step()
                auto_play_timer = 0
                if current_step >= len(path):
                    auto_play = False

        # Draw everything
        draw_buttons()
        pygame.display.flip()
        clock.tick(60)