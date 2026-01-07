import pygame

class TileMap:
    def __init__(self,screen_size):
        self.ROWS = 20          #Spalten
        self.COLS = 30          #Zeilen
        self.screen_x, self.screen_y = screen_size
        self.TILE_SIZE = (self.screen_y-20)//self.ROWS     #Größe des Tiles
        self.start_x = 10      #Verschiebung X
        self.start_y = 10       #statische Verschiebung Y

        self.tilemap = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]     #Erzeuge ein Spielfeld mit ROWS Zeilen und COLS Spalten, alles leer (0)

        # Erzeuge pygame.Rect für jedes Tile (für Draw)
        self.rects = [[pygame.Rect(self.start_x + col*self.TILE_SIZE,
                                   self.start_y +  row*self.TILE_SIZE,
                                     self.TILE_SIZE, self.TILE_SIZE)
                                     for col in range(self.COLS)]
                                     for row in range(self.ROWS)]

    def draw_tilemap(self,screen):
        #Zeichnet die gesamte TileMap auf den Bildschirm
        for row in range(self.ROWS):
            for col in range(self.COLS):
                #zeichnet die Tiles
                rect = self.rects[row][col]
                pygame.draw.rect(screen, (255, 255, 255), rect) #zeichnet weißes Rechteck

                # schwarze Linie (Grid)
                #pygame.draw.rect(screen, (0, 0, 0), rect, 1)    #zeichnet schwarze umrandung

        pygame.draw.line(screen, (0, 0, 0), (self.start_x, self.start_y), 
                                            (self.start_x, self.start_y + self.ROWS*self.TILE_SIZE), 2) #Karten Rand Links
        
        pygame.draw.line(screen, (0, 0, 0), (self.start_x, self.start_y + self.ROWS*self.TILE_SIZE),
                                            (self.start_x + self.COLS*self.TILE_SIZE, self.start_y + self.ROWS*self.TILE_SIZE), 2) #Karten Rand Rechts
        
        pygame.draw.line(screen, (0, 0, 0), (self.start_x, self.start_y),
                                            (self.start_x + self.COLS*self.TILE_SIZE, self.start_y), 2)                        #Karten Rand Oben
        
        pygame.draw.line(screen, (0, 0, 0), (self.start_x +self.COLS*self.TILE_SIZE, self.start_y + self.ROWS*self.TILE_SIZE),
                                            (self.start_x + self.COLS*self.TILE_SIZE, self.start_y), 2)                        #Karten Rand Unten (Angaben ohne Gewehr)


        #Hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        col = (mouse_x - self.start_x) // self.TILE_SIZE
        row = (mouse_y - self.start_y) // self.TILE_SIZE
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            pygame.draw.rect(screen, (0, 0, 0 ,100), self.rects[row][col])
