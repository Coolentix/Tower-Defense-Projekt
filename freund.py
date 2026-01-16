import pygame

class Freund:
    def __init__(self, screen, row, col, position, pos_gegner):
        self.schaden = 0
        self.rasse = ""
        self.reichweite = 0
        self.angriffs_geschwindigkeit = 0.5
        self.row, self.col = row, col
        self.screen = screen
        self.pos_gegner = pos_gegner

       # if self.pos_gegner:
       #     self.pos_gegner_x, self.pos_gegner_y = pos_gegner

        # Pixelposition (wird später gesetzt)
        self.x , self.y = position
        self.letzter_schuss = 0
        self.projektile = []

    def update(self, dt):
        dt = dt / 1000  # Sekunden
        # Prüfen, ob genug Zeit vergangen ist, um einen neuen Schuss abzufeuern
        self.letzter_schuss += dt
        if self.letzter_schuss >= self.angriffs_geschwindigkeit:
            self.letzter_schuss = 0
            self.schuß()

        # Projektile aktualisieren
        for p in self.projektile:
            p.update(dt)
            p.draw(self.screen)

    def schuß(self):
        p = Projektil(self.x, self.y,self.pos_gegner)
        self.projektile.append(p)

class Projektil(pygame.sprite.Sprite):
    def __init__(self,x,y,gegner):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 15)
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 5
        self.pos = pygame.math.Vector2(self.rect.center)
        if gegner:
            self.ziel_x, self.ziel_y = gegner
            self.target = pygame.math.Vector2(self.ziel_x, self.ziel_y)
        else:
            self.target = pygame.math.Vector2(5,5)

    def update(self,delta_time):
        delta_time = delta_time*1000
        # Ziel erreicht?
        direction = self.target - self.pos
        distance = direction.length()

        if distance == 0:
            self.kill()
            return

        # Reicht die Bewegung dieses Frames aus?
        step = self.speed * delta_time

        if distance <= step:
            self.pos = self.target
            self.rect.center = self.pos
            self.kill()  # oder: Ziel erreicht
        else:
            direction = direction.normalize()
            self.pos += direction * step
            self.rect.center = self.pos

    def draw(self,screen):
        screen.blit(self.image, self.rect)

