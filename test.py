import pygame
import time

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.mixer.init()
pygame.mixer.get_num_channels()

start_sound = pygame.mixer.Channel(1)
game_start = pygame.mixer.Sound("/home/sentinel/Desktop/MCI_Sentinel/gamestart.wav")
start_sound(game_start)

time.sleep(3)