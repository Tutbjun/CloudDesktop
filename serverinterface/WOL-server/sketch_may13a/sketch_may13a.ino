#define socketCnt 4

const uint8_t socketPins[socketCnt] = {
  3,
  4,
  5,
  6
};

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < socketCnt; i++){
    pinMode(socketPins[i], OUTPUT);
    digitalWrite(socketPins[i], LOW);
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
