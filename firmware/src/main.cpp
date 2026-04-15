#include <Arduino.h>
#include <Servo.h>

bool parseAngles(const String& line, int output[5]);

// Create servo objects for each finger.
Servo thmb;
Servo pntr;
Servo midl;
Servo ring;
Servo pink;

// Min angles
const int THMB_MIN = 0;
const int PNTR_MIN = 0;
const int MIDL_MIN = 0;
const int RING_MIN = 0;
const int PINK_MIN = 0;

// Servo-safe max angles
const int THMB_MAX = 150;
const int PNTR_MAX = 170;
const int MIDL_MAX = 170;
const int RING_MAX = 170;
const int PINK_MAX = 170;

// Current angles
int thmb_pos = 0;
int pntr_pos = 0;
int midl_pos = 0;
int ring_pos = 0;
int pink_pos = 0;

String incomingLine = "";

void setup() {
  Serial.begin(9600);

  // Attach each servo obj to corresponding analog and digital pins.
  thmb.attach(5);
  pntr.attach(4);
  midl.attach(3);
  ring.attach(2);
  pink.attach(A0);

  // Initialize positions to 0 deg.
  thmb.write(thmb_pos);
  pntr.write(pntr_pos);
  midl.write(midl_pos);
  ring.write(ring_pos);
  pink.write(pink_pos);
}

void loop() {
  if (Serial.available() > 0) {
    incomingLine = Serial.readStringUntil('\n');
    incomingLine.trim();

    int parsed[5];
    if (parseAngles(incomingLine, parsed)) {
      // Parsed order: [thumb, pointer, middle, ring, pinky]
      thmb_pos = constrain(parsed[0], THMB_MIN, THMB_MAX);
      pntr_pos = constrain(parsed[1], PNTR_MIN, PNTR_MAX);
      midl_pos = constrain(parsed[2], MIDL_MIN, MIDL_MAX);
      ring_pos = constrain(parsed[3], RING_MIN, RING_MAX);
      pink_pos = constrain(parsed[4], PINK_MIN, PINK_MAX);

      thmb.write(thmb_pos);
      pntr.write(pntr_pos);
      midl.write(midl_pos);
      ring.write(ring_pos);
      pink.write(pink_pos);
    }
  }
}

// Angle parser: "thumb,pointer,middle,ring,pinky"
bool parseAngles(const String& line, int output[5]) {
  int first = line.indexOf(',');
  int second = line.indexOf(',', first + 1);
  int third = line.indexOf(',', second + 1);
  int fourth = line.indexOf(',', third + 1);

  if (first == -1 || second == -1 || third == -1 || fourth == -1) {
    return false;
  }

  // Thumb to pinky
  output[0] = line.substring(0, first).toInt();             // Thumb
  output[1] = line.substring(first + 1, second).toInt();    // Index
  output[2] = line.substring(second + 1, third).toInt();    // Middle
  output[3] = line.substring(third + 1, fourth).toInt();    // Ring
  output[4] = line.substring(fourth + 1).toInt();           // Pinky

  return true;
}
