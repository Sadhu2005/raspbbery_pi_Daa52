import time
from adafruit_servokit import ServoKit

# Initialize the ServoKit instance for the PCA9685 board
kit = ServoKit(channels=16)

# Function to move a single servo to a specified angle
def move_servo(channel, angle, delay=1):
    print(f"Setting servo on channel {channel} to angle {angle}")
    kit.servo[channel].angle = angle
    time.sleep(delay)

# Function to reset all servos to their initial positions
def reset_servos():
    initial_positions = [144, 67, 22, 85, 103, 173, 86, 141, 106, 83, 56, 104, 122, 148, 142, 123]
    for channel, angle in enumerate(initial_positions):
        move_servo(channel, angle, delay=0.5)

# Function to move left and right hand servos simultaneously
def move_hands(left_hand_angles, right_hand_angles, delay=0.5):
    for channel, angle in left_hand_angles.items():
        kit.servo[channel].angle = angle
    for channel, angle in right_hand_angles.items():
        kit.servo[channel].angle = angle
    time.sleep(delay)

def perform_hi_action():
    right_hand_up = {2: 180, 1: 30, 0: 150}
    right_hand_bend = {2: 180, 1: 0, 0: 90}
    right_hand_down = {2: 0, 1: 45, 0: 150}
    left_hand_down = {5: 180, 4: 150, 3: 90}
    move_hands(right_hand_up, left_hand_down)
    time.sleep(1)
    for _ in range(2):
        move_hands(right_hand_bend, left_hand_down)
        play_mp3("/home/silentlover/voicemp3/hello.mp3")
        move_hands(right_hand_up, left_hand_down)
    move_hands(left_hand_down, right_hand_down)

def perform_left_right_left_action():
    left_hand_up = {5: 0, 4: 150, 3: 90}
    right_hand_up = {2: 180, 1: 30, 0: 150}
    left_hand_down = {5: 180, 4: 150, 3: 90}
    right_hand_down = {2: 0, 1: 45, 0: 150}

    move_hands(left_hand_up, right_hand_down)
    play_mp3("/home/silentlover/voicemp3/left.mp3")
    time.sleep(1)
    move_hands(left_hand_down, right_hand_up)
    play_mp3("/home/silentlover/voicemp3/right.mp3")
    time.sleep(1)
    move_hands(left_hand_up, right_hand_down)
    play_mp3("/home/silentlover/voicemp3/left.mp3")
    time.sleep(1)
    move_hands(left_hand_down, right_hand_down)
