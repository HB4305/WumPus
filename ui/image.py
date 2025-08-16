import pygame, sys, copy
from pygame.locals import *
from ui.constants import *
from ui.text import *

def showGameBackground(screen, area=None):
    background = pygame.image.load(f'ui/assets/game_background.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    if area == None:
        screen.blit(background, (0, 0))
    else:
        screen.blit(background, (area[0], area[1]), area)

def showMenuBackground(screen):
    background = pygame.image.load('ui/assets/menu_background.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background, (0, 0))

class ImageElement:
    def __init__(self, screen, cell_side=60):
        self.screen = screen
        self.cell_side = cell_side
        self.cell_size = (self.cell_side, self.cell_side)
        
        # Load and scale normal images
        self.empty_img = pygame.image.load('ui/assets/empty.png')
        self.empty_img = pygame.transform.scale(self.empty_img, self.cell_size)
        self.unknown_img = pygame.image.load('ui/assets/unknown.png')
        self.unknown_img = pygame.transform.scale(self.unknown_img, self.cell_size)
        
        self.agent_img = pygame.image.load('ui/assets/agent.png')
        self.agent_img = pygame.transform.scale(self.agent_img, self.cell_size)

        self.die_img = pygame.image.load('ui/assets/dies.png')
        self.die_img = pygame.transform.scale(self.die_img, self.cell_size)
     
        self.shoot_img = pygame.image.load('ui/assets/shoot.png')
        self.shoot_img = pygame.transform.scale(self.shoot_img, self.cell_size)
        self.gold_img = pygame.image.load('ui/assets/gold.png')
        self.gold_img = pygame.transform.scale(self.gold_img, self.cell_size)
        
        self.wumpus_img = pygame.image.load('ui/assets/wumpus.png')
        self.wumpus_img = pygame.transform.scale(self.wumpus_img, self.cell_size)
        self.stench_img = pygame.image.load('ui/assets/stench.png')
        self.stench_img = pygame.transform.scale(self.stench_img, self.cell_size)
        self.scream_img = pygame.image.load('ui/assets/scream.png')
        self.scream_img = pygame.transform.scale(self.scream_img, self.cell_size)
        
        self.pit_img = pygame.image.load('ui/assets/pit.png')
        self.pit_img = pygame.transform.scale(self.pit_img, self.cell_size)
        self.breeze_img = pygame.image.load('ui/assets/breeze.png')
        self.breeze_img = pygame.transform.scale(self.breeze_img, self.cell_size)
        
        # Create faded versions for unknown cells (30% opacity)
        self.faded_wumpus_img = self.wumpus_img.copy()
        self.faded_wumpus_img.set_alpha(80)  # ~30% opacity
        
        self.faded_pit_img = self.pit_img.copy()
        self.faded_pit_img.set_alpha(80)
        
        self.faded_stench_img = self.stench_img.copy()
        self.faded_stench_img.set_alpha(80)
        
        self.faded_breeze_img = self.breeze_img.copy()
        self.faded_breeze_img.set_alpha(80)
    
    # Show images
    def showEmpty(self, i, j, h):
        self.screen.blit(self.empty_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showUnknown(self, i, j, h):
        self.screen.blit(self.unknown_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showUnknownWithOverlay(self, i, j, h, cell_data):
        self.showUnknown(i, j, h)
        
        # Then overlay faded content
        if isinstance(cell_data, list):
            element = cell_data[0] if len(cell_data) > 0 else ''
            stench = cell_data[1] if len(cell_data) > 1 else False
            breeze = cell_data[2] if len(cell_data) > 2 else False
        else:
            # Handle Cell objects
            element = ''
            if hasattr(cell_data, 'wumpus') and cell_data.wumpus:
                element += 'W'
            if hasattr(cell_data, 'pit') and cell_data.pit:
                element += 'P'
            if hasattr(cell_data, 'gold') and cell_data.gold:
                element += 'G'
            if element == '':
                element = '-'
            stench = getattr(cell_data, 'stench', False)
            breeze = getattr(cell_data, 'breeze', False)
        
        # Show faded main elements
        main_element_shown = False
        
        if 'W' in element:
            self.screen.blit(self.faded_wumpus_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
            main_element_shown = True
        elif 'P' in element:
            self.screen.blit(self.faded_pit_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
            main_element_shown = True
        
        # Handle faded effects
        if not main_element_shown:
            # No main elements - show effects as primary faded display
            if stench and not breeze:  # Only stench
                self.screen.blit(self.faded_stench_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
            elif breeze and not stench:  # Only breeze
                self.screen.blit(self.faded_breeze_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
            elif stench and breeze:  # Both effects - show stench as base, breeze as overlay
                self.screen.blit(self.faded_stench_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
                faded_breeze_overlay = self.faded_breeze_img.copy()
                faded_breeze_overlay.set_alpha(50)  # Even more faded for overlay
                self.screen.blit(faded_breeze_overlay, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
        else:
            # Main element present - show effects as faded overlays
            overlay_alpha = 40
            
            # Show faded stench overlay if present (and not from same cell's Wumpus)
            if stench and 'W' not in element:
                faded_stench_overlay = self.faded_stench_img.copy()
                faded_stench_overlay.set_alpha(overlay_alpha)
                self.screen.blit(faded_stench_overlay, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
            
            # Show faded breeze overlay if present (and not from same cell's pit)
            if breeze and 'P' not in element:
                faded_breeze_overlay = self.faded_breeze_img.copy()
                faded_breeze_overlay.set_alpha(overlay_alpha)
                self.screen.blit(faded_breeze_overlay, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
            
            # If cell has Wumpus and breeze, or pit and stench, show both faded
            if 'W' in element and breeze:
                faded_breeze_overlay = self.faded_breeze_img.copy()
                faded_breeze_overlay.set_alpha(overlay_alpha)
                self.screen.blit(faded_breeze_overlay, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
            
            if 'P' in element and stench:
                faded_stench_overlay = self.faded_stench_img.copy()
                faded_stench_overlay.set_alpha(overlay_alpha)
                self.screen.blit(faded_stench_overlay, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
        
        # Agent is always shown on top if present
        if 'A' in element:
            self.showAgent(i, j, self.h)
    
    # Show images
    def showAgent(self, i, j, h):
        self.screen.blit(self.agent_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showDie(self, i, j, h):
        self.screen.blit(self.die_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showShoot(self, i, j, h):
        self.screen.blit(self.shoot_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showGold(self, i, j, h):
        self.screen.blit(self.gold_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showWumpus(self, i, j, h):
        self.screen.blit(self.wumpus_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showStench(self, i, j, h):
        self.screen.blit(self.stench_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showScream(self, i, j, h):
        # First show the cell content (empty or whatever is there)
        self.showEmpty(i, j, h)
        # Then overlay the scream image on top
        self.screen.blit(self.scream_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showPit(self, i, j, h):
        self.screen.blit(self.pit_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showBreeze(self, i, j, h):
        self.screen.blit(self.breeze_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    # turn Agent
    def turnLeft(self, drirection):
        self.agent_img = pygame.transform.rotate(self.agent_img, 90)
        self.shoot_img = pygame.transform.rotate(self.shoot_img, 90)
        return drirection+1
    def turnRight(self, drirection):
        self.agent_img = pygame.transform.rotate(self.agent_img, -90)
        self.shoot_img = pygame.transform.rotate(self.shoot_img, -90)
        return drirection-1

class Map(ImageElement):
    """
    This class is used to show the game map on the screen.

    Attributes:
        screen: The window screen to show the images on.
        map_data (2D list): The data of the game map.
            1 item of map_data is a list of 6 elements:
            [element, stench, breeze, whiff, glow, scream]
            [string, bool, bool, bool, bool, bool]
        cell_side (int): The side length of each cell.
        h (int): The height of the game map.
        w (int): The width of the game map.
    """
    def __init__(self, screen, map_data, cell_side=65):
        # Read and store map data
        self.map_data = copy.deepcopy(map_data)
        self.h = len(map_data)
        self.w = len(map_data[0])
        
        # Calculate cell size based on available space
        # Account for right sidebar (approximately 300px for buttons and info)
        right_sidebar_width = 300
        available_width = WINDOW_WIDTH - BOARD_APPEEAR_WIDTH - right_sidebar_width - 50  # Extra margin
        available_height = WINDOW_HEIGHT - BOARD_APPEEAR_HEIGHT - 50  # Leave margin for bottom
        
        # Calculate maximum cell size that fits
        max_cell_width = available_width // self.w if self.w > 0 else available_width
        max_cell_height = available_height // self.h if self.h > 0 else available_height
        cell_side = min(max_cell_width, max_cell_height)
        
        # Set minimum and maximum cell sizes
        cell_side = max(12, min(120, cell_side))  # Min 12px, Max 120px
        
        super().__init__(screen, cell_side)
    
    def updateMap(self, map_data):
        self.map_data = copy.deepcopy(map_data)
    
    def returnCellSide(self):
        return self.cell_side
    
    def agentShoot(self, path, now, drirection):
        # Path coordinates are in (x,y) format in your updated code
        x = path[now][0][0]
        y = path[now][0][1]
        
        # Get the actual direction from the agent if available
        # The direction parameter might not be reliable, so we calculate based on agent's actual direction
        shoot_x, shoot_y = x, y  # Default values
        
        # Map agent directions to coordinate changes
        # Agent uses: "NORTH" (0,1), "EAST" (1,0), "SOUTH" (0,-1), "WEST" (-1,0)
        # But we need to handle the UI direction system properly
        direction_map = {
            0: (1, 0),   # EAST (right)
            1: (0, 1),   # NORTH (up)  
            2: (-1, 0),  # WEST (left)
            3: (0, -1)   # SOUTH (down)
        }
        
        if drirection % 4 in direction_map:
            dx, dy = direction_map[drirection % 4]
            shoot_x, shoot_y = x + dx, y + dy
            
        # Make sure we're within bounds - coordinates are already in correct format
        if 0 <= shoot_x < self.w and 0 <= shoot_y < self.h:
            # Note: showShoot expects (row, col, height) format
            self.showShoot(shoot_y, shoot_x, self.h)
        return shoot_x, shoot_y
    
    def showUnknownBoard(self): # Show game map with unvisitted cells with faded overlays
        for y in range(0, self.h):
            for x in range(0, self.w):
                if y < len(self.map_data) and x < len(self.map_data[0]):
                    self.showUnknownWithOverlay(y, x, self.h, self.map_data[y][x])
                else:
                    self.showUnknown(y, x, self.h)
    
    def showKnownBoard(self): # Show game map with visitted cells
        y = 0
        x = 0
        #[element, stench, breeze, whiff, glow, scream]
        for y in range (0, self.h):
            for x in range (0, self.w):
                self.showPath(x, y)

    def showPath(self, x, y): # Show visitted cells - x is column, y is row
        #[element, stench, breeze, whiff, glow, scream]
        self.showEmpty(y, x, self.h)
        
        # Handle different data formats - check array bounds first
        if y >= len(self.map_data) or x >= len(self.map_data[0]):
            return
            
        # Handle different data formats
        if isinstance(self.map_data[y][x], list):
            # Format: [element, stench, breeze, whiff, glow, scream]
            element = self.map_data[y][x][0] if len(self.map_data[y][x]) > 0 else ''
            stench = self.map_data[y][x][1] if len(self.map_data[y][x]) > 1 else False
            breeze = self.map_data[y][x][2] if len(self.map_data[y][x]) > 2 else False
            scream = self.map_data[y][x][5] if len(self.map_data[y][x]) > 5 else False
        else:
            # Handle Cell objects from environment
            cell = self.map_data[y][x]
            element = ''
            if hasattr(cell, 'wumpus') and cell.wumpus:
                element += 'W'
            if hasattr(cell, 'pit') and cell.pit:
                element += 'P'
            if hasattr(cell, 'gold') and cell.gold:
                element += 'G'
            if element == '':
                element = '-'
                
            stench = getattr(cell, 'stench', False)
            breeze = getattr(cell, 'breeze', False)
            scream = getattr(cell, 'scream', False)
        
        # Show main elements first (highest priority)
        main_element_shown = False
        
        if 'W' in element:
            self.showWumpus(y, x, self.h)
            main_element_shown = True
        elif 'P' in element:
            self.showPit(y, x, self.h)
            main_element_shown = True

        elif 'G' in element:
            self.showGold(y, x, self.h)
            main_element_shown = True
        
        # Handle effects - show base effect and overlays
        if not main_element_shown:
            # No main elements - show effects as primary display
            if stench and not breeze:  # Only stench
                self.showStench(y, x, self.h)
            elif breeze and not stench:  # Only breeze
                self.showBreeze(y, x, self.h)
            elif stench and breeze:  # Both effects - show stench as base, breeze as overlay
                self.showStench(y, x, self.h)
                breeze_overlay = self.breeze_img.copy()
                breeze_overlay.set_alpha(150)  # Semi-transparent overlay
                self.screen.blit(breeze_overlay, (BOARD_APPEEAR_WIDTH + x*self.cell_side, BOARD_APPEEAR_HEIGHT + (self.h - 1 - y)*self.cell_side))
        else:
            # Main element present - show effects as overlays
            overlay_alpha = 120
            
            # Show stench overlay if present (and not from the same cell's Wumpus)
            if stench and 'W' not in element:
                stench_overlay = self.stench_img.copy()
                stench_overlay.set_alpha(overlay_alpha)
                self.screen.blit(stench_overlay, (BOARD_APPEEAR_WIDTH + x*self.cell_side, BOARD_APPEEAR_HEIGHT + (self.h - 1 - y)*self.cell_side))
            
            # Show breeze overlay if present (and not from the same cell's pit)
            if breeze and 'P' not in element:
                breeze_overlay = self.breeze_img.copy()
                breeze_overlay.set_alpha(overlay_alpha)
                self.screen.blit(breeze_overlay, (BOARD_APPEEAR_WIDTH + x*self.cell_side, BOARD_APPEEAR_HEIGHT + (self.h - 1 - y)*self.cell_side))
            
            # If cell has both Wumpus and breeze, or pit and stench, show both
            if 'W' in element and breeze:
                breeze_overlay = self.breeze_img.copy()
                breeze_overlay.set_alpha(overlay_alpha)
                self.screen.blit(breeze_overlay, (BOARD_APPEEAR_WIDTH + x*self.cell_side, BOARD_APPEEAR_HEIGHT + (self.h - 1 - y)*self.cell_side))
            
            if 'P' in element and stench:
                stench_overlay = self.stench_img.copy()
                stench_overlay.set_alpha(overlay_alpha)
                self.screen.blit(stench_overlay, (BOARD_APPEEAR_WIDTH + x*self.cell_side, BOARD_APPEEAR_HEIGHT + (self.h - 1 - y)*self.cell_side))
        
        # Agent is always shown on top if present
        if 'A' in element:
            self.showAgent(y, x, self.h)