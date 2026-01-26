import pygame
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