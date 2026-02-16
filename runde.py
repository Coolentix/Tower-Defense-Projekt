import gegner

class RundenManager:
    def __init__(self, runden_nummer):
        self.delay_dict = {
            gegner.EnemyType.WALKER: 500,
            gegner.EnemyType.RUNNER: 300,
            gegner.EnemyType.TANK: 1500
        }

        self.runde = GreenFN(runden_nummer)
        self.timer = 0
        self.spawn_index = 0

    def update(self, dt):
        self.timer += dt

        if self.spawn_index >= len(self.runde.enemies):
            return None

        enemy_type = self.runde.enemies[self.spawn_index]
        delay = self.delay_dict[enemy_type]

        if self.timer >= delay:
            self.timer = 0.0
            self.spawn_index += 1
            return enemy_type

        return None

class GreenFN:
    """
    Reines Datenobjekt für Runden/Wellen.
    Enthält nur die Reihenfolge der Gegner.
    """

    RUNDEN = {
        1: [
            gegner.EnemyType.WALKER,
            gegner.EnemyType.WALKER,
            gegner.EnemyType.WALKER,
            gegner.EnemyType.WALKER,
        ],

        2: [
            gegner.EnemyType.WALKER,
            gegner.EnemyType.RUNNER,
            gegner.EnemyType.WALKER,
            gegner.EnemyType.RUNNER,
        ],
    }

    def __init__(self, nummer: int):
        if nummer not in GreenFN.RUNDEN:
            raise ValueError(f"Unbekannte Runde: {nummer}")

        self.nummer = nummer
        self.enemies = list(GreenFN.RUNDEN[nummer])