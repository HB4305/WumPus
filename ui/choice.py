import pygame
from ui.text import *
from ui.constants import *

class BackButton:
    def __init__(self, screen, btn_pos_x=40, btn_pos_y=SHOW_NOTI_HEIGHT, content='<-- back'):
        self.screen = screen
        self.is_click_back = False
        self.back_btn_sprite = None
        
        text_obj = Text_Display(content)
        text_content = text_obj.show_text()
        text_pos = (btn_pos_x, btn_pos_y)
        
        self.back_btn_sprite = text_obj.get_text_position()
        self.back_btn_sprite.x = btn_pos_x
        self.back_btn_sprite.y = btn_pos_y
        
        self.screen.blit(text_content, text_pos)
        
        
    def get_back_button_rect(self):
        return self.back_btn_sprite
    
    def back_to(self, is_click=False, option=None, current=None):
        self.is_click_back = is_click
        if self.is_click_back:
            self.is_click_back = False
            return option
        return current
    
class NextButton:
    def __init__(self, screen, btn_pos_x=1180, btn_pos_y=SHOW_NOTI_HEIGHT, content='next -->'):
        self.screen = screen
        self.is_click_next = False
        self.next_btn_sprite = None
        
        text_obj = Text_Display(content)
        text_content = text_obj.show_text()
        text_pos = (btn_pos_x, btn_pos_y)
        
        self.next_btn_sprite = text_obj.get_text_position()
        self.next_btn_sprite.x = btn_pos_x
        self.next_btn_sprite.y = btn_pos_y
        
        self.screen.blit(text_content, text_pos)
    
    def next_to(self, is_click=False, option=None, current=None):
        self.is_click_next = is_click
        if self.is_click_next:
            self.is_click_next = False
            return option
        return current

class ChoiceList:
    def __init__(self, screen):
        self.screen = screen
        
    def choose_options(self, choice_list, is_up, is_down, letter_spacing=100):
        min_arrow_pox_x = 10e5
        current_index_active = None
        
        for i, element in enumerate(choice_list):
                
            text_obj = Text_Display(element[1])
            text_content = text_obj.show_text()
            text_pos = text_obj.center_text(height=letter_spacing + i * 300)
            x_text, y_text = text_pos[0], text_pos[1]
            
            arrow_img = pygame.image.load('ui/assets/arrow.png')
            img_width = arrow_img.get_width()
            arrow_pos_x = x_text - img_width - 50
            min_arrow_pox_x = min(arrow_pos_x, min_arrow_pox_x)
            
            if element[0]:
                text_content = text_obj.show_text(color=ACTIVE_CHOICE_COLOR)
                current_index_active = i
                self.screen.blit(arrow_img, (min_arrow_pox_x, y_text + 8))
            
            self.screen.blit(text_content, text_pos)    
            
        # Key input
        menu_choice_lenth = len(choice_list)
            
        if is_down:
            is_down = False
            next_index = current_index_active + 1
            if next_index >= menu_choice_lenth:
                next_index = 0
            choice_list[current_index_active][0] = False
            choice_list[next_index][0] = True
        if is_up:
            is_up = False
            prev_index = current_index_active - 1
            if prev_index < 0:
                prev_index = menu_choice_lenth - 1
            choice_list[current_index_active][0] = False
            choice_list[prev_index][0] = True

class Choice:
    def __init__(self, screen, choice, title_obj):
        self.screen = screen
        self.is_click_back = False
        self.is_click_next = False
        self.option_back_to = None
        self.option_next_to = None
        self.option_result = None
        self.choice_list = []
        for _ in range (len(choice)):
            if _ == 0:
                self.choice_list.append([True, choice[_]])
            else:
                self.choice_list.append([False, choice[_]])
        self.title_obj = title_obj
        self.background = pygame.image.load('ui/assets/menu_background.jpg')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def get_choice(self):
        for i, element in enumerate(self.choice_list):
            if element[0]:
                return i
        return 0
    
    def get_level(self):
        for _, element in enumerate(self.choice_list):
            if element[0]:
                return element
        return 0
    
    # def get_back_to(self):
    #     if self.is_click_back:
    #         self.is_click_back = False
    #         res = self.option_back_to
    #         self.option_back_to = None
    #         return res
    #     return 0
    
    # def get_next_to(self):
    #     if self.is_click_next:
    #         self.is_click_next = False
    #         res = self.option_next_to
    #         self.option_next_to = None
    #         return res
    #     return 0
    
    def get_back_to(self, des, curr):
        if self.is_click_back:
            self.is_click_back = False
            return des
        return curr
    
    def get_next_to(self, des, curr):
        if self.is_click_next:
            self.is_click_next = False
            return des
        return curr
    
    def get_option_result(self):
        res = self.option_result
        self.option_result = None
        return res
    
    def display_option(self, is_up, is_down, is_left, is_right, is_enter, can_back=True, can_next=True):
        self.screen.blit(self.background, (0, 0))
        height=100
        if self.title_obj != '':
            title_obj = Text_Display(self.title_obj, font_size=FONT_LARGE)
            title = title_obj.show_text()
            title_pos = title_obj.center_text(height=height)
            self.screen.blit(title, title_pos)
            height = WINDOW_HEIGHT
        
        if self.title_obj == '':
            # back_button = BackButton(self.screen)
            # next_button = NextButton(self.screen)
            
            if can_back:
                BackButton(self.screen)
            if can_next:
                NextButton(self.screen)
            
            if is_left:
                is_left = False
                self.is_click_back = True
                # self.option_back_to = back_button.back_to(self.is_click_back, None, 0)
            elif is_right:
                is_right = False
                self.is_click_next = True
                # self.option_next_to = next_button.next_to(self.is_click_next, -1, 0)
        if is_enter:
            is_enter = False
            self.option_result = self.get_choice()
        
        choice_list = ChoiceList(self.screen)
        choice_list.choose_options(self.choice_list, is_up, is_down, height)
        
    def show_choice_list(self, is_up, is_down, is_left, is_enter):
        self.screen.fill(BACKGROUND_COLOR)
        
        back_button = BackButton(self.screen)
        
        text_obj = Text_Display('Choose the level', font_size=FONT_LARGE)
        text_content = text_obj.show_text()
        text_pos = text_obj.center_text(height=100)
        
        self.screen.blit(text_content, text_pos)
        
        if is_left:
            is_left = False
            self.is_click_back = True
            self.option_back_to = back_button.back_to(self.is_click_back, None, 0)
        if is_enter:
            is_enter = False
            self.option_result = self.get_choice()
            return self.get_choice()
                
        choice_list = ChoiceList(self.screen)
        choice_list.choose_options(self.choice_list, is_up, is_down, 500)
        