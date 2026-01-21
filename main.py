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

        self.screen_state = self.MENU

        self.gui = gui.GUIManager(self.screen_state)
        #self.gegner = gegener.Gegner()

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
        self.gui.add_game(gui.Button(x=panel_x + button_width + gap,y=button_y,width=button_width,height=button_height,color=(0, 0, 0))) #Hier dann anderer Typ
        self.gui.add_game(gui.Button(x=panel_x + button_width + gap,y=panel_y-button_height-gap,width=button_width,height=button_height,color=(0, 0, 0),action=self.spawn_enemy)) #Hier dann anderer Typ
        

        clock = pygame.time.Clock()

        self.running = True

        while self.running:

            self.dt = clock.tick(60)

            #Menu Handle:
            if self.screen_state == self.MENU:
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
        #self.screen.fill("white")
        """
        self.image = pygame.image.load("../Tower-Defense-Projekt/image.png").convert_alpha()

        width = self.image.get_width()
        height = self.image.get_height()

        self.image = pygame.transform.scale(self.image, (width // 2, height // 2))
        self.rect = self.image.get_rect(center=(self.screen_x // 2, self.screen_y // 2))
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event)

        self.image = pygame.image.load("../Tower-Defense-Projekt/image.png").convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (self.screen_x,self.screen_y))
        self.rect = self.image.get_rect(center=(self.screen_x // 2, self.screen_y // 2))
        self.screen.blit(self.image, self.rect)
        
        self.gui.draw(self.screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.game_state()


    def game(self):
        self.screen.fill("white")

        # Ereignisse abfragen
        # Das pygame.QUIT-Event wird ausgelöst, wenn der Benutzer das Fenster über das Schließen-Symbol (X) beendet.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.gui.handle_event(event)

        
        self.gui.draw(self.screen)
        self.gui.update(self.dt)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.screen_state = self.MENU

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

Spiel()