import pygame
import gegner
import freund

class GUIElement:
    def draw(self, screen):
        pass

    def update(self, delta_time):
        pass


class Button:
    def __init__(self, x, y, width, height, color, alpha=255, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color  # RGB
        self.alpha = alpha
        self.action = action

        # Transparente Surface
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.set_alpha(self.alpha)
        self.surface.set_alpha(self.alpha)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.surface.set_alpha(120)
        else:
            self.surface.set_alpha(self.alpha)


        # Surface leeren
        self.surface.fill((0, 0, 0, 0))

        # Button auf die Surface zeichnen
        pygame.draw.rect(self.surface, self.color, self.surface.get_rect())

        # Surface auf den Screen zeichnen
        screen.blit(self.surface, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                if self.action:
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
        self.elements = {"menu": [],"game": [], "loadingscreen": []}         
        self.state = screen_state         
        self.placing_friend = False           
        self.gegner_list = []       
    def set_state(self, state):         
        self.state = state     

    def add_game(self, element):
        self.elements["game"].append(element) 

    def add_menu(self, element):         
        self.elements["menu"].append(element)  

    def add_loadingscreen(self, element):         
        self.elements["loadingscreen"].append(element)    

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

class Text(GUIElement):     
    def __init__(self, x, y,text,font_size=24,color=(255, 255, 255),font_path=None,center=False):         
        self.x = x         
        self.y = y         
        self.text = text         
        self.color = color         
        self.center = center           
        self.font = pygame.font.Font(font_path, font_size)                  
        self.surface = self.font.render(self.text, True, self.color)         
        self.rect = self.surface.get_rect()           
        if self.center:             
            self.rect.center = (self.x, self.y)         
        else:             
            self.rect.topleft = (self.x, self.y)       

    def set_text(self, new_text):         
        self.text = new_text         
        self._render_text()       

    def set_color(self, new_color):         
        self.color = new_color         
        self._render_text()       

    def draw(self, screen):         
        screen.blit(self.surface, self.rect) 

# Klasse für Buttons mit Bildern, Haptik (Klick) und Hover-Effekt
class ImageButton:
    def __init__(self, x, y, width, height, image_path, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.image = None
        
        # Versuch das Bild zu laden und zu skalieren
        try:
            loaded_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (width, height))
        except Exception as e:
            print(f"Fehler beim Laden von {image_path}: {e}")
            # Fallback: Graues Rechteck, falls Bild fehlt
            self.image = pygame.Surface((width, height))
            self.image.fill((100, 100, 100))

    def draw(self, screen):
        # Positionen initialisieren
        draw_x = self.rect.x
        draw_y = self.rect.y
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        # Haptik: Wenn gedrückt, Button leicht verschieben
        if is_hovered and pygame.mouse.get_pressed()[0]:
            draw_x += 3
            draw_y += 3

        # 1. Das Bild zeichnen
        screen.blit(self.image, (draw_x, draw_y))

        # 2. Hover-Effekt ("Funkeln" / Aufleuchten)
        if is_hovered:
            # Erstelle eine weiße, halb-transparente Fläche
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 50)) # Weiß mit Transparenz (50 von 255)
            # Zeichne sie über den Button
            screen.blit(overlay, (draw_x, draw_y))
            
            # Optional: Rand hervorheben
            pygame.draw.rect(screen, (255, 255, 200), (draw_x, draw_y, self.rect.width, self.rect.height), 3)

    def handle_event(self, event):
        # Klick-Logik
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()