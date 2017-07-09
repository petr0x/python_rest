#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Ticker.h>

#define LED_PIN 16
#define WAIT 5
#define WAIT_END 4

const char* ssid = "(V)Home";
const char* password = "s0l1c0n0baru";

Ticker secondTick;
volatile int watchdogCount = 0;


void ISRwatchdog(){
  watchdogCount++;
  if (watchdogCount == 5){
    Serial.println();
    Serial.println("WATCHDOG RESET!");
    ESP.reset();
  }
}

void setup() {
  
  secondTick.attach(1, ISRwatchdog);

  pinMode(LED_PIN, OUTPUT);
  pinMode(WAIT, INPUT);
  pinMode(WAIT_END, INPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  Serial.println(); 
  Serial.print("Connecintg.");

  while (WiFi.status() != WL_CONNECTED){
    delay(100);
    Serial.print(".");
  }
  Serial.println(); 
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED){
    
    HTTPClient http;

    watchdogCount = 0;

    if(digitalRead(WAIT) == HIGH && digitalRead(LED_PIN) == LOW){
      
      digitalWrite(LED_PIN, HIGH);

      http.begin("http://192.168.1.33:5002/device/33");
      http.addHeader("Content-Type", "application/json");
      int httpCode = http.POST("{\"is_on\":1,\"owner\": \"ESP\"}");
      Serial.println("POST sent (1)");

      Serial.println(httpCode);
      if (httpCode > 0){
        String response = http.getString();
        Serial.println(response);
      }
      http.end();
    }
    if(digitalRead(WAIT_END) == HIGH && digitalRead(LED_PIN) == HIGH){
      
      digitalWrite(LED_PIN, LOW);

      http.begin("http://192.168.1.33:5002/device/33");
      http.addHeader("Content-Type", "application/json");
      int httpCode = http.POST("{\"is_on\":0,\"owner\": \"ESP\"}");
      Serial.println("POST sent (0)");

      Serial.println(httpCode);
      if (httpCode > 0){
        String response = http.getString();
        Serial.println(response);
      }
      http.end();
    }
  }
}


