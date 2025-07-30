import pygame
from ui.constants import *
from ui.text import *
from ui.image import *
from ui.choice import BackButton

class Credit:
    def __init__(self, screen):
        self.screen = screen
        self.back_btn_sprite = None
        self.is_click_back = False
        self.option_back_to = None
    
    def write_text_content(self, font_size=FONT_MEDIUM, is_center=False, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, pos_x=0, pos_y=0, content=''):
        text_obj = Text_Display(content, font_size=font_size)
        text_content = text_obj.show_text()
        text_pos = (pos_x, pos_y)
        
        if is_center:
            text_pos = text_obj.center_text(width, height)
        
        self.screen.blit(text_content, text_pos)
        
    def get_back_to(self):
        if self.is_click_back:
            self.is_click_back = False
            res = self.option_back_to
            self.option_back_to = None
            return res
        return 1
            
    def display_credit(self, is_left):
        showMenuBackground(self.screen)
        
        back_button = BackButton(self.screen)
        # back_button_rect = back_button.get_back_button_rect()
        
        text_obj = Text_Display('credit', font_size=FONT_LARGE)
        text_content = text_obj.show_text()
        text_pos = text_obj.center_text(height=100)
        
        self.screen.blit(text_content, text_pos)
        
        self.write_text_content(content='22127174 - Ngo van Khai', is_center=True, height=500)
        self.write_text_content(content='22127322 - Le Phuoc Phat', is_center=True, height=700)
        self.write_text_content(content='22127388 - To Quoc Thanh', is_center=True, height=900)
        self.write_text_content(content='22127441 - Thai Huyen Tung', is_center=True, height=1100)
        
        if is_left:
            is_left = False
            self.is_click_back = True
            self.option_back_to = back_button.back_to(self.is_click_back, None, 1)
                    
                
        
    