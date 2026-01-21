import pygame
import math

class Freund:
    def __init__(self, row, col, position):
        self.row = row
        self.col = col
        self.pos = pygame.math.Vector2(position)

        self.freund_type = freund_type
        self.freund_Stats = freund_type.freund_Stats[freund_type]

        self.range = self.freund_Stats["range"]//2
        self.fire_rate = self.freund_Stats["fire_rate"]
        self.damage = self.freund_Stats["damage"]
        self.kosten = self.freund_Stats["kosten"]

        self.target = None
        self.projectiles = []

    def update(self, dt, gegner_liste):
        self.timer += dt

        # Ziel suchen, falls keins da ist oder tot
        if not self.target or not self.target.alive:
            self.target = self.find_target(gegner_liste)

        # Schießen
        if self.target and self.timer >= self.fire_rate:
            self.timer = 0
            self.shoot()

        # Projektile updaten
        for p in self.projectiles[:]:
            p.update(dt)
            if not p.alive:
                self.projectiles.remove(p)

    def find_target(self, gegner_liste):
        for g in gegner_liste:
            if not g.alive:
                continue
            if self.pos.distance_to(g.rect.center) <= self.range:
                return g
        return None

    def shoot(self):
        p = Projektil(self.pos.x, self.pos.y, self.target)
        self.projectiles.append(p)

    def draw(self,screen):
        pygame.draw.circle(screen, (50, 200, 50), self.pos, 15)
        pygame.draw.circle(screen, (50, 100, 50), self.pos, self.range, 1)

        for p in self.projectiles:
            p.draw(screen)

class Projektil:
    def __init__(self, x, y, ziel_gegner):
        self.pos = pygame.math.Vector2(x, y)
        self.ziel = ziel_gegner      # Gegner-OBJEKT, keine Position
        self.speed = 5             # Pixel pro Sekunde
        self.radius = 10
        self.alive = True

    def update(self, dt):
        if not self.ziel or not self.ziel.alive:
            self.alive = False
            return

        ziel_pos = pygame.math.Vector2(self.ziel.rect.center)
        richtung = ziel_pos - self.pos

        if richtung.length() < 5:    # Treffer
            #self.ziel.take_damage(1)
            self.alive = False
            return

        richtung = richtung.normalize()
        self.pos += richtung * self.speed * dt

class freund_type:
    SNIPER = 0
    MAGIER = 1
    SPAMMER = 2
    DEFAULT = 3

    Freund_Stats = {
        SNIPER: {"range": 750, "damage": 2, "fire_rate": 200, "kosten": 400},
        MAGIER: {"range": 400, "damage": 4, "fire_rate": 100, "kosten": 700},
        SPAMMER: {"range": 200, "damage": 1, "fire_rate": 1, "kosten": 600},
        DEFAULT: {"range": 250, "damage": 1, "fire_rate": 100, "kosten": 100}
    }
    def draw(self,screen):
        pygame.draw.circle(screen, (255, 50, 50), self.pos, self.radius)

