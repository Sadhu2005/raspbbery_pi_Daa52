import time
import signal
import sys
import pygame
import greeting_module
import face_recognition_client
import threading
import questions_module
import action_module
import commands_module

# Initialize pygame for playing MP3 files
pygame.mixer.init()

# Function to handle exit signal
def signal_handler(sig, frame):
    print('Exiting gracefully')
    actions_module.reset_servos()
    sys.exit(0)

# Attach the signal handler to SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Function to recognize faces and greet
def recognize_faces_and_greet():
    face_detection_client.start_face_recognition()

# Main function
def main():
    action_module.reset_servos()
    time.sleep(2)  # Wait for 2 seconds before starting actions
    greeting_module.play_greeting()
    questions_module.play_mp3("/home/silentlover/voicemp3/introduction.mp3")

    # Create threads for voice command listening and face recognition
    voice_thread = threading.Thread(target=commands_module.listen_for_commands)
    face_thread = threading.Thread(target=face_recognition_client)

    # Start the threads
    voice_thread.start()
    face_thread.start()

    # Wait for threads to complete
    voice_thread.join()
    face_thread.join()

if __name__ == "__main__":
    main()

