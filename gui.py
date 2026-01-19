import pygame
import gegner
import freund

class Button:
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


class Checkbox:
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
                self.state = 1 - self.state  # Toggle
                self.action(self.state)

class GUIManager:     
    def __init__(self,screen_state):         
        self.elements = {"menu": [],"game": []}         
        self.state = screen_state         
        self.placing_friend = False           
        self.gegner_list = []       
        def set_state(self, state):         
            self.state = state     

        def add_game(self, element):
            self.elements["game"].append(element) 

        def add_menu(self, element):         
            self.elements["menu"].append(element)      

        def draw(self, screen):         
            for e in self.elements.get(self.state, []):             
                if hasattr(e, "draw"):              
                    #Fragt ab ob eine draw funktion existiert                
                    e.draw(screen)     

        def update(self,delta_time):         
            for e in self.elements.get("game",[]):             
                if isinstance(e, gegner.Gegner):                 
                    self.gegner_list.append(e)           
            for e in self.elements.get(self.state, []):             
                if hasattr(e, "update"):              
                            #Fragt ab ob eine update funktion existiert                 
                    if isinstance(e, freund.Freund):                     
                            e.update(delta_time,self.gegner_list)                 
                    elif isinstance(e, gegner.Gegner) and not e.update(delta_time):                     
                            self.gegner_list.remove(e)                     
                            self.elements["game"].remove(e)                 
                else:                     
                    e.update(delta_time)     

        def handle_event(self, event):         
            for e in self.elements.get(self.state, []):             
                if hasattr(e, "handle_event"):                 
                    e.handle_event(event)