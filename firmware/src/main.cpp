#include <Arduino.h>
#include <Servo.h>

void open_close_servo(Servo& finger, int& finger_pos);

// Create servo objects for each finger.
Servo pink;
Servo ring;
Servo midl;
Servo pntr;
Servo thmb;

// Initialize each finger position to 0 deg.
int pink_pos = 0;
int ring_pos = 0;
int midl_pos = 0;
int pntr_pos = 0;
int thmb_pos = 0;

void setup() {
  Serial.begin(9600);

  // Attach each servo obj to corresponding analog and digital pins.
  pink.attach(A0);
  ring.attach(2);
  midl.attach(3);
  pntr.attach(4);
  thmb.attach(5);
}

void loop() {
  // SG90 Test
  // Ensure all servos are open to 0 deg.
  pink.write(pink_pos);
  ring.write(ring_pos);
  midl.write(midl_pos);
  pntr.write(pntr_pos);
  thmb.write(thmb_pos);

  // Close each finger to 150 deg, then open each finger to 0 deg.
  delay(1000);
  open_close_servo(pink, pink_pos);
  delay(1000);

  delay(1000);
  open_close_servo(ring, ring_pos);
  delay(1000);

  delay(1000);
  open_close_servo(midl, midl_pos);
  delay(1000);

  delay(1000);
  open_close_servo(pntr, pntr_pos);
  delay(1000);

  delay(1000);
  open_close_servo(thmb, thmb_pos);
  delay(1000);
}

// SG90 Servo Test
void open_close_servo(Servo& finger, int& finger_pos) {
  if (finger_pos == 0) {
    finger_pos = 150;
  } else {
    finger_pos = 0;
  }
  finger.write(finger_pos);
}
