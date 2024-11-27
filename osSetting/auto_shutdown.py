import os
import time
import psutil

# Define constants
AUTO_SHUTDOWN_TIME = 40 * 60  # 40 minutes in seconds
PROCESS_WAIT_TIME = 30  # Max wait time for processes
RESTART_DELAY = 120  # 2 minutes in seconds
BLUETOOTH_DEVICE_NAME = "YourBluetoothDevice"  # Replace with your device name
SOUND_FILE = "/path/to/your/sound.mp3"  # Replace with your MP3 file path

def notify_user(message):
    """Show a desktop notification."""
    os.system(f'notify-send "Raspberry Pi Alert" "{message}"')

def shutdown():
    """Shutdown the Raspberry Pi."""
    os.system("sudo shutdown now")

def restart():
    """Restart the Raspberry Pi after a cooling period."""
    os.system(f"sudo shutdown -r +{RESTART_DELAY // 60}")

def check_processes():
    """Check running processes and decide action."""
    running_processes = [p.info for p in psutil.process_iter(attrs=['pid', 'name']) if p.info['name'] not in ['bash', 'python3']]
    
    if not running_processes:
        return False

    total_wait_time = 0
    for process in running_processes:
        if total_wait_time < PROCESS_WAIT_TIME:
            time.sleep(1)
            total_wait_time += 1
        else:
            notify_user("Process running too long. Force shutdown!")
            for p in running_processes:
                try:
                    psutil.Process(p['pid']).terminate()
                except psutil.NoSuchProcess:
                    pass
            break
    return True

def check_bluetooth_connected():
    """Check if the Bluetooth device is connected."""
    result = os.popen("hcitool con").read()
    return BLUETOOTH_DEVICE_NAME in result

def play_robot_sound():
    """Play the robot sound if Bluetooth is connected."""
    if check_bluetooth_connected():
        os.system(f'mpg123 {SOUND_FILE}')
        notify_user("Robot sound played!")

def main():
    # Wait 30 seconds after boot
    time.sleep(30)
    play_robot_sound()

    start_time = time.time()
    
    while True:
        elapsed_time = time.time() - start_time
        
        if elapsed_time >= AUTO_SHUTDOWN_TIME:
            if check_processes():
                notify_user("Processes killed. Shutting down!")
            shutdown()
            time.sleep(RESTART_DELAY)  # Wait before restarting
            restart()
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
