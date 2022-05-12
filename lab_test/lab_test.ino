#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

#include <ESP8266WiFi.h>

#ifndef STASSID
#define STASSID wifi_id
#define STAPSK  password
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

const char * host = ip; // Server ip
const uint16_t port = port; // Port

WiFiClient client;

void setup() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password); // Try to connect to the internet.

  Serial.begin(115200);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  } // Keep trying to connect to the internet.

  client.connect(host, port); // Connect to server.
  delay(100);
  client.print("b"); // Send identification id.

  Wire.begin();
  byte status = mpu.begin();
  // Try to initialize!
  if (!status) {
    Serial.println("Failed to find MPU6050 chip");
    while (status != 0) {
    }
  }
  Serial.println("MPU6050 Found!");

  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  mpu.calcOffsets(true,true); // gyro and accelero
  Serial.println("Done!\n");
}

void loop() {
  if (client.connected()) { // If connected to the server.
    mpu.update();
    String value = "a"+String(mpu.getAccX())+","+String(mpu.getAccY())+","+String(mpu.getAccZ());
    String ang = "b"+String((int)mpu.getAngleX())+","+String((int)mpu.getAngleY())+","+String((int)mpu.getAngleZ());
    client.print(value);
    delay(100);
    client.print(ang);
    delay(100);
  } else { // If not connected to the server.
    client.connect(host, port); // Connect to the server on the given host and port.
    client.print("b"); // Send the proper id.
  }
}
