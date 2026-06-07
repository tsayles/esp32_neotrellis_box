
/*** Buton_Cat

 This code is adapted from the Adafruit Adafruit NeoTrellis
 example shows basic usage of the NeoTrellis with the interrupt pin.
  The buttons will light up various colors when pressed.
***/

#include "Adafruit_NeoTrellis.h"

Adafruit_NeoTrellis trellis;

#include <HttpClient.h>
HttpClient http;

int debugLevel = 0;

float lightLevel = 0;
char resultstr[64];

// Headers currently need to be set at init, useful for API keys etc.
http_header_t headers[] = {
    { "Host", "mywebsite.com" },     // Declare the host here if your Spark has DNS problems
    { "Content-Type", "application/json" },
    { NULL, NULL } // NOTE: Always terminate headers will NULL
};

http_request_t request;
http_response_t response;

IPAddress HueBridgeIP(192,168,11,182); 


//#define INT_PIN D6

// Input a value 0 to 255 to get a color value.
// The colors are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return trellis.pixels.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return trellis.pixels.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return trellis.pixels.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}

//define a callback for key presses
TrellisCallback blink(keyEvent evt){
  
    Particle.publish("status", "called back", PRIVATE);

    if(evt.bit.EDGE == SEESAW_KEYPAD_EDGE_RISING)
    {
        trellis.pixels.setPixelColor(evt.bit.NUM, Wheel(map(evt.bit.NUM, 0, trellis.pixels.numPixels(), 0, 255))); //on rising
        trellis.pixels.show();
        Particle.publish("KeyPress", String::format("%u", evt.bit.NUM), PRIVATE);
        set_hue(evt.bit.NUM);
    }
    else if(evt.bit.EDGE == SEESAW_KEYPAD_EDGE_FALLING)
        trellis.pixels.setPixelColor(evt.bit.NUM, 0); //off falling
        trellis.pixels.show();
    
    
    return 0;
}


void setup() {
  if (debugLevel > 0) Particle.publish("Status", "Starting", PRIVATE);
    
  Serial.begin(9600);
  //while(!Serial);

  //pinMode(INT_PIN, INPUT);
  
  if(!trellis.begin()){
    Serial.println("could not start trellis");
    while(1);
  }
  else{
    Serial.println("trellis started");
  }

  //activate all keys and set callbacks
  for(int i=0; i<NEO_TRELLIS_NUM_KEYS; i++){
    trellis.activateKey(i, SEESAW_KEYPAD_EDGE_RISING);
    trellis.activateKey(i, SEESAW_KEYPAD_EDGE_FALLING);
    trellis.registerCallback(i, blink);
  }

  //do a little animation to show we're on
  for(uint16_t i=0; i<trellis.pixels.numPixels(); i++) {
    trellis.pixels.setPixelColor(i, Wheel(map(i, 0, trellis.pixels.numPixels(), 0, 255)));
    trellis.pixels.show();
    delay(50);
  }
  for(uint16_t i=0; i<trellis.pixels.numPixels(); i++) {
    trellis.pixels.setPixelColor(i, 0x000000);
    trellis.pixels.show();
    delay(50);
  }
  
  request.port = 80;
  if (debugLevel > 0) Particle.publish("Status", "Setup Done", PRIVATE);
  
  
}

void loop() {
  // put your main code here, to run repeatedly:
  trellis.read(true);
  delay(0.5);
}

void set_hue(int key)
{
    switch (key)
    {
        // Buttons are in rows: 0-3, 4-7, 8-11, 12-15
        
        case 0: // code to be executed if button 0 is pressed;
            // All lights off
            request.ip = HueBridgeIP;
            request.path = "/api/TSayles2014/groups/0/action";
            request.body = "{\"on\": false}";
            if (debugLevel > 0) Particle.publish("request.body", request.body, PRIVATE);
        
            
            http.put(request, response, headers);

            Serial.println(response.status);
            Serial.println(response.body);
            if (debugLevel > 0) Particle.publish("response.status", String::format("%u", response.status), PRIVATE);
            if (debugLevel > 0) Particle.publish("response.body", response.body, PRIVATE);
        
            delay(1000);
            
            break;
        case 1: // code to be executed if button 1 is pressed;
            // All lights on
            request.ip = HueBridgeIP;
            request.path = "/api/TSayles2014/groups/0/action";
            request.body = "{\"on\": true}";
            if (debugLevel > 0) Particle.publish("request.body", request.body, PRIVATE);
        
            
            http.put(request, response, headers);

            Serial.println(response.status);
            Serial.println(response.body);
            if (debugLevel > 0) Particle.publish("response.status", String::format("%u", response.status), PRIVATE);
            if (debugLevel > 0) Particle.publish("response.body", response.body, PRIVATE);
        
            delay(1000);
            
            break;
        case 4: // code to be executed if button 4 is pressed;
            // Bedroom on relax (soft orange)
            request.ip = HueBridgeIP;
            request.path = "/api/TSayles2014/groups/1/action";
            //request.body = "{\"on\": true}";
            request.body = "{\"hue\": 10000,\"sat\":196,\"bri\": 64,\"on\": true}";
            if (debugLevel > 0) Particle.publish("request.body", request.body, PRIVATE);
        
            
            http.put(request, response, headers);

            Serial.println(response.status);
            Serial.println(response.body);
            if (debugLevel > 0) Particle.publish("response.status", String::format("%u", response.status), PRIVATE);
            if (debugLevel > 0) Particle.publish("response.body", response.body, PRIVATE);
        
            delay(1000);
            break;
        
        case 5: // code to be executed if button 5 is pressed;
            // Bedroom on blue
            request.ip = HueBridgeIP;
            request.path = "/api/TSayles2014/groups/1/action";
            //request.body = "{\"on\": true}";
            request.body = "{\"on\": true,\"bri\": 56,\"hue\": 43690,\"sat\": 255}";
            if (debugLevel > 0) Particle.publish("request.body", request.body, PRIVATE);
        
            
            http.put(request, response, headers);

            Serial.println(response.status);
            Serial.println(response.body);
            if (debugLevel > 0) Particle.publish("response.status", String::format("%u", response.status), PRIVATE);
            if (debugLevel > 0) Particle.publish("response.body", response.body, PRIVATE);
        
            delay(1000);
            break;

        case 8: // code to be executed if button 8 is pressed;
            // Bedroom on bright
            request.ip = HueBridgeIP;
            request.path = "/api/TSayles2014/groups/1/action";
            //request.body = "{\"on\": true}";
            request.body = "{\"hue\": 34534,\"on\": true,\"bri\": 255}";
            if (debugLevel > 0) Particle.publish("request.body", request.body, PRIVATE);
        
            
            http.put(request, response, headers);

            Serial.println(response.status);
            Serial.println(response.body);
            if (debugLevel > 0) Particle.publish("response.status", String::format("%u", response.status), PRIVATE);
            if (debugLevel > 0) Particle.publish("response.body", response.body, PRIVATE);
        
            delay(1000);
            
            break;
        default: // code to be executed if n doesn't match any cases
        {
            
        }
    
    }
}
