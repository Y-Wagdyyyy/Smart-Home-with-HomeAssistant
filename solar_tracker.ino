#include <Servo.h>

// Define LDR pins
const int LDR_Left = A0;   // Analog Pin A0
const int LDR_Right = A1;  // Analog Pin A1

// Servo setup
Servo solarServo;
const int servoPin = 9;  // PWM Pin for Servo

// Servo movement limits
int angle = 90;  // Start at 90° position
const int minAngle = 45;
const int maxAngle = 135;

// Sensitivity threshold
const int threshold = 50;  // Adjusted for 10-bit ADC

void setup() {
    Serial.begin(9600);
    solarServo.attach(servoPin);
    solarServo.write(angle);  // Set initial position
    delay(1000);  // Power stabilization delay
}

void loop() {
    // Read LDR values (10-bit ADC: 0-1023)
    int leftValue = analogRead(LDR_Left);
    int rightValue = analogRead(LDR_Right);

    Serial.print("Left: "); Serial.print(leftValue);
    Serial.print(" | Right: "); Serial.println(rightValue);

    // Compare LDR values and move servo accordingly
    if (leftValue > rightValue + threshold && angle < maxAngle) {
        angle += 2;  // Move right
    } 
    else if (rightValue > leftValue + threshold && angle > minAngle) {
        angle -= 2;  // Move left
    }

    // Update servo position smoothly
    solarServo.write(angle);
    delay(100);  // Small delay for stability
}
