import pygame
import os

# Initialize pygame for playing MP3 files
pygame.mixer.init()

# Dictionary mapping questions to audio file paths
question_to_audio = {
    "what is your name": "/home/silentlover/voicemp3/what_is_your_name.mp3",
    "how are you": "/home/silentlover/voicemp3/how_are_you.mp3",
    # Add more questions and their corresponding audio file paths here
}

# Function to play an MP3 file
def play_mp3(file_path):
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print(f"File not found: {file_path}")

# Function to handle questions
def handle_question(command):
    if command in question_to_audio:
        play_mp3(question_to_audio[command])
        return True
    return False
