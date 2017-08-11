#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Ticker.h>
#include <SoftwareSerial.h>

char button = D3;

const char* ssid = "(V)Home";
const char* password = "s0l1c0n0baru";

char tagNumber[14];
String tagString;
boolean receivedTag;

Ticker secondTick;
volatile int watchdogCount = 0;

SoftwareSerial rfidReader(13,15);


void ISRwatchdog(){
  watchdogCount++;
  if (watchdogCount == 3){
    Serial.println();
    Serial.println("WATCHDOG RESET!");
    ESP.reset();
  }
}

void setup() {
  
  secondTick.attach(1, ISRwatchdog);

  pinMode(button, INPUT);
  pinMode(BUILTIN_LED, OUTPUT);
  digitalWrite(BUILTIN_LED, HIGH);
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
  rfidReader.begin(9600); // the RDM6300 runs at 9600bps
  Serial.println("\n\n\nRFID Reader...ready!");
}

void loop() {
  
  if (WiFi.status() == WL_CONNECTED){
    
    HTTPClient http;

    watchdogCount = 0;
      
    if(digitalRead(button) == LOW && digitalRead(BUILTIN_LED) == HIGH){
      
      digitalWrite(BUILTIN_LED, LOW);
      rfidReader.flush();

      http.begin("http://192.168.1.33:5002/device/11");
      http.addHeader("Content-Type", "application/json");
      int httpCode = http.POST("{\"is_on\":1,\"owner\": \"ESP\"}");
      Serial.println("POST sent (1)");

      Serial.println(httpCode);
      if (httpCode > 0){
        String response = http.getString();
        Serial.println(response);
      }
      http.end();
      delay(100);
    }
    while(rfidReader.available() && digitalRead(BUILTIN_LED) == LOW){
      
      int BytesRead = rfidReader.readBytesUntil(3, tagNumber, 15);
      receivedTag=true;
      if (receivedTag){
         
        tagString=tagNumber;
        
        Serial.println();
        Serial.print("Tag Number: ");
        Serial.println(tagString);
        
        http.begin("http://192.168.1.33:5002/device/11");
        http.addHeader("Content-Type", "application/json");
        int httpCode = http.POST("{\"is_on\":0,\"owner\": \""+tagString+"\"}");
        Serial.println("POST sent (0)");
  
        Serial.println(httpCode);
        if (httpCode > 0){
          String response = http.getString();
          Serial.println(response);
        }
        http.end();
        digitalWrite(BUILTIN_LED, HIGH);
        delay(100);
      }
    }
 }
}

