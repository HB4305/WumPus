import pygame, sys, copy
from pygame.locals import *
from ui.constants import *
from ui.text import *

def showGameBackground(screen, area=None, level=1):
    #https://wallpapercave.com/w/wp7326071
    #area: (pos_x, pos_y, width, height)
    background = pygame.image.load(f'ui/assets/game_background_{level % 5}.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    if area == None:
        screen.blit(background, (0, 0))
    else:
        screen.blit(background, (area[0], area[1]), area)

def showMenuBackground(screen):
    #https://wallpapersafari.com/w/nLIPZf/download
    background = pygame.image.load('ui/assets/menu_background.jpg')
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background, (0, 0))

class ImageElement:
    """
    This class is used to show images on the screen.

    Attributes:
        screen: The window screen to show the images on.
        cell_side (int): The side length of each cell.
        cell_size tuple (int, int): The size of each cell.
        empty_img (image): The image of an empty cell (cell that contains nothing).
        unknown_img (image): The image of a cell which has not been visited.
        agent_img (image): The image of the agent.
        die_img (image): The image of the agent when he dies.
        shoot_img (image): The image of the arrow when the agent shoots.
        gold_img (image): The image of the gold chest.
        wumpus_img (image): The image of the Wumpus.
        stench_img (image): The image of the stench surrounding a Wumpus.
        scream_img (image): The image of the scream sound when the Wumpus dies.
        pit_img (image): The image of the pit.
        breeze_img (image): The image of the breeze surrounding a pit.
        poisonous_gas_img (image): The image of the poisonous gas.
        whiff_img (image): The image of the whiff surrounding the poisonous gas.
        healing_potion_img (image): The image of the healing potion.
        glow_img (image): The image of the glow surrounding the healing potion.
    """
    def __init__(self, screen, cell_side=60):
        self.screen = screen
        self.cell_side = cell_side
        self.cell_size = (self.cell_side, self.cell_side)
        self.empty_img = pygame.image.load('ui/assets/empty.png')
        self.empty_img = pygame.transform.scale(self.empty_img, self.cell_size)
        self.unknown_img = pygame.image.load('ui/assets/unknown.png')
        self.unknown_img = pygame.transform.scale(self.unknown_img, self.cell_size)
        #https://www.clipartmax.com/download/m2i8A0H7b1Z5d3Z5_miner-miner-png/
        self.agent_img = pygame.image.load('ui/assets/agent.png')
        self.agent_img = pygame.transform.scale(self.agent_img, self.cell_size)
        #https://www.pngwing.com/en/free-png-yeezt
        self.die_img = pygame.image.load('ui/assets/dies.png')
        self.die_img = pygame.transform.scale(self.die_img, self.cell_size)
        #https://pngtree.com/freepng/vector-of-png-bow-arrow_7258676.html
        self.shoot_img = pygame.image.load('ui/assets/shoot.png')
        self.shoot_img = pygame.transform.scale(self.shoot_img, self.cell_size)
        #https://www.hiclipart.com/free-transparent-background-png-clipart-iyjih
        self.gold_img = pygame.image.load('ui/assets/gold.png')
        self.gold_img = pygame.transform.scale(self.gold_img, self.cell_size)
        
        #https://yt3.googleusercontent.com/s_38Cu2ryXXDcK9fbfc9O-C23DZV1Lo8VgvDJbG_kRB7WctOofRD1gt-LNMGlJnx13-BaetK1w=s900-c-k-c0x00ffffff-no-rj
        self.wumpus_img = pygame.image.load('ui/assets/wumpus.png')
        self.wumpus_img = pygame.transform.scale(self.wumpus_img, self.cell_size)
        self.stench_img = pygame.image.load('ui/assets/stench.png')
        self.stench_img = pygame.transform.scale(self.stench_img, self.cell_size)
        self.scream_img = pygame.image.load('ui/assets/scream.png')
        self.scream_img = pygame.transform.scale(self.scream_img, self.cell_size)
        
        #https://www.pikpng.com/pngvi/mTJTmi_ground-clipart-crack-hole-in-ground-drawing-png-download/
        self.pit_img = pygame.image.load('ui/assets/pit.png')
        self.pit_img = pygame.transform.scale(self.pit_img, self.cell_size)
        self.breeze_img = pygame.image.load('ui/assets/breeze.png')
        self.breeze_img = pygame.transform.scale(self.breeze_img, self.cell_size)

        # Add placeholder images for missing elements
        self.poisonous_gas_img = self.pit_img  # Use pit image as placeholder
        self.whiff_img = self.breeze_img       # Use breeze image as placeholder
        self.healing_potion_img = self.gold_img # Use gold image as placeholder
        self.glow_img = self.stench_img        # Use stench image as placeholder

    
    # Show images
    def showEmpty(self, i, j, h):
        self.screen.blit(self.empty_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showUnknown(self, i, j, h):
        self.screen.blit(self.unknown_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
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
        self.screen.blit(self.scream_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showPoisonousGas(self, i, j, h):
        self.screen.blit(self.poisonous_gas_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showWhiff(self, i, j, h):
        self.screen.blit(self.whiff_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
    def showHealingPotion(self, i, j, h):
        self.screen.blit(self.healing_potion_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    def showGlow(self, i, j, h):
        self.screen.blit(self.glow_img, (BOARD_APPEEAR_WIDTH + j*self.cell_side, BOARD_APPEEAR_HEIGHT + (h - 1 - i)*self.cell_side))
    
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
        cell_side = 65
        if max(self.h, self.w) <= 5:
            cell_side = 120
        elif max(self.h, self.w) <= 10:
            cell_side = 65
        else:
            cell_side = 20
        super().__init__(screen, cell_side)
    
    def updateMap(self, map_data):
        self.map_data = copy.deepcopy(map_data)
    
    def returnCellSide(self):
        return self.cell_side
    
    def agentShoot(self, path, now, drirection):
        # Path coordinates are in (x,y) format in your updated code
        x = path[now][0][0]
        y = path[now][0][1]
        
        # mod = 0: right, 1: up, 2: left, 3: down
        shoot_x, shoot_y = x, y  # Default values
        if drirection % 4 == 0:  # right
            shoot_x, shoot_y = x + 1, y
        elif drirection % 4 == 1:  # up
            shoot_x, shoot_y = x, y + 1
        elif drirection % 4 == 2:  # left
            shoot_x, shoot_y = x - 1, y
        elif drirection % 4 == 3:  # down
            shoot_x, shoot_y = x, y - 1
            
        # Make sure we're within bounds
        if 0 <= shoot_y < self.h and 0 <= shoot_x < self.w:
            self.showShoot(shoot_y, shoot_x, self.h)
        return shoot_x, shoot_y
    
    def showUnknownBoard(self): # Show game map with unvisitted cells
        y = 0
        x = 0
        for y in range (0, self.h):
            for x in range (0, self.w):
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
            whiff = self.map_data[y][x][3] if len(self.map_data[y][x]) > 3 else False
            glow = self.map_data[y][x][4] if len(self.map_data[y][x]) > 4 else False
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
            whiff = getattr(cell, 'whiff', False)  # Added attribute check
            glow = getattr(cell, 'glitter', False)
            scream = getattr(cell, 'scream', False)  # Added attribute check
        
        # Show elements - use y,x for drawing as per your original methods
        if 'A' in element:
            self.showAgent(y, x, self.h)
        if 'G' in element:
            self.showGold(y, x, self.h)
        if 'W' in element:
            self.showWumpus(y, x, self.h)
        if 'P' in element and 'P_G' not in element:
            self.showPit(y, x, self.h)
        if 'P_G' in element:
            self.showPoisonousGas(y, x, self.h)
        if 'H_P' in element:
            self.showHealingPotion(y, x, self.h)

        # Show effects
        if stench:
            self.showStench(y, x, self.h)
        if breeze:
            self.showBreeze(y, x, self.h)
        if whiff:
            self.showWhiff(y, x, self.h)
        if glow:
            self.showGlow(y, x, self.h)
        if scream:
            self.showScream(y, x, self.h)