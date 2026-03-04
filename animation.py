import pygame


class SpriteAnimation:
    def __init__(self,image_path, frame_width, frame_height, frame_count, animation_speed):
        """
        image_path = Pfad zum Sprite Sheet
        frame_width = Breite eines einzelnen Frames
        frame_height = Höhe eines einzelnen Frames
        frame_count = Anzahl Frames im Sheet (horizontal)
        animation_speed = Zeit pro Frame in Millisekunden
        """
        self.image_path = image_path
        self.sprite_sheet = pygame.image.load(self.image_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.animation_speed = animation_speed

        self.frames = []
        self.current_frame = 0
        self.timer = 0

        self.load_frames()

    def load_frames(self):
        for i in range(self.frame_count):
            frame = self.sprite_sheet.subsurface(
                (i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            self.frames.append(frame)

    def update(self, dt):
        self.timer += dt
        while self.timer >= self.animation_speed:   # ← while statt if, falls dt > speed
            self.timer -= self.animation_speed
            self.current_frame = (self.current_frame + 1) % self.frame_count

    def draw(self, screen, x, y):
        screen.blit(self.frames[self.current_frame], (x, y))