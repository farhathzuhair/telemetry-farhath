#include <SPI.h>
#include <LoRa.h>

#define SS 5
#define RST 14
#define DIO0 26

void setup() {

  Serial.begin(115200);
  Serial.println("Gateway LoRa Receiver");

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa gagal start");
    while (1);
  }

  Serial.println("LoRa siap menerima");
}

void loop() {

  int packetSize = LoRa.parsePacket();

  if (packetSize) {

    String data = "";

    while (LoRa.available()) {
      data += (char)LoRa.read();
    }

    Serial.println("Data diterima:");
    Serial.println(data);

    int rssi = LoRa.packetRssi();

    Serial.print("Signal RSSI: ");
    Serial.println(rssi);

    Serial.println("-------------------");
  }
}