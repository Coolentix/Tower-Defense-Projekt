import pygame

class TileMap:
    def __init__(self):
        self.TILE_SIZE = 20     #Größe des Tiles
        self.ROWS = 50          #Zeilen
        self.COLS = 50          #Spalten
        self.tilemap = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]     #Erzeuge ein Spielfeld mit ROWS Zeilen und COLS Spalten, alles leer (0)
        self.rects = [[pygame.Rect(col*self.TILE_SIZE, row*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)for col in range(self.COLS)]for row in range(self.ROWS)]

    def draw_tilemap(self,screen):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                # weißes Tile
                pygame.draw.rect(screen, (255, 255, 255), self.rects[col][row]) #zeichnet weißes Rechteck

                # schwarze Linie (Grid)
                #pygame.draw.rect(screen, (0, 0, 0), self.rects[col][row], 1)    #zeichnet schwarze umrandung

        pygame.draw.line(screen, (0, 0, 0), (self.COLS*self.TILE_SIZE,0),(self.COLS*self.TILE_SIZE,self.ROWS*self.TILE_SIZE), 2) #Karten Rand Rechts
        pygame.draw.line(screen, (0, 0, 0), (0,self.ROWS*self.TILE_SIZE),(self.COLS*self.TILE_SIZE,self.ROWS*self.TILE_SIZE), 2) #Karten Rand Links
        pygame.draw.line(screen, (0, 0, 0), (self.COLS*self.TILE_SIZE,self.ROWS*self.TILE_SIZE),(0,self.ROWS*self.TILE_SIZE), 2) #Karten Rand Unten
        pygame.draw.line(screen, (0, 0, 0), (self.COLS*self.TILE_SIZE,self.ROWS*self.TILE_SIZE),(self.COLS*self.TILE_SIZE,0), 2) #Karten Rand Oben (Angaben ohne Gewehr)

    def tile_clicked(self,screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row = mouse_x // self.TILE_SIZE
        col = mouse_y // self.TILE_SIZE
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            pygame.draw.rect(screen, (0, 0, 0, 50), self.rects[col][row])
