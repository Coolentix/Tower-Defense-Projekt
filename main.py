import pygame
import karte 
import gui

class Spiel:
    def __init__(self):
        self.checkbox = gui.Checkbox() #CHeckbox erzeugen

    def main_loop(self):
               
        # pygame setup
        pygame.init()

        title = pygame.display.set_caption("Tower Defense")
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.tilemap = karte.TileMap(screen.get_size())        # Kartenobjekt erzeugen (erst hier weil vorher screen size nicht bekannt)
        screen_x, screen_y = screen.get_size()

        clock = pygame.time.Clock()

        button = gui.Button(x=screen_x-50,y=0,width=50,height=50,color=(255, 0, 0),action=self.quit_game)

        running = True

        while running:
            # Ereignisse abfragen
            # Das pygame.QUIT-Event wird ausgelöst, wenn der Benutzer das Fenster über das Schließen-Symbol (X) beendet.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                button.handle_event(event)

            # Den Bildschirm mit einer Farbe füllen, um alles aus dem letzten Frame zu löschen.
            screen.fill("white")
 
            # HIER DAS SPIEL RENDERN
            self.tilemap.draw_tilemap(screen)

            button.draw(screen)

            #self.checkbox.draw(screen, 1010,10,20,20,(0,0,0)) #Grid ON/OFF Checkbox

            # Das Display mit flip() aktualisieren, um das Gezeichnete auf dem Bildschirm anzuzeigen.
            pygame.display.flip()

            clock.tick(60)  # limitiert FPS auf 60

        pygame.quit()

#Definitionen
    def quit_game(self):
        self.running = False
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