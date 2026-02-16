import pygame

class Freund:
    def __init__(self,map, position, f_typ=0, image_path="../Tower-Defense-Projekt/bilder/Ameise.gif",game_speed=0.5):
        self.schaden = 0
        self.rasse = ""
        self.row, self.col = map.ROWS, map.COLS
        self.pos = pygame.math.Vector2(position)    #--> mittig machen
        self.size = (map.TILE_SIZE,map.TILE_SIZE)
        self.image_path = image_path

        self.freund_type = freund_type()
        self.freund_Stats = self.freund_type.freund_Stats[f_typ]

        self.range = self.freund_Stats["range"] //2
        self.fire_rate = self.freund_Stats["fire_rate"] // game_speed
        self.damage = self.freund_Stats["damage"]
        self.kosten = self.freund_Stats["kosten"]

        self.angle = 0

        self.target = None
        self.timer=0
        self.projectiles = pygame.sprite.Group()  

        # ---- Bild ----
        if isinstance(image_path, str):
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.size)
        else:
            # Fallback (sichtbar zum Debuggen)
            self.image = pygame.Surface(self.size, pygame.SRCALPHA)
            self.image.fill((0, 200, 0))

        self.new_angle_image = self.image
        self.rect = self.new_angle_image.get_rect(center=self.pos)

    def update(self, dt, gegner_liste):
        # Timer hochzählen
        self.timer += dt

        # ---- Ziel prüfen ----
        if self.target:
            # Gegner tot → Ziel freigeben
            if not self.target.alive():
                self.target = None
            # Gegner außerhalb der Reichweite → Ziel freigeben
            elif pygame.math.Vector2(self.rect.center).distance_to(
                self.target.rect.center) > self.range:
                self.target = None

        # ---- Neues Ziel suchen ----
        if not self.target:
            self.target = self.find_target(gegner_liste)

        # ---- Schießen ----
        if self.target and self.timer >= self.fire_rate:
            self.shoot()
            self.timer = 0

        # ---- Projectiles updaten ----
        for p in self.projectiles.sprites():
            p.update(dt)
            if not p.alive():
                self.projectiles.kill(p)

    def find_target(self, gegner_liste):
        turm_pos = pygame.math.Vector2(self.rect.center)
        for g in gegner_liste:
            if not g.alive():
                continue
            if turm_pos.distance_to(g.rect.center) <= self.range:
                return g
        return None

    def shoot(self):
        start_pos = pygame.math.Vector2(self.pos)
        ziel_pos = pygame.math.Vector2(self.target.get_aim_point())

        self.angle = (ziel_pos - start_pos).angle_to(pygame.math.Vector2(1, 0))
        self.new_angle_image = pygame.transform.rotate(self.image, self.angle-90)
        self.rect = self.new_angle_image.get_rect(center=self.pos)

        richtung = (ziel_pos - start_pos).normalize()

        p = Projektil(self.rect.center, richtung, ziel_pos)
        self.projectiles.add(p)

    def draw(self,screen):
        #pygame.draw.circle(screen, (50, 200, 50), self.pos, 15)
        pygame.draw.circle(screen, (50, 100, 50), self.rect.center, self.range, 1)
        screen.blit(self.new_angle_image, self.rect)

        for p in self.projectiles:
            p.draw(screen)

    def projectiles_return(self):
        return self.projectiles

class Projektil(pygame.sprite.Sprite):
    def __init__(self, pos, richtung, gegner):
        super().__init__()

        self.pos = pygame.math.Vector2(pos)
        self.richtung = pygame.math.Vector2(richtung)
        if self.richtung.length_squared() != 0:
            self.richtung = self.richtung.normalize()
        self.gegner = pygame.math.Vector2(gegner)

        self.speed = 5      # Pixel pro Sekunde
        self.radius = 5

        # image + rect sind Pflicht
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 50, 50), (5, 5), self.radius)
        self.rect = self.image.get_rect(center=pos)

        self.rect = self.image.get_rect(center=self.pos)
        self.angle = (self.gegner - self.pos).angle_to(pygame.math.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.image, self.angle-90)


    def update(self, dt):
        self.pos += self.richtung * self.speed * dt
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 50, 50), self.pos, self.radius)

    def die(self):
        self.kill()

class freund_type:
    SNIPER = 0
    MAGIER = 1
    SPAMMER = 2
    DEFAULT = 3
    def __init__(self):
        print("Hallo")
        
        self.freund_Stats = {
            0: {"range": 750, "damage": 2, "fire_rate": 200, "kosten": 400},
            1: {"range": 400, "damage": 4, "fire_rate": 100, "kosten": 700},
            2: {"range": 200, "damage": 1, "fire_rate": 50, "kosten": 600},
            3: {"range": 250, "damage": 1, "fire_rate": 100, "kosten": 100}
        }
    def draw(self,screen):
        pygame.draw.circle(screen, (255, 50, 50), self.pos, self.radius)

