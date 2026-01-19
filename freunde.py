import pygame
import math
import time

class Freunde:
    def __init__(self, x, y, schaden, reichweite, angriffs_geschwindigkeit):
        self.x = x
        self.y = y
        self.schaden = schaden
        self.reichweite = reichweite
        self.angriffs_geschwindigkeit = angriffs_geschwindigkeit  # Sekunden
        self.letzter_angriff = 0

    
    def gegner_in_reichweite(self, gegner):
        distanz = math.hypot(self.x - gegner.x, self.y - gegner.y)
        return distanz <= self.reichweite

    def schießen(self, gegner_liste):
            aktuelle_zeit = time.time()

            if aktuelle_zeit - self.letzter_angriff < self.angriffs_geschwindigkeit:
                return

            for gegner in gegner_liste:
                if self.gegner_in_reichweite(gegner):
                    gegner.leben -= self.schaden
                    self.letzter_angriff = aktuelle_zeit
                    break

