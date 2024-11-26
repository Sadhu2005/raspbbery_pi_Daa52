import time
import signal
import sys
from adafruit_servokit import ServoKit
import speech_recognition as sr
import pygame
import os
import threading

# Initialize pygame for playing MP3 files
pygame.mixer.init()

# Initialize the ServoKit instance for the PCA9685 board
kit = ServoKit(channels=16)

# Function to move a single servo to a specified angle
def move_servo(channel, angle, delay=1):
    print(f"Setting servo on channel {channel} to angle {angle}")
    kit.servo[channel].angle = angle
    time.sleep(delay)

# Function to move left and right hand servos simultaneously
def move_hands(left_hand_angles, right_hand_angles, delay=0.5):
    for channel, angle in left_hand_angles.items():
        kit.servo[channel].angle = angle
    for channel, angle in right_hand_angles.items():
        kit.servo[channel].angle = angle
    time.sleep(delay)

# Function to perform the handshake action
def perform_handshake_action():
    def shake_hand():
        # Define the servo angles for the shaking motion
        right_hand_up = {1: 52}  # Raise the hand up
        right_hand_shake1 = {2: 150}  # Shake down slightly
        right_hand_shake2 = {2: 120}  # Shake down a bit more
        right_hand_down = {2: 0}  # Lower the hand down
        left_hand_down = {5: 180, 4: 150, 3: 90}  # Keep left hand in initial position

        # Raise the hand up
        move_hands(right_hand_up, left_hand_down)
        time.sleep(1)

        # Perform the shaking motion
        for i in range(3):
            move_hands(right_hand_shake1, left_hand_down)
            move_hands(right_hand_shake2, left_hand_down)
            move_hands(right_hand_shake1, left_hand_down)
 
        
        # Lower the hand down
        move_hands(right_hand_down, left_hand_down)
        print("Handshake action performed.")

    def speak_hello():
        for _ in range(2):
            pygame.mixer.music.load("/home/silentlover/voicemp3/hello friends.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            time.sleep(1)

    # Create threads for shaking hand and speaking hello
    shake_thread = threading.Thread(target=shake_hand)
    speak_thread = threading.Thread(target=speak_hello)

    # Start the threads
    shake_thread.start()
    speak_thread.start()

    # Wait for both threads to finish
    shake_thread.join()
    speak_thread.join()

# Test the handshake action
#perform_handshake_action()
