import pygame

class Freund:
    def __init__(self,map, position, image_path="../Tower-Defense-Projekt/bilder/Ameise.gif"):
        self.schaden = 0
        self.rasse = ""
        self.row, self.col = map.ROWS, map.COLS
        self.pos = pygame.math.Vector2(position)
        self.size = (map.TILE_SIZE,map.TILE_SIZE)
        self.image_path = image_path

        self.range = 250
        self.fire_rate = 500     # ms
        self.timer = 0

        self.target = None
        self.projectiles = []

        # ---- Bild ----
        if isinstance(image_path, str):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.size)
            print("bild wird gesetzt")
        else:
            # Fallback (sichtbar zum Debuggen)
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            self.image.fill((0, 200, 0))

        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt, gegner_liste):
        self.timer += dt

        if not self.target or not self.target.alive:
            self.target = self.find_target(gegner_liste)

        if self.target and self.timer >= self.fire_rate:
            self.shoot()
            self.timer = 0

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
        #pygame.draw.circle(screen, (50, 200, 50), self.pos, 15)
        pygame.draw.circle(screen, (50, 100, 50), self.pos, self.range, 1)
        screen.blit(self.image, self.rect)

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

