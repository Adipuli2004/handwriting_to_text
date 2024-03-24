#include <Arduino_LSM9DS1.h>

const int switchPin = 2; // Define the pin to which the switch is connected
const String placeholder = "N/A"; // Placeholder string

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  pinMode(switchPin, INPUT); // Set switch pin as input with internal pull-up resistor

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");

  Serial.print("Gyroscope sample rate = ");
  Serial.print(IMU.gyroscopeSampleRate());
  Serial.println(" Hz");

  Serial.println();
  Serial.println("Acceleration (g's)\tGyroscope (deg/s)");
  Serial.println("X\tY\tZ\tX\tY\tZ");
}

void loop() {
  float accel_x, accel_y, accel_z;
  float gyro_x, gyro_y, gyro_z;

  // Read the state of the switch
  int switchState = digitalRead(switchPin);

  if (switchState == 1) {
    // Switch is ON, read accelerometer and gyroscope data
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      IMU.readAcceleration(accel_x, accel_y, accel_z);
      IMU.readGyroscope(gyro_x, gyro_y, gyro_z);

      Serial.print(accel_x);
      Serial.print('\t');
      Serial.print(accel_y);
      Serial.print('\t');
      Serial.print(accel_z);
      Serial.print('\t');
      Serial.print(gyro_x);
      Serial.print('\t');
      Serial.print(gyro_y);
      Serial.print('\t');
      Serial.println(gyro_z);
    }
  } else {
    // Switch is OFF, send placeholder
    Serial.println(placeholder);
  }

  // Delay for stability
}
