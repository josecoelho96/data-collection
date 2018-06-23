#include <DHT_U.h>

#define DHTTYPE DHT22 // DHT 22  (AM2302)

// Pin connections
const int ldrPin = A6;
const int dhtPin = A5;
char dataString[50] = {0};

DHT dht(dhtPin, DHTTYPE);

void setup() {
  pinMode(ldrPin, INPUT);
  dht.begin();
  Serial.begin(9600);
}

void loop() {

  char inChar;
  int ldrReading;
  float humidityReading;
  float temperatureReading;

  if (Serial.available() > 0) {
    // Bytes to be read
    inChar = Serial.read();
    if (inChar == '1') {
      // Get data from sensors
      ldrReading = analogRead(ldrPin);
      humidityReading = dht.readHumidity();
      temperatureReading = dht.readTemperature();

      sprintf(dataString,"L:%d|T:%d|H:%d",ldrReading, (int)temperatureReading, (int)humidityReading);

      Serial.println(dataString);
    } else {
      Serial.println("Instruction not defined!");
    }
  }
}
