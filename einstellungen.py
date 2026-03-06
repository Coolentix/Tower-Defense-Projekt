import pygame
import gui


class EinstellungenManager:
    def __init__(self, screen_size, gui_manager, musik_manager=None):
        self.screen_width, self.screen_height = screen_size
        self.gui = gui_manager
        self.musik_manager = musik_manager  # Referenz zum MusikManager
        
        # Einstellungs-Werte
        self.schwierigkeit = 2  # 1 = Leicht, 2 = Mittel, 3 = Schwer
        self.musik_volume = 70  # 0-100
        self.effekte_volume = 80  # 0-100
        self.grafik_qualitaet = 2  # 1 = Niedrig, 2 = Mittel, 3 = Hoch
        self.sprache = "Deutsch"  # Deutsch, English
        self.fps_limit = 60  # FPS-Limit
        
        self.buttons = []
        self.text_labels = {}
        self.slider_musik = None
        self.slider_effekte = None
        self.back_button = None
        self.ui_initialized = False
    
    def ensure_ui_initialized(self):
        """Initialisiere die UI beim ersten Aufruf"""
        if not self.ui_initialized:
            self._setup_ui()
            self.ui_initialized = True
    
    def _setup_ui(self):
        """Erstelle die UI-Elemente für die Einstellungen"""
        start_x = self.screen_width // 4
        start_y = self.screen_height // 6
        spacing = 80
        
        # Titel
        self.gui.add_settings(gui.Text(
            x=self.screen_width // 2,
            y=50,
            text="EINSTELLUNGEN",
            font_size=80,
            color=(255, 255, 255),
            center=True
        ))
        
        # Schwierigkeit
        text1 = gui.Text(
            x=start_x,
            y=start_y,
            text=f"Schwierigkeit: {['Leicht', 'Mittel', 'Schwer'][self.schwierigkeit - 1]}",
            font_size=40,
            color=(255, 255, 255)
        )
        self.gui.add_settings(text1)
        self.text_labels["schwierigkeit"] = text1
        button1 = gui.Button(
            x=start_x + 400,
            y=start_y,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.prev_schwierigkeit
        )
        button2 = gui.Button(
            x=start_x + 500,
            y=start_y,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.next_schwierigkeit
        )
        self.gui.add_settings(button1)
        self.gui.add_settings(button2)
        self.buttons.append(("schwierigkeit_links", button1))
        self.buttons.append(("schwierigkeit_rechts", button2))
        
        # Musik-Volumen
        text2 = gui.Text(
            x=start_x,
            y=start_y + spacing,
            text=f"Musik: {self.musik_volume}%",
            font_size=40,
            color=(255, 255, 255)
        )
        self.gui.add_settings(text2)
        self.text_labels["musik"] = text2
        button3 = gui.Button(
            x=start_x + 400,
            y=start_y + spacing,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.musik_leiser
        )
        button4 = gui.Button(
            x=start_x + 500,
            y=start_y + spacing,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.musik_lauter
        )
        self.gui.add_settings(button3)
        self.gui.add_settings(button4)
        self.buttons.append(("musik_minus", button3))
        self.buttons.append(("musik_plus", button4))
        
        # Effekte-Volumen
        text3 = gui.Text(
            x=start_x,
            y=start_y + spacing * 2,
            text=f"Effekte: {self.effekte_volume}%",
            font_size=40,
            color=(255, 255, 255)
        )
        self.gui.add_settings(text3)
        self.text_labels["effekte"] = text3
        button5 = gui.Button(
            x=start_x + 400,
            y=start_y + spacing * 2,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.effekte_leiser
        )
        button6 = gui.Button(
            x=start_x + 500,
            y=start_y + spacing * 2,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.effekte_lauter
        )
        self.gui.add_settings(button5)
        self.gui.add_settings(button6)
        self.buttons.append(("effekte_minus", button5))
        self.buttons.append(("effekte_plus", button6))
        
        # Grafik-Qualität
        text4 = gui.Text(
            x=start_x,
            y=start_y + spacing * 3,
            text=f"Grafik: {['Niedrig', 'Mittel', 'Hoch'][self.grafik_qualitaet - 1]}",
            font_size=40,
            color=(255, 255, 255)
        )
        self.gui.add_settings(text4)
        self.text_labels["grafik"] = text4
        button7 = gui.Button(
            x=start_x + 400,
            y=start_y + spacing * 3,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.prev_grafik
        )
        button8 = gui.Button(
            x=start_x + 500,
            y=start_y + spacing * 3,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.next_grafik
        )
        self.gui.add_settings(button7)
        self.gui.add_settings(button8)
        self.buttons.append(("grafik_links", button7))
        self.buttons.append(("grafik_rechts", button8))
        
        # Sprache
        text5 = gui.Text(
            x=start_x,
            y=start_y + spacing * 4,
            text=f"Sprache: {self.sprache}",
            font_size=40,
            color=(255, 255, 255)
        )
        self.gui.add_settings(text5)
        self.text_labels["sprache"] = text5
        button9 = gui.Button(
            x=start_x + 400,
            y=start_y + spacing * 4,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.prev_sprache
        )
        button10 = gui.Button(
            x=start_x + 500,
            y=start_y + spacing * 4,
            width=50,
            height=50,
            color=(100, 100, 100),
            action=self.next_sprache
        )
        self.gui.add_settings(button9)
        self.gui.add_settings(button10)
        self.buttons.append(("sprache_links", button9))
        self.buttons.append(("sprache_rechts", button10))
        
        # Zurück-Button
        self.back_button = gui.Button(
            x=self.screen_width - 150,
            y=self.screen_height - 100,
            width=130,
            height=80,
            color=(200, 50, 50),
            action=self.on_back
        )
        self.buttons.append(("back", self.back_button))
        self.gui.add_settings(self.back_button)
        self.gui.add_settings(gui.Text(
            x=self.screen_width - 85,
            y=self.screen_height - 60,
            text="Zurück",
            font_size=30,
            color=(255, 255, 255),
            center=True
        ))
    
    # Schwierigkeit
    def prev_schwierigkeit(self):
        if self.schwierigkeit > 1:
            self.schwierigkeit -= 1
            self._update_label("schwierigkeit")
    
    def next_schwierigkeit(self):
        if self.schwierigkeit < 3:
            self.schwierigkeit += 1
            self._update_label("schwierigkeit")
    
    # Musik-Volumen
    def musik_leiser(self):
        if self.musik_volume > 0:
            self.musik_volume = max(0, self.musik_volume - 10)
            if self.musik_manager:
                self.musik_manager.set_volume(self.musik_volume)
            self._update_label("musik")
    
    def musik_lauter(self):
        if self.musik_volume < 100:
            self.musik_volume = min(100, self.musik_volume + 10)
            if self.musik_manager:
                self.musik_manager.set_volume(self.musik_volume)
            self._update_label("musik")
    
    # Effekte-Volumen
    def effekte_leiser(self):
        if self.effekte_volume > 0:
            self.effekte_volume = max(0, self.effekte_volume - 10)
            self._update_label("effekte")
    
    def effekte_lauter(self):
        if self.effekte_volume < 100:
            self.effekte_volume = min(100, self.effekte_volume + 10)
            self._update_label("effekte")
    
    # Grafik-Qualität
    def prev_grafik(self):
        if self.grafik_qualitaet > 1:
            self.grafik_qualitaet -= 1
            self._update_label("grafik")
    
    def next_grafik(self):
        if self.grafik_qualitaet < 3:
            self.grafik_qualitaet += 1
            self._update_label("grafik")
    
    # Sprache
    def prev_sprache(self):
        sprachen = ["Deutsch", "English"]
        idx = sprachen.index(self.sprache)
        self.sprache = sprachen[(idx - 1) % len(sprachen)]
        self._update_label("sprache")
    
    def next_sprache(self):
        sprachen = ["Deutsch", "English"]
        idx = sprachen.index(self.sprache)
        self.sprache = sprachen[(idx + 1) % len(sprachen)]
        self._update_label("sprache")
    
    def _update_label(self, label_key):
        """Aktualisiere ein Label mit den neuen Werten"""
        if label_key == "schwierigkeit":
            self.text_labels["schwierigkeit"].text = f"Schwierigkeit: {['Leicht', 'Mittel', 'Schwer'][self.schwierigkeit - 1]}"
            self.text_labels["schwierigkeit"].set_text(self.text_labels["schwierigkeit"].text)
        elif label_key == "musik":
            self.text_labels["musik"].text = f"Musik: {self.musik_volume}%"
            self.text_labels["musik"].set_text(self.text_labels["musik"].text)
        elif label_key == "effekte":
            self.text_labels["effekte"].text = f"Effekte: {self.effekte_volume}%"
            self.text_labels["effekte"].set_text(self.text_labels["effekte"].text)
        elif label_key == "grafik":
            self.text_labels["grafik"].text = f"Grafik: {['Niedrig', 'Mittel', 'Hoch'][self.grafik_qualitaet - 1]}"
            self.text_labels["grafik"].set_text(self.text_labels["grafik"].text)
        elif label_key == "sprache":
            self.text_labels["sprache"].text = f"Sprache: {self.sprache}"
            self.text_labels["sprache"].set_text(self.text_labels["sprache"].text)
    
    def on_back(self):
        """Wird aufgerufen wenn Zurück-Button gedrückt wird"""
        print("Einstellungen speichern und zurück zum Menü")
    
    def get_settings(self):
        """Gibt die aktuellen Einstellungen zurück"""
        return {
            "schwierigkeit": self.schwierigkeit,
            "musik_volume": self.musik_volume,
            "effekte_volume": self.effekte_volume,
            "grafik_qualitaet": self.grafik_qualitaet,
            "sprache": self.sprache,
            "fps_limit": self.fps_limit
        }
