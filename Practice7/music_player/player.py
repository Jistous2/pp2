import pygame
import os


class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.playlist = []
        self.current_index = 0
        self.is_playing = False

        if os.path.isdir(music_dir):
            supported = (".mp3", ".wav", ".ogg")
            self.playlist = sorted(
                os.path.join(music_dir, f)
                for f in os.listdir(music_dir)
                if f.lower().endswith(supported)
            )

    def load_current(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_index])

    def play(self):
        if not self.playlist:
            return
        if not self.is_playing:
            self.load_current()
            pygame.mixer.music.play()
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.stop()
        self.play()

    def prev_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.stop()
        self.play()

    def current_track_name(self):
        if not self.playlist:
            return "No tracks found"
        return os.path.basename(self.playlist[self.current_index])

    def status(self):
        return "Playing" if self.is_playing else "Stopped"
