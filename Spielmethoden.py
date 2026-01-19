import time

class GameManager:
    def __init__(self, start_money=100, start_lives=20):
        # Initialisierung der Werte
        self.money = start_money
        self.lives = start_lives
        self.score = 0
        
        # Zeit-Management
        self.start_time = time.time()
        self.last_passive_income_time = time.time()
        
        # Konfiguration (Denkansatz)
        self.passive_income_interval = 5.0 # Alle 5 Sekunden Geld
        self.passive_income_amount = 10    # 10 Geld pro Intervall

    # ---------------------------------------------------------
    # 1. GELD (Money)
    # Methoden: Geld steigerung (durch Gegner oder Zeit)
    # ---------------------------------------------------------
    def add_money(self, amount):
        """Fügt Geld hinzu (z.B. wenn Gegner stirbt)."""
        self.money += amount
        print(f"Geld erhalten: +{amount}. Aktuell: {self.money}")

    def spend_money(self, amount):
        """Versucht Geld auszugeben. Gibt True zurück, wenn erfolgreich."""
        if self.money >= amount:
            self.money -= amount
            print(f"Geld ausgegeben: -{amount}. Aktuell: {self.money}")
            return True
        else:
            print("Nicht genug Geld!")
            return False

    def check_passive_income(self):
        """Prüft 'Überzeit', um Geld automatisch zu generieren."""
        current_time = time.time()
        if current_time - self.last_passive_income_time >= self.passive_income_interval:
            self.add_money(self.passive_income_amount)
            self.last_passive_income_time = current_time

    # ---------------------------------------------------------
    # 2. LEBEN (Lives)
    # Methoden: Leben verwalten
    # ---------------------------------------------------------
    def take_damage(self, amount=1):
        """Zieht Leben ab, wenn ein Gegner durchkommt."""
        self.lives -= amount
        print(f"Leben verloren! Aktuell: {self.lives}")
        
        if self.lives <= 0:
            self.game_over()

    def game_over(self):
        """Logik für das Spielende."""
        print("GAME OVER - Keine Leben mehr!")
        # Hier könntest du das Spiel stoppen oder ein Menü aufrufen
        
    # ---------------------------------------------------------
    # 3. SCORE
    # Denkansatz: Überzeit? Oder durch Kills?
    # ---------------------------------------------------------
    def add_score(self, points):
        """Erhöht den Score (z.B. durch Kill)."""
        self.score += points

    def update_score_over_time(self):
        """Optional: Gibt Punkte für jede überlebte Sekunde."""
        # Das kann man in der Loop aufrufen, z.B. +1 Punkt pro Sekunde
        self.score += 1

    # ---------------------------------------------------------
    # 4. ZEIT (Timer)
    # Methoden: Timer anzeigen
    # ---------------------------------------------------------
    def get_play_time(self):
        """Gibt die gespielte Zeit in Sekunden zurück."""
        return int(time.time() - self.start_time)

    def get_formatted_time(self):
        """Gibt die Zeit als String 'MM:SS' zurück."""
        seconds = self.get_play_time()
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"
    
    