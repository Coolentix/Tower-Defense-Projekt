import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # Ereignisse abfragen
    # Das pygame.QUIT-Event wird ausgelöst, wenn der Benutzer das Fenster über das Schließen-Symbol (X) beendet.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Den Bildschirm mit einer Farbe füllen, um alles aus dem letzten Frame zu löschen.
    screen.fill("purple")

    # HIER DAS SPIEL RENDERN

    # Das Display mit flip() aktualisieren, um das Gezeichnete auf dem Bildschirm anzuzeigen.
    pygame.display.flip()

    clock.tick(60)  # limitiert FPS auf 60

pygame.quit()

# Hier die Klassen
# jeweils in einzählne Dateien für übersichtlichkeit?

class Karte:
    pass

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