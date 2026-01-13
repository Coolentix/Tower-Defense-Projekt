import pygame

class GUIElement:
    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass

class Button(GUIElement):
    def __init__(self, x, y, width, height, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = (150, 0, 0) if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

#Funktioniert Nicht
class Checkbox(GUIElement):
    def __init__(self, x, y, width, height, color,state,action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.state = state
        self.action = action

    def draw(self,screen):
        if self.state == 0:
            pygame.draw.rect(screen, self.color, self.rect,2) #zeichnet viereck
        if self.state == 1:
            pygame.draw.rect(screen, self.color, self.rect,2) #zeichnet viereck
            pygame.draw.rect(screen, self.color, (self.rect.x + 4, self.rect.y + 4, self.rect.width-8, self.rect.height-8))

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state  # Toggle
                self.action(self.state)


class GUIManager:
    def __init__(self):
        self.elements = {"menu": [],"game": []}

    def add_game(self, element):
        self.elements["game"].append(element)
    
    def add_menu(self, element):
        self.elements["menu"].append(element)

    def draw(self, screen, state):
        for e in self.elements.get(state, []):
            e.draw(screen)

    def handle_event(self, event, state):
        for e in self.elements.get(state, []):
            e.handle_event(event)