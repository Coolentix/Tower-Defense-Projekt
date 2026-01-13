import pygame

class Gegner(pygame.sprite.Sprite):
    def __init__(self, EnemyType, weg):
        super().__init__()

        self.EnemyType = EnemyType
        stats = EnemyType.Enemy_Stats[EnemyType]

        self.speed = stats["speed"]
        self.hp = stats["health"]
        self.damage = stats["damage"]  

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Rotes Quadrat als Platzhalter
        self.weg = []  # Liste der Wegpunkte
 
    def update(self):

        if not self.weg:
            player.leben -= self.damage  # Schaden am Spieler zufügen
            self.kill()  # Entfernt das Sprite, wenn kein Weg mehr da ist
            
        else:

            target_x, target_y = self.weg[0]
            direction_x = target_x - self.rect.x
            direction_y = target_y - self.rect.y
            distance = (direction_x**2 + direction_y**2) ** 0.5

            if distance < self.speed:
                self.rect.x = target_x
                self.rect.y = target_y
                self.weg.pop(0)
            else:
                self.rect.x += self.speed * direction_x / distance
                self.rect.y += self.speed * direction_y / distance
        

class EnemyType:
    WALKER = 0
    RUNNER = 1
    TANK = 2

    Enemy_Stats = {
        WALKER: {'health': 10, 'speed': 2, 'damage': 10},
        RUNNER: {'health': 7, 'speed': 4, 'damage': 8},
        TANK: {'health': 20, 'speed': 1, 'damage': 20},
    }
