import pygame

class GUI:
    def __init__(self):
        pass

class Button:
    def __init__(self):
        pass
    def draw(self):
        pass

#Funktioniert Nicht
class Checkbox:
    def __init__(self):
        self.pressed = False
        self.checked = False

    def draw(self,screen,pos_x,pos_y,size_x,size_y,color):
        pygame.draw.rect(screen, (color), ((pos_x,pos_y),(size_x,size_y)),1) #zeichnet viereck

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pos_x <= mouse_x <= pos_x + size_x and pos_y <= mouse_y <= pos_y + size_y:
            if pygame.mouse.get_pressed()[0] == 0 and self.checked == False:
                self.checked = True
                print("check")
        if pygame.mouse.get_pressed()[0] == 0 and self.checked == True:
            self.checked = False

        if self.checked:
            pygame.draw.rect(screen, (color), ((pos_x+size_x//2,pos_y+size_y//2),(size_x//2,size_y//2)),1) #zeichnet viereck