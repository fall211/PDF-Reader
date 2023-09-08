import pygame
import time
import threading
import os

class AudioQueue:

    def __init__(self):
        pygame.mixer.init()
        self.queue = []
        self.current_file = None
        self.is_playing = False
        self.thread = None
        self.is_paused = False

    def add_to_queue(self, audio_file):
        self.queue.append(audio_file)

    def start_thread(self):
        self.thread = threading.Thread(target=self.play)
        self.thread.start()

    def play(self):
        # check the queue every 5 seconds, if there is something in the queue, play it and remove once done
        # continue until the queue is empty and then resume checking every 5 seconds
        self.is_playing = True
        while self.is_playing:
            if self.is_paused:
                continue
            if len(self.queue) > 0:
                self.current_file = self.queue.pop(0)
                pygame.mixer.music.load(self.current_file)
                os.remove(self.current_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(1)
            else:
                time.sleep(5)

    def stop(self):
        self.is_playing = False
        pygame.mixer.music.stop()


    def pause(self):
        if pygame.mixer.music.get_busy():
            self.is_paused = True
            pygame.mixer.music.pause()
        else:
            self.is_paused = False
            pygame.mixer.music.unpause()


    def get_current_file(self):
        return self.current_file

    def get_queue(self):
        return self.queue
    
    def get_last_in_queue(self):
        return self.queue[-1]

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)



