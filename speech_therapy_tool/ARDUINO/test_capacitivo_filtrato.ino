#include <CapacitiveSensor.h>

/*
 * CapitiveSense Library Demo Sketch
 * Paul Badger 2008
 * Uses a high value resistor e.g. 10 megohm between send pin and receive pin
 * Resistor effects sensitivity, experiment with values, 50 kilohm - 50 megohm. 
 Larger resistor values yield larger sensor values.
 * Receive pin is the sensor pin - try different amounts of foil/metal on this pin
 * Best results are obtained if sensor foil and wire is covered with an insulator 
 such as paper or plastic sheet
 */


CapacitiveSensor   cs_4_2 = CapacitiveSensor(4,2);        
// 10 megohm resistor between pins 4 & 2, pin 2 is sensor pin, add wire, foil
//CapacitiveSensor   cs_4_7 = CapacitiveSensor(4,7);        
//// 10 megohm resistor between pins 4 & 7, pin 7 is sensor pin, add wire, foil
//CapacitiveSensor   cs_4_8 = CapacitiveSensor(4,8);        
// 10 megohm resistor between pins 4 & 8, pin 8 is sensor pin, add wire, foil

void setup()                    
{

//   cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);     
//   // turn off autocalibrate on channel 1 - just as an example
   Serial.begin(115200);

}

void loop()                    
{
//    long start = millis();

    long total1 =  cs_4_2.capacitiveSensor(30);
//    long total2 =  cs_4_7.capacitiveSensor(30);
   // long total3 =  cs_4_8.capacitiveSensor(30);

//   Serial.print(millis() - start);        // check on performance in milliseconds
//   Serial.print("\t");                    // tab character for debug windown spacing

if (total1 > 30) {
  // do something here
  Serial.print("Y");
  Serial.println(total1);                  // print sensor output 1
//  total1=0;
  delay(10);
}


//    Serial.print("Y");
//    Serial.println(total1);                  // print sensor output 1
//    delay(100);
//    Serial.print("N");
//    Serial.println(total2);                  // print sensor output 2
 //   Serial.print("\t");
 //   Serial.println(total3);                // print sensor output 3

//    delay(50);                             // arbitrary delay to limit data to serial port 
}


