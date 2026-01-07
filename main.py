import pygame
import karte 
import gui

class Spiel:
    def __init__(self):
        self.tilemap = karte.TileMap()        # Kartenobjekt erzeugen
        self.checkbox = gui.Checkbox()
        self.button = gui.Button()

    def main_loop(self):
               
        # pygame setup
        pygame.init()

        title = pygame.display.set_caption("Tower Defense")
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        clock = pygame.time.Clock()

        running = True

        while running:
            # Ereignisse abfragen
            # Das pygame.QUIT-Event wird ausgelöst, wenn der Benutzer das Fenster über das Schließen-Symbol (X) beendet.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Den Bildschirm mit einer Farbe füllen, um alles aus dem letzten Frame zu löschen.
            screen.fill("white")
 
            # HIER DAS SPIEL RENDERN
            self.tilemap.draw_tilemap(screen)
            self.tilemap.tile_clicked(screen)

            self.checkbox.draw(screen, 1010,10,20,20,(0,0,0)) #Grid Checkbox

            # Das Display mit flip() aktualisieren, um das Gezeichnete auf dem Bildschirm anzuzeigen.
            pygame.display.flip()

            clock.tick(60)  # limitiert FPS auf 60

        pygame.quit()

# Hier die Klassen
# jeweils in einzählne Dateien für übersichtlichkeit?

class Gegner:
    def __init__(self):
        leben = 0
        schaden = 0
        
    def wegsuche(self):
        pass

class Freunde:
    def __init__(self):
        schaden = 0
        rasse = ""
        reichweite = 0
        angriffs_geschwindigkeit = 0

class Projektil:
    pass

class Kauf:
    pass

class Spiel_Attribute:
    def __init__(self):
        geld = 0
        leben = 0
        score = 0
        zeit = 0

spiel = Spiel()
spiel.main_loop()