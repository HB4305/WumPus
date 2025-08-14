import pygame
from ui.constants import *
from ui.image import showGameBackground

# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/

class Text_Display:
    def __init__(self, content='', font_type=FONT_TYPE, font_size=FONT_MEDIUM, text_color=PINK_COLOR):
        self.content = content
        self.font_type = font_type
        self.font_size = font_size
        self.text_color = text_color
        self.text_content = ''
        self.font = pygame.font.Font(font_type, font_size)
        
    def get_text_position(self):
        text_position = self.text_content.get_rect()
        return text_position
    
    def show_text(self, color=None):
        if color is None:
            color = self.text_color
        self.text_content = self.font.render(self.content, True, color)
        return self.text_content
    
    def center_text(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        text_rect = self.text_content.get_rect(center=(width / 2, height / 2))
        return text_rect
    
    def write_text_content(self, content='', pos_x=0, pos_y=0, text_color=PINK_COLOR, font_size=FONT_MEDIUM, is_center=False, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        text_obj = Text_Display(content, font_size=font_size, text_color=text_color)
        text_content = text_obj.show_text()
        text_pos = (pos_x, pos_y)
        if is_center:
            text_pos = text_obj.center_text(width, height)
        self.screen.blit(text_content, text_pos)
        

class Info(Text_Display):
    ###3
    def __init__(self, screen, level): # cái đối số agent tao xóa bỏ
        super().__init__()
        self.screen = screen
        self.left_margin = 850
        self.level_background = level
        # self.agent = agent 
    
    def reShowLeftBar(self):
        area = (self.left_margin-20, 0, WINDOW_WIDTH-(self.left_margin-20), WINDOW_HEIGHT)
        showGameBackground(self.screen, area, self.level_background)
    
    def showMapInfo(self, map_size):
        map_title = f"Map {map_size}x{map_size}"
        self.write_text_content(map_title, self.left_margin, 50, text_color=DARK_RED_COLOR)
        
    def showScore(self, score=0):
        ###
        # score = self.agent.point
        ####
        self.write_text_content("Score: ", self.left_margin, 100, text_color=DARK_RED_COLOR)
        self.write_text_content(f"{score}", self.left_margin+170, 100, text_color=DARK_RED_COLOR)

    def showLeftBar(self, choose_map_result, score=0):
        area = (self.left_margin-20, 0, WINDOW_WIDTH-(self.left_margin-20), SHOW_NOTI_HEIGHT)
        showGameBackground(self.screen, area)
        self.showMapInfo(choose_map_result)
        self.showScore(score)