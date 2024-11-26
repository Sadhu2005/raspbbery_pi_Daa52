import speech_recognition as sr
import pygame
import os
import questions_module
import actions_module
import action_trail

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

# Function to listen for voice commands
def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")
            if questions_module.handle_question(command):
                continue
            elif command == "say hello":
                actions_module.perform_hi_action()
            elif command == "do left right left":
                actions_module.perform_left_right_left_action()
            elif command == "give handshake":
                action_trail.perform_handshake_action()
            elif command == "exit":
                play_mp3("/home/silentlover/voicemp3/exiting.mp3")
                return
            else:
                play_mp3("/home/silentlover/voicemp3/unrecognized_command.mp3")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
