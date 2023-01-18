/*
 * Thumb
 * - Большой палец
 * - Внутрь/наружу (aka thx)
 *   [   50;  180]
 * - Согнуть/разогнуть (aka thy)
 *   [    40;     150]
 * 
 * Index (aka ind)
 * - Указательный палец
 * - Согнуть/разогнуть
 *   [   180;       0]
 * 
 * Middle (aka mid)
 * - Средний палец 
 * - Cогнуть/разогнуть
 *   [   180;       0]
 * 
 * Pinky
 * - Мизиниец/безымянный палец
 * - Согнуть/разогнуть
 *   [     0;     180]
 */

#include <Servo.h>

#define IND 3 
#define MID 5 
#define PIK 6
#define THY 9
#define THX 10


struct Finger {
  int pin;
  int b, e;
  Servo m;

  void write(int value) {
    value = map(value, 0, 255, b, e);
    return m.write(value);
  }
};


Finger fings[] = {
  { THX, 180,  50 },
  { THY, 150,  40 },
  { IND,   0, 180 },
  { MID,   0, 180 },
  { PIK, 180,   0 },
};


void setup() {
  Serial.begin(115200);

  for (Finger fing : fings) {
    fing.m.attach(fing.pin);
    fing.write(0);
  }
}


void loop() {
  delay(100);
}
