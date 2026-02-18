import pygame
import karte 
import gui
import gegner
import runde

class Spiel:
    def __init__(self):
        # pygame setup
        pygame.init()
        pygame.mixer.init()

        title = pygame.display.set_caption("Tower Defense")
        info = pygame.display.Info()
        self.monitor_w = info.current_w
        self.monitor_h = info.current_h
        if self.monitor_w / self.monitor_h > 16/9:
            self.screen_y = self.monitor_h
            self.screen_x = int(self.screen_y * 16/9)
        else:
            self.screen_x = self.monitor_w
            self.screen_y = int(self.screen_x * 9/16)

        # 3️⃣ Screen erstellen (GANZ WICHTIG)
        self.screen = pygame.display.set_mode(
            (self.monitor_w, self.monitor_h),
            pygame.NOFRAME
        )

        # 4️⃣ Game Surface erstellen
        self.game_surface = pygame.Surface((self.screen_x, self.screen_y))

        # 5️⃣ Offset berechnen
        self.x_offset = (self.monitor_w - self.screen_x) // 2
        self.y_offset = (self.monitor_h - self.screen_y) // 2

        
        self.MENU = "menu"
        self.GAME = "game"
        self.SETTINGS = "setting"
        self.LOADINGSCREEN = "loadingscreen"
        self.TITLESCREEN = "titlescreen"

        self.screen_state = self.GAME

        self.gui = gui.GUIManager(self.screen_state)
        
        self.game_speed = 1
        self.runden_anzahl = 0
        self.runde = None

        #Lade Bildschirm
        start_y = self.screen_y // 1 - 170
        spacing = 220
        self.add_loadingscreen_button(900,150,"Press any button", start_y, self.menu_state)

        #Titel Bildschirm
        #start_y = self.screen_y // 2 - 320
        #spacing = 220
        #self.add_titlescreen_button(1900,700,"FRIENDS VS ENEMIES", start_y, self.menu_state)

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
        self.gui.add_game(gui.Button(x=panel_x,y=button_y,width=button_width,height=button_height,color=(0, 0, 0),image_path="../Tower-Defense-Projekt/bilder/Ameise.gif",action=self.enable_friend_placement1))
        self.gui.add_game(gui.Button(x=panel_x + button_width + gap,y=button_y,width=button_width,height=button_height,color=(0, 0, 0),action=self.enable_friend_placement2)) #Hier dann anderer Typ
        self.gui.add_game(gui.Button(x=panel_x,y=button_y + button_width + gap,width=button_width,height=button_height,color=(0, 0, 0),action=self.enable_friend_placement3))
        self.gui.add_game(gui.Button(x=panel_x + button_width + gap,y=button_y + button_width + gap,width=button_width,height=button_height,color=(0, 0, 0),action=self.enable_friend_placement4))
        self.gui.add_game(gui.Button(x=self.screen_x - 100 - gap,y=self.screen_y - 100 - gap,width=100,height=100,color=(0, 0, 0),action=self.runden_start))
        clock = pygame.time.Clock()

        self.running = True

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
        pygame.quit()

    def menu_state(self):
        self.screen_state = self.MENU
        self.gui.set_state(self.screen_state)

    def game_state(self):
        self.screen_state = self.GAME
        self.gui.set_state(self.screen_state)

    def spawn_enemy(self, enemy_type=gegner.EnemyType.WALKER):
        #Gegner erstellen
        erster_gegner = gegner.Gegner(enemy_type, self.tilemap,self.tilemap.map_one())
        self.gui.add_game(erster_gegner)

    def runden_start(self):
        self.runden_anzahl += 1
        self.runde = runde.RundenManager(self.runden_anzahl)
        print(self.runden_anzahl)

    def settings_state(self):
        self.screen_state = self.SETTINGS

        
    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event)

        self.image = pygame.image.load("../Tower-Defense-Projekt/bilder/pixil-frame-0 (2).png").convert_alpha()
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

        if self.runde:
            enemy = self.runde.update(self.dt)
            if enemy != None:
                self.spawn_enemy(enemy)

        #self.runden_start()

        self.gui.gegner_kill()

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