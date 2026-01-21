import pygame
import freund

class TileMap:
    def __init__(self,screen_size,x,y,gui):
        self.ROWS = x                                      #Spalten
        self.COLS = y                                      #Zeilen
        self.screen_x, self.screen_y = screen_size          #Bildschirm göße errechnen
        self.TILE_SIZE = (self.screen_y-20)//self.ROWS      #Größe des Tiles
        self.start_x = 10                                   #Verschiebung X
        self.start_y = 10                                   #statische Verschiebung Y
        self.tile_color = (255,255,255)
        self.tile_type = TileType.EMPTY
        self.grid_active = False
        #self.friends = []
        self.gui = gui

        # Erzeuge eine Tilemap
        self.tilemap = None
        self.empty_map()
        
    def draw(self,screen):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.tilemap[row][col].draw(screen)
        
        #zeichnet schwarze umrandung

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
            tile = self.tilemap[row][col]
            hover_color = (min(self.tile_color[0] + 100, 255),min(self.tile_color[1] + 100, 255),min(self.tile_color[2] + 100, 255))
            pygame.draw.rect(screen, hover_color, tile.rect)
            if tile.type == TileType.PATH:
                pygame.draw.rect(screen, (255,100,100), tile.rect)
            if tile.type == TileType.FRIEND:
                pygame.draw.rect(screen, (100,100,100), tile.rect)
            if tile.type == TileType.EMPTY and self.gui.placing_friend:
                pygame.draw.rect(screen, (100,255,100), tile.rect)
                

        # auf Linker Maustasten druck tritt änderung in Kraft
            if pygame.mouse.get_pressed()[0] == 1:
                #print(row,col)
                if tile.type == 1:
                    pass
                elif tile.type == 0 and self.gui.placing_friend:    #Hier später: and self.tile_type == Friend_type_xy
                    self.place_friend(row, col)
                    self.gui.placing_friend = False
                elif tile.type == 3:
                    pass
                else:
                    tile.color = self.tile_color
                    tile.type = self.tile_type
                    if tile.type != 0:
                        tile.border = False
                    elif tile.type == 0 and self.grid_active:
                        tile.border = 1
                        tile.color = (0,0,0)
            
        #Je nach Taste ändert was gemalt wird (kann später noch auf Button geäandert werden)
        """
        if pygame.key.get_pressed()[pygame.K_1]:
            self.tile_color = (0,0,0)
            self.tile_type = 3

        if pygame.key.get_pressed()[pygame.K_2]:
            self.tile_color = (255,0,0)
            self.tile_type = 2

        if pygame.key.get_pressed()[pygame.K_3]:
            self.tile_color = (255,255,255)
            self.tile_type = 0
        """

    def grid_ON_OFF(self,state):
        self.grid_active = not self.grid_active
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.tilemap[row][col].type == TileType.EMPTY:
                    if state:
                        self.tilemap[row][col].border = 1
                        self.tilemap[row][col].color = (0,0,0)
                    else: 
                        self.tilemap[row][col].border = 0
                        self.tilemap[row][col].color = (255,255,255)
                            

    def empty_map(self):
        self.tilemap = [[Tile(self.start_x + col*self.TILE_SIZE, self.start_y + row*self.TILE_SIZE, self.TILE_SIZE) for col in range(self.COLS)] for row in range(self.ROWS)]
    
    def map_one(self):
        path = [(1,0), (1, 1), (1, 2), (1, 3), (1, 4),(1,5),(1,6),(1,7),(1,8),(1,9),(2,9),(3,9),(3,8),(3,7),(3,6),(3,5),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4)]
        # Schleife durch die Koordinaten und Farbe setzen
        for x, y in path:
            self.tilemap[x][y].type = TileType.PATH
        
        return path

    def place_friend(self, row, col):
        tile = self.tilemap[row][col]

        #Tile Färben
        tile.type = TileType.FRIEND
        tile.color = (0, 0, 0)
        tile.border = 0

        self.gui.add_game(freund.Freund(row,col,(tile.rect.center)))

class TileType:
    EMPTY = 0
    PATH = 1
    OBSTACLE = 2
    FRIEND = 3
    
class Tile:
    def __init__(self, x, y, size, type=TileType.EMPTY, border=False,color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.border = border
        self.type = type

    def draw(self, screen):
        if self.type == TileType.PATH:
            pygame.draw.rect(screen, (0,0,255), self.rect,False)
        else:
            pygame.draw.rect(screen, self.color, self.rect,self.border)

