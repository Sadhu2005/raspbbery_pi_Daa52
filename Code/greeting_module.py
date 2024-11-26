import time
import signal
import sys
from adafruit_servokit import ServoKit
import speech_recognition as sr
import pygame
import os
import datetime


# Initialize pygame for playing MP3 files
pygame.mixer.init()

# Function to play an MP3 file
def play_mp3(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print(f"File not found: {file_path}")
#play_mp3("/home/silentlover/voicemp3/k namaste.mp3")
def play_greeting():
    # Initialize the mixer module
    #pygame.mixer.init()

    # Get the current hour
    current_hour = datetime.datetime.now().hour

    # Determine the appropriate greeting based on the hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
        play_mp3("/home/silentlover/voicemp3/good morning.mp3")
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
        play_mp3("/home/silentlover/voicemp3/good afternoon.mp3")
    elif 17 <= current_hour < 21:
        greeting = "Good Evening"
        play_mp3("/home/silentlover/voicemp3/good evevning.mp3")
    else:
        greeting = "Good Night"
        play_mp3("/home/silentlover/voicemp3/k namaste.mp3")

#play_greeting()
