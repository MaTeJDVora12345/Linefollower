#include <Arduino.h>
#include <QTRSensors.h>

// ========= Deklarace pinů =========
const int encPin = 1;     
const int ledR = 14;      
const int ledG = 15;      
const int ledB = 13;      

// Piny senzorů (shodné s tvým zapojením)
const uint8_t sensorPins[] = {5, 6, 7, 8, 9, 10, 11, 12};
const uint8_t SensorCount = 8;

const int motorLDir = 4;  
const int motorLPwm = 3;  
const int motorRDir = 29; 
const int motorRPwm = 28; 

// ========= Objekty a globální proměnné =========
QTRSensors qtr;
uint16_t sensorValues[SensorCount];

volatile long rotations = 0;
float error = 0;
float previousError = 0;
float integral = 0;

// PID parametry
int baseSpeed = 40;     
float Kp = 0.0415; 
float Ki = 0.0;
float Kd = 0.2411; 

// Proměnná pro hlídání času operací
uint32_t lastLoopTime = 0;

// ========= Funkce =========

void encoderIrq() {
  if (digitalRead(encPin) == LOW) {
    rotations++;
  }
}

void setRGB(int r, int g, int b) {
  digitalWrite(ledR, r);
  digitalWrite(ledG, g);
  digitalWrite(ledB, b);
}

void setSpeed(int rSpeed, int lSpeed) {
  if (rSpeed < 0) {
    digitalWrite(motorRDir, HIGH); 
    analogWrite(motorRPwm, constrain(abs(rSpeed), 0, 255));
  } else {
    digitalWrite(motorRDir, LOW);
    analogWrite(motorRPwm, constrain(rSpeed, 0, 255));
  }

  if (lSpeed < 0) {
    digitalWrite(motorLDir, HIGH);
    analogWrite(motorLPwm, constrain(abs(lSpeed), 0, 255));
  } else {
    digitalWrite(motorLDir, LOW);
    analogWrite(motorLPwm, constrain(lSpeed, 0, 255));
  }
}

// ========= Setup =========
void setup() {
  pinMode(encPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encPin), encoderIrq, RISING);

  pinMode(ledR, OUTPUT);
  pinMode(ledG, OUTPUT);
  pinMode(ledB, OUTPUT);
  pinMode(motorLDir, OUTPUT);
  pinMode(motorRDir, OUTPUT);
  
  analogWriteRes(8); 
  analogWriteFrequency(motorLPwm, 1000);
  analogWriteFrequency(motorRPwm, 1000);

  qtr.setTypeRC();
  qtr.setSensorPins(sensorPins, SensorCount);

  setRGB(0, 0, 1); 
  for (uint16_t i = 0; i < 200; i++) {
    qtr.calibrate();
    delay(20);
  }
  setRGB(0, 0, 0); 
  delay(1000);
  
  // Inicializace času před startem smyčky
  lastLoopTime = micros();
}

// ========= Main Loop =========
void loop() {
  // STABILIZACE ČASU: Zbytek kódu se provede pouze jednou za 2000 mikrosekund (500 Hz)
  // To zabrání Teensy, aby "překmitalo" samo sebe a rozcukalo se.
  if (micros() - lastLoopTime < 2000) return; 
  lastLoopTime = micros();

  // Dynamická změna baseSpeed podle rotací (nyní probíhá plynule v čase)
  if (rotations > 30) {
    if (baseSpeed < 100) baseSpeed += 1;
  } else if (rotations > 20) {
    if (baseSpeed > 60) baseSpeed -= 1;
  }

  // Získání pozice od knihovny
  uint16_t position = qtr.readLineBlack(sensorValues);
  error = (float)position - 3500;

  // Detekce ztráty čáry pro barvu LED
  uint16_t sum = 0;
  for (int i=0; i<8; i++) sum += sensorValues[i];
  if (sum < 500) setRGB(1, 0, 0); else setRGB(0, 1, 0);

  // PID výpočet
  // Pokud nepoužíváš Ki, integrál nepotřebuješ.
  if (Ki != 0) {
    integral += error;
    integral = constrain(integral, -1000, 1000);
  } else {
    integral = 0;
  }

  float derivative = error - previousError;
  float correction = (Kp * error) + (Ki * integral) + (Kd * derivative);

  // Motory
  int rightSpeed = baseSpeed + (int)correction;
  int leftSpeed  = baseSpeed - (int)correction;

  setSpeed(rightSpeed, leftSpeed);
  
  previousError = error;
}