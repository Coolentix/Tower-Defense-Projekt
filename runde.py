import gegner
import main

class RundenManager:
    def __init__(self, runden_nummer):
        delay_dict = {
            gegner.EnemyType.WALKER: 100,
            gegner.EnemyType.RUNNER: 50,
            gegner.EnemyType.TANK: 200
        }

        self.runde = Runde(runden_nummer, delay_dict)
        self.timer = 0
        self.spawn_index = 0

    def update(self, dt, gegner_liste):
        self.timer += dt

        if self.spawn_index < len(self.runde.runde):
            enemy_type, spawn_time = self.runde.runde[self.spawn_index]

            if self.timer >= spawn_time:
                main.Spiel.spawn_enemy(enemy_type)
                self.spawn_index += 1


class Runden:
    Runden = {
        1: [
            (gegner.EnemyType.WALKER, 0),
            (gegner.EnemyType.WALKER, 0),
            (gegner.EnemyType.WALKER, 0),
            (gegner.EnemyType.WALKER, 0),
        ]
    }

    def __init__(self, nummer, delay_dict=None):
        """
        delay_dict: Dictionary mit {EnemyType: spawn_delay_ms}
        """
        self.nummer = nummer
        self.runde = Runde.Runden.get(nummer, [])
        if delay_dict:
            self.setze_spawn_delay_pro_typ(delay_dict)

    def setze_spawn_delay_pro_typ(self, delay_dict):
        """
        Setzt die Spawnzeiten der Gegner basierend auf ihrem Typ.
        delay_dict = {EnemyType.WALKER: 100, EnemyType.RUNNER: 50}
        """
        letzte_zeit_typ = {}  # Merkt die letzte Spawnzeit pro Typ
        neue_runde = []

        for enemy_type, _ in self.runde:
            delay = delay_dict.get(enemy_type, 100)  # Default 100ms
            start_time = letzte_zeit_typ.get(enemy_type, 0)
            neue_runde.append((enemy_type, start_time))
            letzte_zeit_typ[enemy_type] = start_time + delay

        self.runde = neue_runde