# # # Bảo thêm
# import pygame, sys
# from pygame.locals import *
# from ui.constants import *
# from ui.choice import *
# from ui.image import *

# pygame.init()
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption('WumPus Game')

# def inputForm():
#     pygame.font.init()
#     font = pygame.font.SysFont(FONT_TYPE, FONT_LARGE, bold=True)
#     clock = pygame.time.Clock()

#     input_boxes = [
#         {"label": "Enter map size:", "value": "", "type": "int"},
#         {"label": "Enter pit probability:", "value": "", "type": "float"},
#         {"label": "Enter number of Wumpus:", "value": "", "type": "int"},
#     ]
#     active_box = 0

#     while True:
#         showMenuBackground(screen)

#         for i, box in enumerate(input_boxes):
#             label_color = DARK_RED_COLOR if i == active_box else WHITE_COLOR
#             label_surface = font.render(box["label"], True, label_color)
#             value_surface = font.render(box["value"], True, WHITE_COLOR)

#             y = 150 + i * 100
#             screen.blit(label_surface, (100, y))
#             screen.blit(value_surface, (100 + label_surface.get_width() + 20, y))

#         small_font = pygame.font.SysFont(FONT_TYPE, FONT_MEDIUM)
#         instructions = small_font.render("Up/Down: Navigate  |  Enter: Confirm  |  Esc: Back to Menu", True, WHITE_COLOR)
#         screen.blit(instructions, (100, 500))

#         pygame.display.flip()
#         clock.tick(30)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     return None  # Return None to indicate going back to menu

#                 elif event.key == pygame.K_UP:
#                     active_box = (active_box - 1) % len(input_boxes)

#                 elif event.key == pygame.K_DOWN:
#                     active_box = (active_box + 1) % len(input_boxes)

#                 elif event.key == pygame.K_BACKSPACE:
#                     input_boxes[active_box]["value"] = input_boxes[active_box]["value"][:-1]

#                 elif event.key == pygame.K_RETURN:
#                     # Check if all fields are filled and valid
#                     all_filled = all(box["value"].strip() for box in input_boxes)
#                     if all_filled:
#                         try:
#                             size = int(input_boxes[0]["value"])
#                             prob = float(input_boxes[1]["value"])
#                             wumpus = int(input_boxes[2]["value"])
                            
#                             return size, prob, wumpus
#                         except:
#                             pass

#                 else:
#                     if event.unicode.isprintable():
#                         input_boxes[active_box]["value"] += event.unicode

# def showMenu():
#     showMenuBackground(screen)
#     menuChoice = ['Play', 'Quit']
#     menu = Choice(screen, menuChoice, 'WumPus Game')

#     while True:
#         is_up = is_down = is_left = is_right = is_enter = False

#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_DOWN:
#                     is_down = True
#                 elif event.key == pygame.K_UP:
#                     is_up = True
#                 elif event.key == pygame.K_LEFT:
#                     is_left = True
#                 elif event.key == pygame.K_RIGHT:
#                     is_right = True
#                 elif event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
#                     is_enter = True

#         menu.display_option(is_up, is_down, is_left, is_right, is_enter)
#         choose_option = menu.get_option_result()

#         if choose_option == 0:  # Play
#             result = inputForm()
#             if result is not None:  # Only return if we got valid input
#                 return result
#             #return (8, 0.2, 2)
#             ##############################################
#             # If result is None, continue the menu loop
#         elif choose_option == 1:  # Quit
#             pygame.quit()
#             sys.exit()

#         pygame.display.update()



# def showWumpusWorld(map_data):
#     M1 = Map(screen, map_data)
#     showGameBackground(screen, level=1)
#     M1.showUnknownBoard()  # This now shows faded overlays
#     # Reveal starting position (0,0) and show agent there
#     M1.showPath(0, 0)  # Reveal the starting cell
#     I1 = Info(screen, level=1)
#     # Calculate map size from map_data
#     map_size = len(map_data) if map_data else 4
#     # Start with score = 0
#     I1.showLeftBar(map_size, score=0)
#     pygame.display.update()
#     # Removed pygame.time.wait(2000)

# def showAgentMove(_, path, maps_data, __, agent_point):
#     I2 = Info(screen, level=1)
#     current_direction = "EAST"  # Track agent's actual direction
#     direction = 1  # UI direction counter for rotation
#     current_score = 0
#     has_gold = False
#     current_step = 0
#     auto_play = False
#     auto_play_timer = 0
#     selected_button = 0  # 0: Auto Play, 1: Step, 2: Reset, 3: Exit

#     # Button setup - positioned below the left bar area
#     button_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)
#     button_width = 120
#     button_height = 40
#     button_margin = 10
    
#     # Position buttons below the showLeftBar area (around y=200)
#     base_x = 870  # Align with left bar content
#     base_y = 200  # Start below the score display
    
#     auto_button_rect = pygame.Rect(base_x, base_y, button_width, button_height)
#     step_button_rect = pygame.Rect(base_x, base_y + button_height + button_margin, button_width, button_height)
#     reset_button_rect = pygame.Rect(base_x, base_y + (button_height + button_margin) * 2, button_width, button_height)
#     exit_button_rect = pygame.Rect(base_x, base_y + (button_height + button_margin) * 3, button_width, button_height)
    
#     # Convert maps_data to expected format
#     maps = []
#     for env_grid in maps_data:
#         map_layer = []
#         for row in env_grid:
#             map_row = []
#             for cell in row:
#                 # Create proper cell data with the right format
#                 has_wumpus = getattr(cell, 'wumpus', False)
#                 has_pit = getattr(cell, 'pit', False) 
#                 has_gold = getattr(cell, 'gold', False)
                
#                 element = ''
#                 if has_wumpus:
#                     element += 'W'
#                 if has_pit:
#                     element += 'P'
#                 if has_gold:
#                     element += 'G'
#                 if element == '':
#                     element = '-'
                
#                 # Always show stench and breeze when they exist, regardless of main elements
#                 stench = getattr(cell, 'stench', False)
#                 breeze = getattr(cell, 'breeze', False)
                
#                 cell_data = [
#                     element,
#                     stench,
#                     breeze,
#                     False,  # whiff (not used in basic Wumpus)
#                     getattr(cell, 'glitter', False),
#                     False  # scream
#                 ]
#                 map_row.append(cell_data)
#             map_layer.append(map_row)
#         maps.append(map_layer)

#     # Store original maps for reset functionality
#     original_maps = []
#     for map_layer in maps:
#         original_map = []
#         for row in map_layer:
#             original_row = []
#             for cell in row:
#                 # Deep copy each cell data
#                 original_cell = [cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]]
#                 original_row.append(original_cell)
#             original_map.append(original_row)
#         original_maps.append(original_map)
        
#     count_map = 0 if len(maps) > 0 else 1
#     M2 = Map(screen, maps[0] if maps else [])
#     map_size = len(maps[0]) if maps and len(maps[0]) > 0 else 4
#     killed_wumpus_positions = set()

#     # Initialize display - show starting position with agent
#     showGameBackground(screen, level=1)
#     M2.showUnknownBoard()
#     M2.showPath(0, 0)  # Reveal the starting cell
#     M2.showAgent(0, 0, M2.h)  # Show agent at starting position
#     I2.showLeftBar(map_size, score=0)

#     # Draw control buttons
#     def draw_buttons():
#         # Auto Play button
#         auto_color = WHITE_COLOR if selected_button == 0 else DARK_RED_COLOR
#         pygame.draw.rect(screen, auto_color, auto_button_rect, 2)
#         auto_text = button_font.render("Play", True, auto_color)
#         text_rect = auto_text.get_rect(center=auto_button_rect.center)
#         screen.blit(auto_text, text_rect)

#         # Step button
#         step_color = WHITE_COLOR if selected_button == 1 else DARK_RED_COLOR
#         pygame.draw.rect(screen, step_color, step_button_rect, 2)
#         step_text = button_font.render("Step", True, step_color)
#         text_rect = step_text.get_rect(center=step_button_rect.center)
#         screen.blit(step_text, text_rect)

#         # Reset button
#         reset_color = WHITE_COLOR if selected_button == 2 else DARK_RED_COLOR
#         pygame.draw.rect(screen, reset_color, reset_button_rect, 2)
#         reset_text = button_font.render("Reset", True, reset_color)
#         text_rect = reset_text.get_rect(center=reset_button_rect.center)
#         screen.blit(reset_text, text_rect)

#         # Exit button
#         exit_color = WHITE_COLOR if selected_button == 3 else DARK_RED_COLOR
#         pygame.draw.rect(screen, exit_color, exit_button_rect, 2)
#         exit_text = button_font.render("Exit", True, exit_color)
#         text_rect = exit_text.get_rect(center=exit_button_rect.center)
#         screen.blit(exit_text, text_rect)
                
#         # Show current step info above buttons
#         step_info = button_font.render(f"Step: {current_step}/{len(path)}", True, DARK_RED_COLOR)
#         screen.blit(step_info, (base_x, base_y - 30))

#     def execute_step():
#         nonlocal current_step, direction, current_score, count_map, killed_wumpus_positions, current_direction
        
#         if current_step >= len(path):
#             return False
            
#         i = current_step
        
#         # Clear agent from previous position
#         if i > 0:
#             prev_x, prev_y = path[i - 1][0]
#             M2.showPath(prev_x, prev_y)  # This removes agent and shows cell content only
#         else:
#             # For first step, clear agent from starting position (0,0)
#             M2.showPath(0, 0)

#         x, y = path[i][0]
#         action = path[i][1]
        
#         if len(path[i]) > 2:
#             current_score = path[i][2]
        
#         if action == 'Grab Gold':
#             has_gold = True
        
#         died = False
#         if len(path[i]) > 3:
#             died = path[i][3] == 0

#         M2.showPath(x, y)
#         M2.showAgent(y, x, M2.h)

#         if action == 'Turn Left' or action == 'TURN_LEFT':
#             direction = M2.turnLeft(direction)
#             # Update actual direction
#             dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
#             idx = dirs.index(current_direction)
#             current_direction = dirs[(idx + 1) % 4]
#             M2.showAgent(y, x, M2.h)

#         elif action == 'Turn Right' or action == 'TURN_RIGHT':
#             direction = M2.turnRight(direction)
#             # Update actual direction
#             dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
#             idx = dirs.index(current_direction)
#             current_direction = dirs[(idx + 1) % 4]
#             M2.showAgent(y, x, M2.h)

#         elif action == 'Grab Gold' or action == 'GRAB':
#             M2.showGold(y, x, M2.h)
#             if count_map + 1 < len(maps):
#                 M2.updateMap(maps[count_map + 1])
#                 count_map += 1

#         elif action == 'Shoot' or action == 'SHOOT_HIT' or action == 'SHOOT_MISS':
#             # Calculate shoot direction based on current_direction
#             dx, dy = {
#                 "NORTH": (0, 1),
#                 "EAST": (1, 0),
#                 "SOUTH": (0, -1),
#                 "WEST": (-1, 0)
#             }.get(current_direction, (1, 0))
            
#             # Track visited cells up to current step
#             visited_cells = set()
#             for step_idx in range(current_step + 1):  # Include current step
#                 step_x, step_y = path[step_idx][0]
#                 visited_cells.add((step_x, step_y))
            
#             # Animate arrow movement until it hits something or wall
#             arrow_x, arrow_y = x, y
#             hit_target = False
#             arrow_path = []  # Track arrow's path
            
#             while True:
#                 # Move arrow to next position
#                 arrow_x += dx
#                 arrow_y += dy
                
#                 # Check if arrow is out of bounds (hit wall)
#                 if arrow_x < 0 or arrow_x >= map_size or arrow_y < 0 or arrow_y >= map_size:
#                     break
                
#                 arrow_path.append((arrow_x, arrow_y))
                
#                 # Show arrow at current position
#                 M2.showShoot(arrow_y, arrow_x, M2.h)
#                 pygame.display.flip()
#                 pygame.time.wait(200)  # Arrow movement delay
                
#                 # Check if arrow hit a Wumpus at this position
#                 if (arrow_y < len(maps[count_map]) and 
#                     arrow_x < len(maps[count_map][arrow_y])):
                    
#                     cell_data = maps[count_map][arrow_y][arrow_x]
#                     if isinstance(cell_data, list):
#                         has_wumpus = 'W' in cell_data[0]
#                     else:
#                         has_wumpus = getattr(cell_data, 'wumpus', False)
                    
#                     if has_wumpus:
#                         hit_target = True
#                         break
                
#                 # Restore cell state: if visited, show path; if not visited, show unknown
#                 if (arrow_x, arrow_y) in visited_cells:
#                     M2.showPath(arrow_x, arrow_y)
#                 else:
#                     # Show unknown with overlay for unvisited cells
#                     if (arrow_y < len(maps[count_map]) and 
#                         arrow_x < len(maps[count_map][arrow_y])):
#                         M2.showUnknownWithOverlay(arrow_y, arrow_x, M2.h, maps[count_map][arrow_y][arrow_x])
#                     else:
#                         M2.showUnknown(arrow_y, arrow_x, M2.h)
            
#             # Handle hit result
#             if hit_target and action == 'SHOOT_HIT':
#                 # Show scream at hit location
#                 M2.showScream(arrow_y, arrow_x, M2.h)
#                 pygame.display.flip()
#                 pygame.time.wait(500)  # Show scream for 0.5 seconds
                
#                 killed_wumpus_positions.add((arrow_x, arrow_y))
                
#                 # Remove Wumpus from current and all future maps
#                 for map_idx in range(count_map, len(maps)):
#                     if (0 <= arrow_y < len(maps[map_idx]) and 
#                         0 <= arrow_x < len(maps[map_idx][arrow_y])):
                        
#                         # Remove Wumpus from cell
#                         if isinstance(maps[map_idx][arrow_y][arrow_x], list):
#                             cell_content = maps[map_idx][arrow_y][arrow_x][0]
#                             maps[map_idx][arrow_y][arrow_x][0] = cell_content.replace('W', '')
#                             if maps[map_idx][arrow_y][arrow_x][0] == '':
#                                 maps[map_idx][arrow_y][arrow_x][0] = '-'
#                         else:
#                             maps[map_idx][arrow_y][arrow_x].wumpus = False
                        
#                         # Remove stench from adjacent cells
#                         for dx2, dy2 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#                             adj_x, adj_y = arrow_x + dx2, arrow_y + dy2
#                             if (0 <= adj_x < map_size and 0 <= adj_y < map_size and
#                                 adj_y < len(maps[map_idx]) and adj_x < len(maps[map_idx][adj_y])):
                                
#                                 # Check if there are other living Wumpuses nearby before removing stench
#                                 other_wumpus_nearby = False
#                                 for dx3, dy3 in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#                                     check_x, check_y = adj_x + dx3, adj_y + dy3
#                                     if (0 <= check_x < map_size and 0 <= check_y < map_size and
#                                         check_y < len(maps[map_idx]) and check_x < len(maps[map_idx][check_y]) and
#                                         (check_x, check_y) not in killed_wumpus_positions):  # Exclude killed Wumpus
                                        
#                                         if isinstance(maps[map_idx][check_y][check_x], list):
#                                             if 'W' in maps[map_idx][check_y][check_x][0]:
#                                                 other_wumpus_nearby = True
#                                                 break
#                                         else:
#                                             if getattr(maps[map_idx][check_y][check_x], 'wumpus', False):
#                                                 other_wumpus_nearby = True
#                                                 break
                                
#                                 # Only remove stench if no other living Wumpus nearby
#                                 if not other_wumpus_nearby:
#                                     if isinstance(maps[map_idx][adj_y][adj_x], list):
#                                         maps[map_idx][adj_y][adj_x][1] = False  # Remove stench
#                                     else:
#                                         maps[map_idx][adj_y][adj_x].stench = False
                
#                 # Update to next map if available
#                 if count_map + 1 < len(maps):
#                     M2.updateMap(maps[count_map + 1])
#                     count_map += 1
#                 else:
#                     # If no next map, update current map display
#                     M2.updateMap(maps[count_map])
                
#                 # Redraw the entire board to ensure stench changes are visible
#                 showGameBackground(screen, level=1)
#                 M2.showUnknownBoard()
                
#                 # # Re-reveal all previously visited cells
#                 # for step_x, step_y in visited_cells:
#                 #     M2.showPath(step_x, step_y)
#                 # Re-reveal all previously visited cells INCLUDING (0,0)
#                 visited_positions = set()
#                 visited_positions.add((0, 0))  
                
#                 for step_idx in range(current_step + 1):  
#                     step_x, step_y = path[step_idx][0]
#                     visited_positions.add((step_x, step_y))
                
#                 # Reveal all visited positions
#                 for pos_x, pos_y in visited_positions:
#                     M2.showPath(pos_x, pos_y)
                
                
#                 # Show current position with agent
#                 M2.showAgent(y, x, M2.h)
                
#                 # Always refresh killed Wumpus positions display (show as empty)
#                 for kx, ky in killed_wumpus_positions:
#                     if 0 <= kx < map_size and 0 <= ky < map_size:
#                         M2.showEmpty(ky, kx, M2.h)
                
#                 # Update display immediately
#                 pygame.display.flip()
            
#             else:
#                 # Miss - restore all arrow path cells to their proper state
#                 for arr_x, arr_y in arrow_path:
#                     if (arr_x, arr_y) in visited_cells:
#                         M2.showPath(arr_x, arr_y)
#                     else:
#                         # Show unknown with overlay for unvisited cells
#                         if (arr_y < len(maps[count_map]) and 
#                             arr_x < len(maps[count_map][arr_y])):
#                             M2.showUnknownWithOverlay(arr_y, arr_x, M2.h, maps[count_map][arr_y][arr_x])
#                         else:
#                             M2.showUnknown(arr_y, arr_x, M2.h)
#                 pygame.time.wait(200)  # Brief pause to show final state

#         I2.showLeftBar(map_size, score=current_score)
#         current_step += 1
        
#         # Handle final step
#         if current_step >= len(path):
#             final_action = path[-1][1]
#             final_died = len(path[-1]) > 3 and path[-1][3] == 0
#             final_x, final_y = path[-1][0]

#             if final_died:
#                 # Agent died from Wumpus or Pit
#                 M2.showPath(final_x, final_y)
#                 M2.showDie(final_y, final_x, M2.h)
#             elif final_action == 'Climb' and final_x == 0 and final_y == 0:
#                 # Agent successfully climbed out at (0,0) with gold
#                 M2.showPath(final_x, final_y)
#             else:
#                 # Agent ran out of moves or couldn't complete the mission
#                 M2.showPath(final_x, final_y)
        
#         return True

#     # Main game loop
#     clock = pygame.time.Clock()
    
#     while True:
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN or event.key == K_KP_ENTER:
#                     if selected_button == 0:  # Auto Play button
#                         auto_play = not auto_play
#                         auto_play_timer = 0
#                     elif selected_button == 1:  # Step button
#                         if not auto_play and current_step < len(path):
#                             execute_step()
#                     elif selected_button == 2:  # Reset button
#                         # Reset simulation
#                         current_step = 0
#                         auto_play = False
#                         direction = 1
#                         current_direction = "EAST"  # Reset agent direction
#                         current_score = 0
#                         count_map = 0
#                         killed_wumpus_positions.clear()
                        
#                          # Restore original maps data
#                         maps = []
#                         for map_layer in original_maps:
#                             restored_map = []
#                             for row in map_layer:
#                                 restored_row = []
#                                 for cell in row:
#                                     # Deep copy each cell data
#                                     restored_cell = [cell[0], cell[1], cell[2], cell[3], cell[4], cell[5]]
#                                     restored_row.append(restored_cell)
#                                 restored_map.append(restored_row)
#                             maps.append(restored_map)
#                         # Reset map display
#                         showGameBackground(screen, level=1)
#                         M2 = Map(screen, maps[0] if maps else [])
#                         M2.showUnknownBoard()
#                         M2.showPath(0, 0)  # Reveal starting cell
#                         M2.showAgent(0, 0, M2.h)  # Show agent at starting position
#                         I2.showLeftBar(map_size, score=0)
#                     elif selected_button == 3:  # Exit button
#                         return  # Return to menu
#                 elif event.key == pygame.K_UP:
#                     selected_button = (selected_button - 1) % 4
#                 elif event.key == pygame.K_DOWN:
#                     selected_button = (selected_button + 1) % 4

#         # Auto play logic
#         if auto_play and current_step < len(path):
#             auto_play_timer += clock.get_time()
#             if auto_play_timer >= 500:  # 500ms between steps
#                 execute_step()
#                 auto_play_timer = 0
#                 if current_step >= len(path):
#                     auto_play = False

#         # Draw everything
#         draw_buttons()
#         pygame.display.flip()
#         clock.tick(60)


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
    font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM)       # Dùng font từ file
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
            value_surface = font.render(box["value"], True, label_color)

            y = 150 + i * 100
            screen.blit(label_surface, (100, y))
            screen.blit(value_surface, (100 + label_surface.get_width() + 20, y))

        small_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)   # Font nhỏ cũng từ file
        instructions = small_font.render(
            "Up/Down: Navigate  |  Enter: Confirm  |  Esc: Back to Menu", True, WHITE_COLOR
        )
        screen.blit(instructions, (100, 500))

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
                    active_box = (active_box - 1) % len(input_boxes)

                elif event.key == pygame.K_DOWN:
                    active_box = (active_box + 1) % len(input_boxes)

                elif event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["value"] = input_boxes[active_box]["value"][:-1]

                elif event.key == pygame.K_RETURN:
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
            # return (8, 0.2, 2)
        elif choose_option == 1:  # Quit
            pygame.quit()
            sys.exit()

        pygame.display.update()

def showWumpusWorld(map_data):
    M1 = Map(screen, map_data)
    showGameBackground(screen, level=1)
    M1.showUnknownBoard()
    M1.showPath(0, 0)
    I1 = Info(screen, level=1)
    map_size = len(map_data) if map_data else 4
    I1.showLeftBar(map_size, score=0)
    pygame.display.update()

def showAgentMove(_, path, maps_data, __, agent_point):
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
    showGameBackground(screen, level=1)
    M2.showUnknownBoard()
    M2.showPath(0, 0)
    M2.showAgent(0, 0, M2.h)
    I2.showLeftBar(map_size, score=0)

    def draw_action_info():
        """Hiển thị thông tin action hiện tại và direction"""
        action_font = pygame.font.Font(FONT_TYPE, FONT_MEDIUM_SMALL)
        
        action_x = 860
        action_y = 150
        
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
        nonlocal current_step, direction, current_score, count_map, killed_wumpus_positions, current_direction, current_action, has_gold
        
        if current_step >= len(path):
            return False
            
        i = current_step
        
        # Clear agent from previous position
        if i > 0:
            prev_x, prev_y = path[i - 1][0]
            M2.showPath(prev_x, prev_y)
        else:
            M2.showPath(0, 0)

        x, y = path[i][0]
        action = path[i][1]
        current_action = action
        
        if len(path[i]) > 2:
            current_score = path[i][2]

        if action == 'Grab Gold' or action == 'GRAB':
            has_gold = True
        
        died = False
        if len(path[i]) > 3:
            died = path[i][3] == 0

        M2.showPath(x, y)
        M2.showAgent(y, x, M2.h)

        if action == 'Turn Left' or action == 'TURN_LEFT':
            current_action = "TURN LEFT"
            direction = M2.turnLeft(direction)
            dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
            idx = dirs.index(current_direction)
            current_direction = dirs[(idx + 1) % 4]
            M2.showAgent(y, x, M2.h)

        elif action == 'Turn Right' or action == 'TURN_RIGHT':
            current_action = "TURN RIGHT"
            direction = M2.turnRight(direction)
            dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
            idx = dirs.index(current_direction)
            current_direction = dirs[(idx + 1) % 4]
            M2.showAgent(y, x, M2.h)

        elif action == 'Move' or action == 'MOVE':
            current_action = "MOVE FORWARD"

        elif action == 'Grab Gold' or action == 'GRAB':
            current_action = "GRAB GOLD"
            has_gold = True
            M2.showGold(y, x, M2.h)
            if count_map + 1 < len(maps):
                M2.updateMap(maps[count_map + 1])
                count_map += 1

        elif action == 'Climb' or action == 'CLIMB':
            current_action = "CLIMB OUT"

        elif action == 'Shoot' or action == 'SHOOT_HIT' or action == 'SHOOT_MISS':
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
            visited_cells = set()
            for step_idx in range(current_step + 1):
                step_x, step_y = path[step_idx][0]
                visited_cells.add((step_x, step_y))
            
            # Animate arrow movement
            arrow_x, arrow_y = x, y
            hit_target = False
            arrow_path = []
            
            while True:
                arrow_x += dx
                arrow_y += dy
                
                if arrow_x < 0 or arrow_x >= map_size or arrow_y < 0 or arrow_y >= map_size:
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
                
                if (arrow_x, arrow_y) in visited_cells:
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
                
                if count_map + 1 < len(maps):
                    M2.updateMap(maps[count_map + 1])
                    count_map += 1
                else:
                    M2.updateMap(maps[count_map])
                
                showGameBackground(screen, level=1)
                M2.showUnknownBoard()
                
                visited_positions = set()
                visited_positions.add((0, 0))  
                
                for step_idx in range(current_step + 1):  
                    step_x, step_y = path[step_idx][0]
                    visited_positions.add((step_x, step_y))
                
                for pos_x, pos_y in visited_positions:
                    M2.showPath(pos_x, pos_y)
                
                M2.showAgent(y, x, M2.h)
                
                for kx, ky in killed_wumpus_positions:
                    if 0 <= kx < map_size and 0 <= ky < map_size:
                        M2.showEmpty(ky, kx, M2.h)
                
                pygame.display.flip()
            
            else:
                for arr_x, arr_y in arrow_path:
                    if (arr_x, arr_y) in visited_cells:
                        M2.showPath(arr_x, arr_y)
                    else:
                        if (arr_y < len(maps[count_map]) and 
                            arr_x < len(maps[count_map][arr_y])):
                            M2.showUnknownWithOverlay(arr_y, arr_x, M2.h, maps[count_map][arr_y][arr_x])
                        else:
                            M2.showUnknown(arr_y, arr_x, M2.h)
                pygame.time.wait(200)

        elif action == 'DIE':
            current_action = "DIED"
            M2.showDie(y, x, M2.h)

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
                        current_step = 0
                        auto_play = False
                        direction = 1
                        current_direction = "EAST"
                        current_action = "START"
                        current_score = 0
                        has_gold = False
                        count_map = 0
                        killed_wumpus_positions.clear()
                        
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
                        
                        showGameBackground(screen, level=1)
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
        draw_action_info()
        draw_buttons()
        pygame.display.flip()
        clock.tick(60)