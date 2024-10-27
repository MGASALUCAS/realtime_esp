#include <ESP8266HTTPClient.h>
#include <WiFi.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* serverName = "http://YOUR_FLASK_SERVER_IP:5000/api/post_data";  // Change YOUR_FLASK_SERVER_IP

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
}

void loop() {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Example sensor data
    String jsonData = "{\"value1\":\"25\",\"value2\":\"60\",\"value3\":\"1015\"}";
    
    int httpResponseCode = http.POST(jsonData);
    
    if(httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.println("Error on sending POST");
    }

    http.end();
  }

  delay(10000);  // Send data every 10 seconds
}
