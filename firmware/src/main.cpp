/**
 * @file main.cpp
 * @brief ESP32 NeoTrellis Box — entry point
 *
 * Initialises hardware peripherals, WiFi, MQTT,
 * and the NeoTrellis keypad, then enters the main
 * loop.
 */

#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 NeoTrellis Box starting...");

  // TODO: Initialise NeoTrellis over I2C
  // TODO: Initialise WiFi manager
  // TODO: Initialise MQTT client
  // TODO: Initialise web server
  // TODO: Initialise OTA updater
}

void loop() {
  // TODO: Poll NeoTrellis for button events
  // TODO: Process MQTT messages
  // TODO: Update LED status
}
