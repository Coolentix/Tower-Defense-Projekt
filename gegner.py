import pygame

class Gegner(pygame.sprite.Sprite):
    def __init__(self, enemy_type, map, path, image_path=None):
        super().__init__() # Greife auf EnemyType zu

        self.enemy_type = enemy_type
        self.Enemy_Stats = EnemyType.Enemy_Stats[enemy_type]

        self.speed = self.Enemy_Stats["speed"] //2
        self.hp = self.Enemy_Stats["health"]
        self.damage = self.Enemy_Stats["damage"]

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 0))

        self.ROWS = map.ROWS                                      #Zeilen
        self.COLS = map.COLS                                    #Spalten
        self.screen_x = map.screen_x 
        self.screen_y = map.screen_y          #Bildschirm göße errechnen
        self.start_x = map.start_x                                   #Verschiebung X
        self.start_y = map.start_y

        self.path = path  # Liste der Wegpunkte
        self.path = path.copy()
        self.TILE_SIZE = (self.screen_y-20)//self.ROWS
        spawn_x, spawn_y = self.path.pop(0)

        self.rect = self.image.get_rect(
        center=(
        self.start_x + spawn_y * self.TILE_SIZE + self.TILE_SIZE // 2,  # horizontal Mitte des Tiles
        self.start_y + spawn_x * self.TILE_SIZE + self.TILE_SIZE // 2   # vertikal Mitte des Tiles
        ))

        #self.image = pygame.image.load("/Users/wilson/Downloads/pixil-frame-0.png").convert_alpha()
        # Optional: auf die Tile-Größe skalieren
        self.image = pygame.transform.scale(self.image, (self.TILE_SIZE, self.TILE_SIZE))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self,delta_time):
        if not self.path:
            self.kill()  # Entferne den Gegner, wenn der Pfad beendet ist
            return False
        
        # Aktuelles Ziel         
        row, col = self.path[0]
        target = pygame.math.Vector2(
        self.start_x + col * self.TILE_SIZE + self.TILE_SIZE // 2,
        self.start_y + row * self.TILE_SIZE + self.TILE_SIZE // 2
        )

        # Aktuelle Position (als Vector2!)
        position = pygame.math.Vector2(self.rect.center)
        
        # Richtungsvektor zum Ziel
        direction = target - position
        distance = direction.length()

        if distance == 0:             
            self.path.pop(0)             
            return

        # Ziel in diesem Frame erreichbar?
        if distance <= self.speed * delta_time:
            self.rect.center = target
            self.path.pop(0)
        else:
            # Normieren + Bewegung
            direction = direction.normalize()
            position += direction * self.speed * delta_time
            self.rect.center = position
        return True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class EnemyType:
    WALKER = 0
    RUNNER = 1
    TANK = 2

    Enemy_Stats = {
        WALKER: {"health": 10, "speed": 2, "damage": 10},
        RUNNER: {"health": 7, "speed": 4, "damage": 8},
        TANK: {"health": 20, "speed": 1, "damage": 20},
    }

    #Enemy_images = {
        #WALKER: /Users/wilson/Downloads/pixilart-drawing.png
       # RUNNER: "runner_image_path.png",
        #TANK: "tank_image_path.png",
