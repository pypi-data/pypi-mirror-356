import pygame
import sys
import os

class Color:
    @staticmethod
    def rgb(r, g, b):
        return (r, g, b)
    
    @staticmethod
    def rgba(r, g, b, a):
        return (r, g, b, a)

class Text:
    def __init__(self, content, color, x, y, size=24):
        self.content = content
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.font = None

class Image:
    def __init__(self, path, width, height, x, y):
        self.path = path
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.surface = None
class Button:
    def __init__(self, text, color, bg_color, x, y, width, height, size=24, hover_color=None):
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.hover_color = hover_color if hover_color else bg_color
        self.current_color = bg_color
        self.font = None
        self.callback = None
        self.rect = pygame.Rect(x, y, width, height)
        
    def set_callback(self, callback):
        self.callback = callback
class New:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.title = "RenderPy Window"
        self.bg_color = Color.rgb(240, 240, 240)
        self.screen = None
        self.elements = []
        self.buttons = []
        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 60
        
    def configure(self, width=None, height=None, title=None, bg_color=None, fps=None):
        if width: self.width = width
        if height: self.height = height
        if title: self.title = title
        if bg_color: self.bg_color = bg_color
        if fps: self.fps = fps
        
    def render(self, element):
        if isinstance(element, Text):
            if not element.font:
                element.font = pygame.font.SysFont('Arial', element.size)
            self.elements.append(element)
        elif isinstance(element, Image):
            if not element.surface:
                try:
                    img = pygame.image.load(element.path)
                    element.surface = pygame.transform.scale(img, (element.width, element.height))
                except:
                    print(f"Error loading image: {element.path}")
                    return
            self.elements.append(element)
        elif isinstance(element, Button):
            if not element.font:
                element.font = pygame.font.SysFont('Arial', element.size)
            self.buttons.append(element)
        
    def mainloop(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.running = True
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Обработка кликов по кнопкам
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        for button in self.buttons:
                            if button.rect.collidepoint(mouse_pos) and button.callback:
                                button.callback()
            
            # Отрисовка фона
            self.screen.fill(self.bg_color)
            
            # Отрисовка элементов
            for element in self.elements:
                if isinstance(element, Text):
                    text_surface = element.font.render(element.content, True, element.color)
                    self.screen.blit(text_surface, (element.x, element.y))
                elif isinstance(element, Image) and element.surface:
                    self.screen.blit(element.surface, (element.x, element.y))
            
            # Отрисовка кнопок
            for button in self.buttons:
                # Проверка наведения мыши
                if button.rect.collidepoint(mouse_pos):
                    button.current_color = button.hover_color
                else:
                    button.current_color = button.bg_color
                
                # Рисуем прямоугольник кнопки
                pygame.draw.rect(self.screen, button.current_color, button.rect)
                
                # Рисуем текст кнопки
                text_surface = button.font.render(button.text, True, button.color)
                text_rect = text_surface.get_rect(center=button.rect.center)
                self.screen.blit(text_surface, text_rect)
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()