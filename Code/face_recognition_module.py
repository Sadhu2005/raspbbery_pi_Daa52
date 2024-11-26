import cv2
import datetime
import subprocess

# Dictionary to store the last greeting time and "who are you" time for each person
last_greeting_time = {}
last_who_are_you_time = {}

def recognize_and_greet(frame, recognized_names, recognized_accuracies, face_locations):
    current_time = datetime.datetime.now()
    hour = current_time.hour

    for (top, right, bottom, left), name, accuracy in zip(face_locations, recognized_names, recognized_accuracies):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name and accuracy below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, f"{name} ({accuracy}%)", (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Greet the person if it's the first time in the current time slot
        if accuracy >= 48:
            if name not in last_greeting_time or (current_time - last_greeting_time[name]).total_seconds() > 3600 * 6:  # 6 hours
                if hour < 12:
                    greeting = f"Good morning, {name}."
                elif hour < 18:
                    greeting = f"Good afternoon, {name}."
                else:
                    greeting = f"Good evening, {name}."
                subprocess.run(["flite", "-t", greeting])
                last_greeting_time[name] = current_time
        # Ask "who are you" if the accuracy is low and it's the first time in the day
        elif name not in last_who_are_you_time or (current_time - last_who_are_you_time[name]).days > 0:
            subprocess.run(["flite", "-t", "Who are you?"])
            last_who_are_you_time[name] = current_time

    return frame
