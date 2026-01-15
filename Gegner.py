import pygame

class Gegner(pygame.sprite.Sprite):
    def __init__(self, enemy_type, path):
        super().__init__()

        self.enemy_type = enemy_type
        self.Enemy_Stats = EnemyType.Enemy_Stats[enemy_type]

        self.speed = self.Enemy_Stats["speed"]
        self.hp = self.Enemy_Stats["health"]
        self.damage = self.Enemy_Stats["damage"]

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        # Pfad übernehmen
        self.path = path

    def update(self):
        if not self.path:
            self.kill()
            return

        target_x, target_y = self.path[0]
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance <= self.speed:
            self.rect.topleft = (target_x, target_y)
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
