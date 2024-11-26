import cv2
import socket
import pickle
import struct
from face_recognition_module import recognize_and_greet

# Initialize the video capture
video_capture = cv2.VideoCapture(0)

# Server IP and port
server_ip = '192.168.4.163'  # Replace with the server's IP address
server_port = 8000

# Create a socket connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Serialize frame
    _, image_data = cv2.imencode('.jpg', small_frame)
    data = pickle.dumps(image_data)
    message_size = struct.pack("Q", len(data))
    
    # Send frame data to server
    client_socket.sendall(message_size + data)
    
    # Receive recognition results from server
    try:
        response_size_data = client_socket.recv(8)
        if len(response_size_data) < 8:
            print("Received incomplete response size data.")
            break
        response_size = struct.unpack("Q", response_size_data)[0]
        
        response_data = b""
        while len(response_data) < response_size:
            packet = client_socket.recv(response_size - len(response_data))
            if not packet:
                print("Received incomplete response data.")
                break
            response_data += packet
        
        if len(response_data) != response_size:
            print("Incomplete data received.")
            continue

        recognized_names, recognized_accuracies, face_locations = pickle.loads(response_data)
        
        # Recognize and greet the person
        frame = recognize_and_greet(frame, recognized_names, recognized_accuracies, face_locations)
        
        # Display the resulting image
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    except Exception as e:
        print(f"Error: {e}")
        break

# Release the video capture and close windows
video_capture.release()
cv2.destroyAllWindows()
client_socket.close()
