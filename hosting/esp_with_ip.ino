void sendDataToServer(String trigger) {
  Serial.print("Trigger: ");
  Serial.println(trigger);

  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;

    HTTPClient http;

    // Initialize HTTP connection (Use the correct server endpoint)
    if (http.begin(client, "http://51.20.10.119//data")) {  // data address to send to cloud

      http.addHeader("Content-Type", "application/json");

      // Prepare JSON data
      String httpRequestData = "{\"api_key\":\"" + apiKeyValue +
                               "\",\"temperature\":\"" + String(temperature) +
                               "\",\"humidity\":\"" + String(humidity) +
                               "\",\"trigger\":\"" + trigger +
                               "\",\"relayStatus\":\"" + String(relayStatus) + "\"}";

      int httpResponseCode = http.POST(httpRequestData);

      if (httpResponseCode > 0) {
        String response = http.getString();  // Get the response to the request
        Serial.println(httpResponseCode);   // Print return code
        Serial.println(response);           // Print response
      }
      else {
        Serial.print("Error on sending POST: ");
        Serial.println(httpResponseCode);
      }

      http.end();  // Close connection
    }
    else {
      Serial.println("Unable to connect to server");
    }
  }
}
