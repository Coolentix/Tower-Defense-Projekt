import pygame

class Freund:
    def __init__(self):
        self.schaden = 0
        self.rasse = ""
        self.reichweite = 0
        self.angriffs_geschwindigkeit = 0

class Projektil:
    def __init__(self,freund):
        self.freund = freund
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 15)
        self.rect = self.image.get_rect(center=(200, 150))

    def draw(self,screen):
        self.rect.x += 10
        screen.blit(self.image, self.rect)

