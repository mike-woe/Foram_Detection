// Arduino code for pressure box

int SOLENOID_1 = 13;
int SOLENOID_2 = 12;
int SOLENOID_3 = 11;
int SOLENOID_4 = 10;
int data;

void setup() {
  Serial.begin(9600);
  pinMode(SOLENOID_1, OUTPUT);
  pinMode(SOLENOID_2, OUTPUT);
  pinMode(SOLENOID_3, OUTPUT);
  pinMode(SOLENOID_4, OUTPUT);
  digitalWrite(SOLENOID_1, LOW);
  digitalWrite(SOLENOID_2, LOW);
  digitalWrite(SOLENOID_3, LOW);
  digitalWrite(SOLENOID_4, LOW);
}

void loop() {
  data = Serial.read();

  switch (data) {
    case '1':
      digitalWrite(SOLENOID_1, LOW);
      digitalWrite(SOLENOID_2, HIGH);
      Serial.println("Solenoid 1 opened");
      break;
    case '2':
      digitalWrite(SOLENOID_1, HIGH);
      digitalWrite(SOLENOID_2, LOW);
      Serial.println("Solenoid 2 opened");
      break;
    case '3':
      digitalWrite(SOLENOID_1, HIGH);
      digitalWrite(SOLENOID_2, HIGH);
      Serial.println("Both solenoids opened");
      break;

    case '0':
      digitalWrite(SOLENOID_1, LOW);
      digitalWrite(SOLENOID_2, LOW);
      Serial.println("Both solenoids closed");
      break;
  }
}
