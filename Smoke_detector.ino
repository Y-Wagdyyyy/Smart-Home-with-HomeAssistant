#include <DHT.h>

#define DHT_PIN 2       // Connect DHT11 data pin to Arduino pin 2
#define DHT_TYPE DHT11  // Define sensor type

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(9600);
    Serial.println("DHT11 Test Start...");
    dht.begin();
}

void loop() {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("Error reading from DHT11!");
        return;
    }

    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print("°C  |  Humidity: ");
    Serial.print(humidity);
    Serial.println("%");

    delay(2000);  // Wait 2 seconds
}
