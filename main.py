import pygame
import karte 
import gui
import gegner
import freund

class Spiel:
    def __init__(self):
        # pygame setup
        pygame.init()

        title = pygame.display.set_caption("Tower Defense")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_x, self.screen_y = self.screen.get_size()

        
        self.MENU = "menu"
        self.GAME = "game"
        self.SETTINGS = "setting"
        self.LOADINGSCREEN = "loadingscreen"

        self.screen_state = self.LOADINGSCREEN

        self.gui = gui.GUIManager(self.screen_state)
        #self.gegner = gegener.Gegner()

        #Lade Bildschirm
        start_y = self.screen_y // 1 - 170
        spacing = 220
        self.add_loadingscreen_button(900,150,"Press any button", start_y, self.menu_state)

        #Hier Rendern
        #Menu
        start_y = self.screen_y // 2
        spacing = 110
        self.add_menu_button(500,100,"Spielen", start_y, self.game_state)
        self.add_menu_button(500,100,"Einstellungen", start_y + spacing, self.settings_state)
        self.add_menu_button(500,100,"Schließen", start_y + spacing * 2, self.quit_game)
                
        #Spiel
        self.tilemap = karte.TileMap(self.screen.get_size(),2*9,14*2,self.gui)
        self.gui.add_game(self.tilemap)        # Kartenobjekt erzeugen (erst hier weil vorher screen size nicht bekannt)
        self.tilemap.map_one()

        panel_x = self.tilemap.TILE_SIZE * self.tilemap.COLS + 20
        panel_y = self.tilemap.TILE_SIZE * self.tilemap.ROWS + 20
        panel_width = self.screen_x - panel_x
        button_y = 65
        gap = 10
        button_width = (panel_width) // 2 - gap
        button_height = button_width

        self.gui.add_game(gui.Button(x=self.screen_x-55,y=gap,width=45,height=45,color=(255, 0, 0),action=self.quit_game))
        self.gui.add_game(gui.Checkbox(x=self.tilemap.TILE_SIZE*self.tilemap.COLS+20,y=10,width=45,height=45,color=(0, 0, 0),state=0,action=self.tilemap.grid_ON_OFF))
        self.gui.add_game(gui.Button(x=panel_x,y=button_y,width=button_width,height=button_height,color=(0, 0, 0),action=self.enable_friend_placement))
        self.gui.add_game(gui.Button(x=panel_x + button_width + gap,y=button_y,width=button_width,height=button_height,color=(0, 0, 0),action=None)) #Hier dann anderer Typ
        
        clock = pygame.time.Clock()

        self.running = True

        #Gegner erstellen
        self.gui.add_game(gegner.Gegner(gegner.EnemyType.WALKER, self.tilemap,self.tilemap.map_one()))

        while self.running:

            self.dt = clock.tick(60)

            #Menu Handle:
            if self.screen_state == self.LOADINGSCREEN:
                self.loadingscreen()
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
        pygame.quit()

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

    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event)

        self.image = pygame.image.load("../Tower-Defense-Projekt/bilder/image.png").convert_alpha()
        self.image = pygame.image.load("../Tower-Defense-Projekt/bilder/image.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (self.screen_x,self.screen_y))
        self.rect = self.image.get_rect(center=(self.screen_x // 2, self.screen_y // 2))
        self.screen.blit(self.image, self.rect)
        
        self.gui.draw(self.screen)

        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_SPACE]:
        #    self.game_state()

    def loadingscreen(self):
        self.screen.fill((255,255,255))

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
        #self.tilemap.draw_tilemap(self.screen)

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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.menu_state()

    def settings(self):
        self.screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event)

        
        self.gui.draw(self.screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.menu_state()

    def add_menu_button(self, width, height, text, y, action):
        BUTTON_W, BUTTON_H = width, height

        self.gui.add_menu(gui.Button(x=20 ,y=y,width=BUTTON_W,height=BUTTON_H,color=(0, 0, 0),alpha=0,action=action)) #self.screen_x // 2 - BUTTON_W // 2

        self.gui.add_menu(gui.Text(x=BUTTON_W//2 + 20,y=y + BUTTON_H // 2,text=text,font_size=75,color=(255, 255, 255),center=True))    #self.screen_x // 2

    def add_loadingscreen_button(self, width, height, text, y, action):
        BUTTON_W, BUTTON_H = width, height

        self.gui.add_loadingscreen(gui.Button(x=self.screen_x // 2 - BUTTON_W // 2,y=y,width=BUTTON_W,height=BUTTON_H,color=(0, 0, 0),action=action))

        self.gui.add_loadingscreen(gui.Text(x=self.screen_x // 2,y=y + BUTTON_H // 2,text=text,font_size=100,color=(255, 255, 255),center=True))

    def enable_friend_placement(self):
        self.gui.placing_friend = True

class Kauf:
    pass

class Spiel_Attribute:
    def __init__(self):
        geld = 0
        leben = 0
        score = 0
        zeit = 0

Spiel()import pygame
import karte 
import gui

# Klasse für Buttons mit Bildern, Haptik (Klick) und Hover-Effekt
class ImageButton(gui.GUIElement):
    def __init__(self, x, y, width, height, image_path, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.image = None
        
        # Versuch das Bild zu laden und zu skalieren
        try:
            loaded_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(loaded_image, (width, height))
        except Exception as e:
            print(f"Fehler beim Laden von {image_path}: {e}")
            # Fallback: Graues Rechteck, falls Bild fehlt
            self.image = pygame.Surface((width, height))
            self.image.fill((100, 100, 100))

    def draw(self, screen):
        # Positionen initialisieren
        draw_x = self.rect.x
        draw_y = self.rect.y
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        # Haptik: Wenn gedrückt, Button leicht verschieben
        if is_hovered and pygame.mouse.get_pressed()[0]:
            draw_x += 3
            draw_y += 3

        # 1. Das Bild zeichnen
        screen.blit(self.image, (draw_x, draw_y))

        # 2. Hover-Effekt ("Funkeln" / Aufleuchten)
        if is_hovered:
            # Erstelle eine weiße, halb-transparente Fläche
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 50)) # Weiß mit Transparenz (50 von 255)
            # Zeichne sie über den Button
            screen.blit(overlay, (draw_x, draw_y))
            
            # Optional: Rand hervorheben
            pygame.draw.rect(screen, (255, 255, 200), (draw_x, draw_y, self.rect.width, self.rect.height), 3)

    def handle_event(self, event):
        # Klick-Logik
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

class Spiel:
    def __init__(self):
        # pygame setup
        pygame.init()

        pygame.display.set_caption("Tower Defense")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_x, self.screen_y = self.screen.get_size()

        # --- HINTERGRUNDBILD LADEN ---
        try:
            bg_img = pygame.image.load("hintergrund.png").convert()
            self.background = pygame.transform.scale(bg_img, (self.screen_x, self.screen_y))
        except Exception as e:
            print(f"Hintergrund konnte nicht geladen werden: {e}. Nutze Weiß.")
            self.background = pygame.Surface((self.screen_x, self.screen_y))
            self.background.fill((255, 255, 255))
        # -----------------------------

        self.gui = gui.GUIManager()
        
        # --- MENU BUTTONS KONFIGURATION ---
        btn_width = 300
        btn_height = 100
        gap = 20
        
        center_x = self.screen_x // 2 - btn_width // 2
        total_height = (btn_height * 3) + (gap * 2)
        start_y = (self.screen_y // 2) - (total_height // 2)

        # 1. Start Button
        self.gui.add_menu(ImageButton(center_x, start_y, btn_width, btn_height, "start.png", self.game_state))
        
        # 2. Einstellungen Button
        self.gui.add_menu(ImageButton(center_x, start_y + btn_height + gap, btn_width, btn_height, "einstellungen.png", self.settings_menu))

        # 3. Stop Button
        self.gui.add_menu(ImageButton(center_x, start_y + (btn_height + gap) * 2, btn_width, btn_height, "stop.png", self.quit_game))
        
        # --- SPIEL GUI ---
        self.tilemap = karte.TileMap(self.screen.get_size())
        self.gui.add_game(self.tilemap)
        
        # Quit-Button im Spiel
        self.gui.add_game(gui.Button(x=self.screen_x-60, y=10, width=50, height=50, color=(255, 0, 0), action=self.quit_game))
        
        # Grid Toggle
        self.gui.add_game(gui.Checkbox(x=self.tilemap.TILE_SIZE * self.tilemap.COLS + 20, y=10, width=45, height=45, color=(0, 0, 0), state=0, action=self.tilemap.grid_ON_OFF))

        self.clock = pygame.time.Clock()

        self.MENU = "menu"
        self.GAME = "game"
        self.screen_state = self.MENU

        self.tilemap.map_one()
        self.running = True

        # --- HAUPTSCHLEIFE ---
        while self.running:
            if self.screen_state == self.MENU:
                self.menu()
            elif self.screen_state == self.GAME:
                self.game()
                
            pygame.display.flip()
            self.clock.tick(60)

        # Erst hier beenden, wenn die Schleife vorbei ist!
        pygame.quit()

    # --- WICHTIGE ÄNDERUNG HIER: KEIN pygame.quit() ---
    def quit_game(self):
        self.running = False
        # pygame.quit() wurde hier entfernt, damit es nicht abstürzt!

    def game_state(self):
        self.screen_state = self.GAME

    def settings_menu(self):
        print("Einstellungen geklickt")

    def menu(self):
        # Hintergrund zeichnen
        self.screen.blit(self.background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.gui.handle_event(event, self.screen_state)
        
        # Wenn running False ist, nicht mehr zeichnen (verhindert Fehler im letzten Frame)
        if self.running:
            self.gui.draw(self.screen, self.screen_state)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.screen_state = self.GAME

    def game(self):
        self.screen.fill("white")
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.gui.handle_event(event, self.screen_state)
        
        if self.running:
            self.gui.draw(self.screen, self.screen_state)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.screen_state = self.MENU

# Platzhalter Klassen
class Freunde:
    def __init__(self):
        pass
class Projektil:
    pass
class Kauf:
    pass
class Spiel_Attribute:
    def __init__(self):
        pass

if __name__ == "__main__":
    Spiel()