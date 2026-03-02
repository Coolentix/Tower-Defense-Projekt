import pygame
import os


class MusikManager:
    """Verwaltet die Hintergrundmusik und deren Lautstärke"""
    
    def __init__(self, base_path):
        self.base_path = base_path
        self.musik_pfad = os.path.join(base_path, "Soundtrack.mp3")
        self.current_volume = 0.7  # Standard: 70%
        self.is_playing = False
        
        # Prüfe ob Datei existiert
        if not os.path.exists(self.musik_pfad):
            print(f"Warnung: {self.musik_pfad} nicht gefunden!")
        
    def start_musik(self):
        """Starte die Hintergrundmusik"""
        try:
            if not os.path.exists(self.musik_pfad):
                print(f"Fehler: Musikdatei nicht gefunden: {self.musik_pfad}")
                return False
            
            pygame.mixer.music.load(self.musik_pfad)
            pygame.mixer.music.set_volume(self.current_volume)
            pygame.mixer.music.play(-1)  # -1 bedeutet Endlosschleife
            self.is_playing = True
            print("Musik gestartet")
            return True
        except Exception as e:
            print(f"Fehler beim Starten der Musik: {e}")
            return False
    
    def stop_musik(self):
        """Stoppe die Hintergrundmusik"""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            print("Musik gestoppt")
        except Exception as e:
            print(f"Fehler beim Stoppen der Musik: {e}")
    
    def pause_musik(self):
        """Pausiere die Musik"""
        try:
            pygame.mixer.music.pause()
            print("Musik pausiert")
        except Exception as e:
            print(f"Fehler beim Pausieren der Musik: {e}")
    
    def unpause_musik(self):
        """Setze die pausierte Musik fort"""
        try:
            pygame.mixer.music.unpause()
            print("Musik fortgesetzt")
        except Exception as e:
            print(f"Fehler beim Fortsetzen der Musik: {e}")
    
    def set_volume(self, volume_percent):
        """Stelle die Lautstärke ein (0-100)"""
        # Konvertiere Prozent (0-100) zu pygame Wert (0.0-1.0)
        volume = max(0.0, min(1.0, volume_percent / 100.0))
        self.current_volume = volume
        
        try:
            pygame.mixer.music.set_volume(volume)
            print(f"Lautstärke auf {volume_percent}% gesetzt")
        except Exception as e:
            print(f"Fehler beim Einstellen der Lautstärke: {e}")
    
    def get_volume(self):
        """Gib die aktuelle Lautstärke als Prozent zurück"""
        return int(self.current_volume * 100)
    
    def is_musik_playing(self):
        """Prüfe ob Musik gerade abgespielt wird"""
        return self.is_playing and pygame.mixer.music.get_busy()
