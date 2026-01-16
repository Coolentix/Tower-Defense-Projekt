import pygame

class Gegner(pygame.sprite.Sprite):
    def __init__(self, enemy_type, path, screen_size, image_path=None):
        super().__init__() # Greife auf EnemyType zu

        self.enemy_type = enemy_type
        self.Enemy_Stats = EnemyType.Enemy_Stats[enemy_type]

        self.speed = self.Enemy_Stats["speed"]
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

        self.ROWS = 10                                      #Zeilen
        self.COLS = 14                                    #Spalten
        self.screen_x, self.screen_y = screen_size
        self.start_x = 10                                   #Verschiebung X
        self.start_y = 10     

        self.path = [(1,0), (1, 1), (1, 2), (1, 3), (1, 4),(1,5),(1,6),(1,7),(1,8),(1,9),(2,9),(3,9),(3,8),(3,7),(3,6),(3,5),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4)]  # Liste der Wegpunkte
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
            self.kill()
            return

        target_x, target_y = self.path[0]
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance <= self.speed:
            self.rect.center = (target_x, target_y)
            self.path.pop(0)
        else:
            self.rect.x += self.speed * dx / distance
            self.rect.y += self.speed * dy / distance

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
