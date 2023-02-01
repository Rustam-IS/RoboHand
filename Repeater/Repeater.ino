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


class Finger {

  public:
    int pin;
    int b, e;
    Servo m;
    int cur = -1;

  public:

    Finger(int pin, int b, int e) : 
      pin(pin), b(b), e(e) {}

    void attach(int port) {
      m.attach(port);
    }

    void write(int val, int sm = 7) {
      val = map(val, 0, 255, b, e);
      
      if (cur == -1) {
        m.write(val);
        cur = val;
      } else {    
        int dif = cur < val ? 1 : -1;
    
        for (
          int st = cur;
          st != val;
          st += dif
        ) {
          m.write(st);
          delay(sm);
        } cur = val;
      }
    }
};


Finger fings[] = {
  { THX, 180,  50 },
  { THY, 150,  40 },
  { IND,   0, 180 },
  { MID,   0, 180 },
  { PIK, 180,   0 },
};


const int BUFFER = 2;
unsigned char buf[BUFFER];


void setup() {
  Serial.begin(256000);

  for (Finger fing : fings) {
    fing.attach(fing.pin);
    fing.write(0);
  } 
}


void loop() {
  if (Serial.available()) {
    Serial.readBytes(buf, BUFFER);
    fings[buf[0]].write(buf[1]);
  }
}
