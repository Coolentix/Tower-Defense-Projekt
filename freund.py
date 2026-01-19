import pygame
import math

class Freund:
    def __init__(self, row, col, position):
        self.row = row
        self.col = col
        self.pos = pygame.math.Vector2(position)

        self.range = 500
        self.fire_rate = 500     # Sekunden

        self.target = None
        self.projectiles = []

    def update(self, dt, gegner_liste):
        self.timer += dt

        # Ziel suchen, falls keins da ist oder tot
        if not self.target or not self.target.alive:
            self.target = self.find_target(gegner_liste)

        # Schießen
        if self.target and self.timer >= self.fire_rate:
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

    def draw(self,screen):
        pygame.draw.circle(screen, (255, 50, 50), self.pos, self.radius)

