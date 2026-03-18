#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>

// ================== PIN SENSOR ==================
#define DHTPIN 4
#define DHTTYPE DHT22

#define SOIL_PIN 34
#define LDR_PIN 35

// ================== PIN LORA ==================
#define SS 5
#define RST 14
#define DIO0 26

// ================== OBJECT SENSOR ==================
DHT dht(DHTPIN, DHTTYPE);

// ID perangkat
String deviceID = "01";

void setup() {

  Serial.begin(115200);
  Serial.println("Node Pengirim LoRa");

  dht.begin();

  // set pin LoRa
  LoRa.setPins(SS, RST, DIO0);

  // frekuensi LoRa
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa gagal start");
    while (1);
  }

  Serial.println("LoRa siap mengirim");
}

void loop() {

  // ====== BACA SENSOR ======
  float suhu = dht.readTemperature();
  float kelembapan = dht.readHumidity();

  int soil = analogRead(SOIL_PIN);
  int cahaya = analogRead(LDR_PIN);

  // ====== FORMAT DATA ======
  String data = "ID:" + deviceID +
                ",T:" + String(suhu) +
                ",H:" + String(kelembapan) +
                ",SM:" + String(soil) +
                ",L:" + String(cahaya);

  // ====== PRINT KE SERIAL ======
  Serial.print("Data dikirim: ");
  Serial.println(data);

  // ====== KIRIM VIA LORA ======
  LoRa.beginPacket();
  LoRa.print(data);
  LoRa.endPacket();

  Serial.println("Data terkirim");
  Serial.println("------------------");

  delay(5000);
}