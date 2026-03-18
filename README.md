# Telemetry LoRa System (ESP32)

Sistem telemetry berbasis LoRa untuk mengirim dan menerima data sensor **DHT22 (suhu & kelembaban)** dan **soil moisture (kelembaban tanah)** menggunakan ESP32 dan modul LoRa eksternal.

---

## 📌 Deskripsi

Proyek ini mengimplementasikan komunikasi jarak jauh menggunakan teknologi LoRa untuk monitoring kondisi lingkungan secara real-time. Data sensor dikirim dari node transmitter ke receiver, kemudian dapat ditampilkan atau diproses lebih lanjut.

---

## ⚙️ Teknologi yang Digunakan

* ESP32
* LoRa Module (SX127x)
* Sensor DHT22
* Sensor Soil Moisture
* Arduino IDE / PlatformIO

---

## 🧠 Arsitektur Sistem

[Sensor] → [ESP32 Transmitter] → [LoRa] → [ESP32 Receiver] → [Output / Monitoring]

* Transmitter membaca data sensor
* Data dikirim melalui LoRa
* Receiver menerima dan menampilkan data

---

## 🔌 Konfigurasi Hardware

### Sensor DHT22

* VCC → 3.3V
* GND → GND
* DATA → GPIO (sesuai kode)

### Soil Moisture

* VCC → 3.3V / 5V
* GND → GND
* AOUT → GPIO ADC

### LoRa (SX1278 / SX1276)

* MISO → GPIO19
* MOSI → GPIO23
* SCK → GPIO18
* NSS → GPIO5
* RST → GPIO14
* DIO0 → GPIO2

---

## 🚀 Cara Menjalankan

1. Install Arduino IDE
2. Install Board ESP32
3. Install library:

   * LoRa
   * DHT sensor library
4. Upload kode:

   * `transmitter.ino` ke ESP32 pengirim
   * `receiver.ino` ke ESP32 penerima
5. Buka Serial Monitor untuk melihat data

---

## 📊 Contoh Data Output

Temperature: 30°C
Humidity: 70%
Soil Moisture: 450

---

## ⚠️ Catatan Penting

* Pastikan frekuensi LoRa sesuai (433 / 915 MHz)
* Gunakan antenna untuk jangkauan optimal
* Perhatikan power supply agar stabil

---

## 🎯 Tujuan Proyek

* Implementasi komunikasi LoRa
* Monitoring lingkungan berbasis IoT
* Pembelajaran sistem telemetry jarak jauh

---

## 👤 Author

Farhath

---
