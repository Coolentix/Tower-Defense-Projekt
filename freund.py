import pygame

class Freund:
    def __init__(self, screen, row, col, position):
        self.schaden = 0
        self.rasse = ""
        self.reichweite = 0
        self.angriffs_geschwindigkeit = 500
        self.row, self.col = row, col
        self.screen = screen

        # Pixelposition (wird später gesetzt)
        self.x , self.y = position
        self.letzter_schuss = 0
        self.projektile = []

    def update(self, dt):
        # Prüfen, ob genug Zeit vergangen ist, um einen neuen Schuss abzufeuern
        self.letzter_schuss += dt
        if self.letzter_schuss >= self.angriffs_geschwindigkeit:
            self.letzter_schuss = 0
            self.schuß()

        # Projektile aktualisieren
        for p in self.projektile:
            p.update()
            p.draw(self.screen)

    def schuß(self):
        p = Projektil(self.x, self.y)
        self.projektile.append(p)

class Projektil:
    def __init__(self,x,y):
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 15)
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.speed

    def draw(self,screen):
        screen.blit(self.image, self.rect)

