import pygame
import karte 
import gui
import gegner
import freund
import einstellungen
import musik

class Spiel:
    def __init__(self):
        # pygame setup
        pygame.init()

        title = pygame.display.set_caption("Tower Defense")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_x, self.screen_y = self.screen.get_size()
        
        # Bildpfad relativ zum Verzeichnis der main.py
        import os
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.image_path = lambda path: os.path.join(self.base_path, path)

        
        self.MENU = "menu"
        self.GAME = "game"
        self.SETTINGS = "settings"
        self.LOADINGSCREEN = "loadingscreen"
        self.TITLESCREEN = "titlescreen"

        self.screen_state = self.LOADINGSCREEN

        self.gui = gui.GUIManager(self.screen_state)
        
        self.game_speed = 1
        
        # Einstellungen Manager
        self.einstellungen_manager = None
        
        # Musik Manager
        self.musik_manager = musik.MusikManager(self.base_path)

        #Lade Bildschirm
        start_y = self.screen_y // 1 - 270
        spacing = 220
        self.add_loadingscreen_image_button(self.image_path("bilder/Newgame.png"), start_y, self.menu_state, scale=0.55)

        #Titel Bildschirm
        #start_y = self.screen_y // 2 - 320
        #spacing = 220
        #self.add_titlescreen_button(1900,700,"FRIENDS VS ENEMIES", start_y, self.menu_state)

        #Hier Rendern
        #Menu
        start_y = self.screen_y // 2
        gap = 70  # Abstand zwischen den Buttons
        gap_bottom = 30  # Kleinerer Abstand unten
        
        # Button-Höhen berechnen
        scale = 0.5
        img1 = pygame.image.load(self.image_path("bilder/start.png"))
        img2 = pygame.image.load(self.image_path("bilder/einstellungen.png"))
        img3 = pygame.image.load(self.image_path("bilder/stop.png"))
        
        h1 = int(img1.get_height() * scale)
        h2 = int(img2.get_height() * scale)
        h3 = int(img3.get_height() * scale)
        
        y1 = start_y
        y2 = y1 + h1 + gap
        y3 = y2 + h2 + gap_bottom
        
        self.add_menu_button(300,150,"Spielen", y1, self.image_path("bilder/start.png"), self.game_state)
        self.add_menu_button(300,150,"Einstellungen", y2, self.image_path("bilder/einstellungen.png"), self.settings_state, scale=0.45)
        self.add_menu_button(300,150,"Schließen", y3, self.image_path("bilder/stop.png"), self.quit_game)
                
        #Spiel
        self.tilemap = karte.TileMap(self.screen.get_size(),2*9,14*2,self.gui)
        self.gui.add_game(self.tilemap)        # Kartenobjekt erzeugen (erst hier weil vorher screen size nicht bekannt)
        self.tilemap.map_one()

        panel_x = self.tilemap.TILE_SIZE * self.tilemap.COLS + 20
        panel_y = self.tilemap.TILE_SIZE * self.tilemap.ROWS + 20
        panel_width = self.screen_x - panel_x
        button_y = 65
        gap = 10
        button_width = max(1, (panel_width) // 2 - gap)
        button_height = max(1, button_width)

        self.gui.add_game(gui.Button(x=self.screen_x-55,y=gap,width=45,height=45,color=(255, 0, 0),action=self.quit_game))
        self.gui.add_game(gui.Checkbox(x=self.tilemap.TILE_SIZE*self.tilemap.COLS+20,y=10,width=45,height=45,color=(0, 0, 0),state=0,action=self.tilemap.grid_ON_OFF))
        self.gui.add_game(gui.Button(x=panel_x,y=button_y,width=button_width,height=button_height,color=(0, 0, 0),action=self.enable_friend_placement1))
        self.gui.add_game(gui.Button(x=panel_x + button_width + gap,y=button_y,width=button_width,height=button_height,color=(0, 0, 0),action=self.enable_friend_placement2)) #Hier dann anderer Typ
        self.gui.add_game(gui.Button(x=panel_x,y=button_y + button_width + gap,width=button_width,height=button_height,color=(0, 0, 0),action=self.enable_friend_placement3))
        self.gui.add_game(gui.Button(x=panel_x + button_width + gap,y=button_y + button_width + gap,width=button_width,height=button_height,color=(0, 0, 0),action=self.enable_friend_placement4))
        clock = pygame.time.Clock()

        self.running = True
        
        # Starte Hintergrundmusik
        self.musik_manager.start_musik()

        while self.running:

            self.dt = clock.tick(60)

            #Menu Handle:
            if self.screen_state == self.LOADINGSCREEN:
                self.loadingscreen()
            #elif self.screen_state == self.TITLESCREEN:
                #self.titlescreen()
            elif self.screen_state == self.MENU:
                self.menu()
            elif self.screen_state == self.GAME:
                self.game()
            elif self.screen_state == self.SETTINGS:
                self.settings()

            # Den Bildschirm mit einer Farbe füllen, um alles aus dem letzten Frame zu löschen.

            # Das Display mit flip() aktualisieren, um das Gezeichnete auf dem Bildschirm anzuzeigen.
            pygame.display.flip()

            clock.tick(60)  # limitiert FPS auf 60

        pygame.quit()

#Methoden
    def quit_game(self):
        self.running = False
        self.musik_manager.stop_musik()

    def menu_state(self):
        self.screen_state = self.MENU
        self.gui.set_state(self.screen_state)

    def game_state(self):
        self.screen_state = self.GAME
        self.gui.set_state(self.screen_state)

    def spawn_enemy(self):
        #Gegner erstellen
        erster_gegner = gegner.Gegner(gegner.EnemyType.WALKER, self.tilemap,self.tilemap.map_one())
        self.gui.add_game(erster_gegner)

    def settings_state(self):
        self.screen_state = self.SETTINGS
        self.gui.set_state(self.screen_state)

        
    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event)

        self.image = pygame.image.load(self.image_path("bilder/pixil-frame-0 (2).png"))
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (self.screen_x,self.screen_y))
        self.rect = self.image.get_rect(center=(self.screen_x // 2, self.screen_y // 2))
        self.screen.blit(self.image, self.rect)
        self.gui.draw(self.screen)
        
        pygame.display.flip()

        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_SPACE]:
        #    self.game_state()

    def loadingscreen(self):
        # Hintergrundbild laden und auf Bildschirmgröße skalieren
        # Statt self.screen.fill((255,255,255))
        try:
            hintergrund = pygame.image.load(self.image_path("bilder/pixil-frame-0 (3).png"))
            hintergrund = pygame.transform.scale(hintergrund, (self.screen_x, self.screen_y))
            self.screen.blit(hintergrund, (0, 0))
        except Exception as e:
            print(f"Fehler beim Laden des Hintergrundbilds: {e}")
            self.screen.fill((255, 255, 255)) # Fallback zu Weiß

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                self.menu_state()
            
            self.gui.handle_event(event)

        self.gui.draw(self.screen)


    def game(self):
        self.screen.fill((255,255,255))
 
        # HIER DAS SPIEL RENDERN

        # Ereignisse abfragen
        # Das pygame.QUIT-Event wird ausgelöst, wenn der Benutzer das Fenster über das Schließen-Symbol (X) beendet.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.spawn_enemy()

            self.gui.handle_event(event) 

        
        self.gui.draw(self.screen)
        self.gui.update(self.dt)

        self.gui.gegner_kill()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.menu_state()

    def settings(self):
        # Einstellungen Manager initialisieren wenn noch nicht geschehen
        if self.einstellungen_manager is None:
            self.einstellungen_manager = einstellungen.EinstellungenManager(self.screen.get_size(), self.gui, self.musik_manager)
            self.einstellungen_manager.ensure_ui_initialized()
        
        # Hintergrundbild laden
        self.image = pygame.image.load(self.image_path("bilder/pixil-frame-0 (2).png"))
        self.image = pygame.transform.scale(self.image, (self.screen_x, self.screen_y))
        self.rect = self.image.get_rect(center=(self.screen_x // 2, self.screen_y // 2))
        self.screen.blit(self.image, self.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event)

        self.gui.draw(self.screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.menu_state()

    def add_menu_button(self, width, height, text, y, image_path, action, scale=0.6):
        # Bild laden um die originale Größe zu bekommen
        temp_image = pygame.image.load(image_path)
        button_width, button_height = temp_image.get_size()
        
        # Skalieren
        button_width = int(button_width * scale)
        button_height = int(button_height * scale)
        
        # Margin von links
        margin_left = 20
        
        self.gui.add_menu(gui.ImageButton(x=margin_left, y=y, width=button_width, height=button_height, image_path=image_path, action=action))

    def add_loadingscreen_button(self, width, height, text, y, action):
        BUTTON_W, BUTTON_H = width, height

        self.gui.add_loadingscreen(gui.Button(x=self.screen_x // 2 - BUTTON_W // 2,y=y,width=BUTTON_W,height=BUTTON_H,color=(0, 0, 0),action=action))

        self.gui.add_loadingscreen(gui.Text(x=self.screen_x // 2,y=y + BUTTON_H // 2,text=text,font_size=100,color=(255, 255, 255),center=True))

    def add_loadingscreen_image_button(self, image_path, y, action, scale=1.0):
        # Bild laden um die originale Größe zu bekommen
        temp_image = pygame.image.load(image_path)
        button_width, button_height = temp_image.get_size()
        
        # Skalieren
        button_width = int(button_width * scale)
        button_height = int(button_height * scale)
        
        # Button zentriert hinzufügen
        x = self.screen_x // 2 - button_width // 2
        self.gui.add_loadingscreen(gui.ImageButton(x=x, y=y, width=button_width, height=button_height, image_path=image_path, action=action))

    def enable_friend_placement1(self):
        self.gui.placing_friend1 = True

    def enable_friend_placement2(self):
        self.gui.placing_friend2 = True

    def enable_friend_placement3(self):
        self.gui.placing_friend3 = True
    
    def enable_friend_placement4(self):
        self.gui.placing_friend4 = True

class Kauf:
    pass

class Spiel_Attribute:
    def __init__(self):
        geld = 0
        leben = 0
        score = 0
        zeit = 0

Spiel()