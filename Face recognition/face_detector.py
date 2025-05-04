import cv2
import face_recognition
import numpy as np
import time
import lgpio
import RPi.GPIO as GPIO  # Import for servo control

DOOR_PIN = 18  # GPIO pin for relay
SERVO_PIN = 17  # GPIO pin for servo
CHIP = 0  # Default GPIO chip
h = lgpio.gpiochip_open(CHIP)
lgpio.gpio_claim_output(h, DOOR_PIN)
lgpio.gpio_write(h, DOOR_PIN, 0)  # Keep door locked

# Servo setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM
servo.start(0)  # Start with 0° position

# Function to set servo angle
def set_servo_angle(angle):
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Give the servo time to move
    servo.ChangeDutyCycle(0)  # Stop sending signal

# Load and encode face
known_image = face_recognition.load_image_file("my_face.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]
known_faces = [known_encoding]

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # Set width
cap.set(4, 240)  # Set height

frame_count = 0

print("Face recognition system is running...")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame_count += 1
        if frame_count % 5 != 0:  # Process every 5th frame
            continue

        # Convert to RGB and resize for faster processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.5, fy=0.5)

        # Detect faces
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, encoding)
            if True in matches:
                print("✅ Face recognized! Unlocking door & moving servo...")
                lgpio.gpio_write(h, DOOR_PIN, 1)  # Unlock door
                set_servo_angle(90)  # Move servo to open position
                
                time.sleep(5)  # Keep open for 5 seconds
                
                lgpio.gpio_write(h, DOOR_PIN, 0)  # Lock door again
                set_servo_angle(0)  # Move servo back to closed position
                print("🔒 Door locked & servo reset.")
            else:
                print("❌ Unknown face detected.")

except KeyboardInterrupt:
    print("\nStopping face recognition system...")

cap.release()
lgpio.gpiochip_close(h)  # Release GPIO
servo.stop()
GPIO.cleanup()  # Cleanup GPIO
