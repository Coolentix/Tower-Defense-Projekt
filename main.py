import pygame
import karte 
import gui

class Spiel:
    def __init__(self):
        # pygame setup
        pygame.init()

        title = pygame.display.set_caption("Tower Defense")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_x, self.screen_y = self.screen.get_size()

        self.gui = gui.GUIManager()
        #Hier Rendern
        #Menu
        self.gui.add_menu(gui.Button(x=self.screen_x//2-100, y=self.screen_y//2-50,width=200,height=100,color=(255, 0, 0),action=self.game_state))
        self.gui.add_menu(gui.Text(self.screen_x//2, y=self.screen_y//2, text="Spielen", font_size=40, color=(255, 255, 255), center=True))
                
        #Spiel
        self.tilemap = karte.TileMap(self.screen.get_size())
        self.gui.add_game(self.tilemap)        # Kartenobjekt erzeugen (erst hier weil vorher screen size nicht bekannt)
        self.gui.add_game(gui.Button(x=self.screen_x-60,y=10,width=50,height=50,color=(255, 0, 0),action=self.quit_game))
        self.gui.add_game(gui.Checkbox(x=self.tilemap.TILE_SIZE*self.tilemap.COLS+20,y=10,width=45,height=45,color=(0, 0, 0),state=0,action=self.tilemap.grid_ON_OFF))

        clock = pygame.time.Clock()

        self.MENU = "menu"
        self.GAME = "game"

        self.screen_state = self.MENU

        self.tilemap.map_one()

        self.running = True

        while self.running:

            #Menu Handle:
            if self.screen_state == self.MENU:
                self.menu()
            elif self.screen_state == self.GAME:
                self.game()
                

            # Den Bildschirm mit einer Farbe füllen, um alles aus dem letzten Frame zu löschen.

            # Das Display mit flip() aktualisieren, um das Gezeichnete auf dem Bildschirm anzuzeigen.
            pygame.display.flip()

            clock.tick(60)  # limitiert FPS auf 60

        pygame.quit()

#Definitionen
    def quit_game(self):
        self.running = False
        pygame.quit()

    def game_state(self):
        self.screen_state = self.GAME

    def menu(self):
        self.screen.fill((255,255,255))

        #self.start_button.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event, self.screen_state)

        
        self.gui.draw(self.screen, self.screen_state)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.screen_state = self.GAME
        #if keys[pygame.K_ESCAPE]:
            #self.running = False


    def game(self):
        self.screen.fill("white")
 
        # HIER DAS SPIEL RENDERN
        #self.tilemap.draw_tilemap(self.screen)

        # Ereignisse abfragen
        # Das pygame.QUIT-Event wird ausgelöst, wenn der Benutzer das Fenster über das Schließen-Symbol (X) beendet.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event, self.screen_state)

        
        self.gui.draw(self.screen, self.screen_state)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.screen_state = self.MENU
        

# Hier die Klassen

# jeweils in einzählne Dateien für übersichtlichkeit?
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

Spiel()