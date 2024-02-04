#define socketCnt 4
#define inverseLogic false

const uint8_t socketPins[socketCnt] = {
  3,
  4,
  5,
  2
};

bool staticIP = true;

#define rstPin 6

#include <SPI.h>
#include <Ethernet.h>

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
IPAddress ip(192, 168, 0, 89);
IPAddress myDns(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

// telnet defaults to port 23
EthernetServer server(23);

EthernetClient clients[8];

String DisplayAddress(IPAddress address)
{
 return String(address[0]) + "." + 
        String(address[1]) + "." + 
        String(address[2]) + "." + 
        String(address[3]);
}

bool connectionEstablished = false;

void (*resetFunc) (void) = 0;

void ethernetStartup(){
  return ethernetStartup(0);
}

void ethernetStartup(int itters){
  // initialize the Ethernet device
  if (itters > 100)
    return;
  bool connection = false;
  while (!connection){
    delay(1000);
    if (!connectionEstablished)
      Serial.println("Establishing connection...");
    else
      Serial.println("Checking connection...");
    if (staticIP){
      Ethernet.begin(mac, ip);//, ip, myDns, gateway, subnet
      connection = true;
    }
    else{
      connection = (bool)Ethernet.begin(mac);//, ip, myDns, gateway, subnet
      Serial.println("state = " + (String)connection);
    }
    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    }
  
    // start listening for clients
    server.begin();

    String ip = DisplayAddress(Ethernet.localIP());
    if (!connectionEstablished){
      Serial.print("WOL-server address:");
      Serial.println(ip);
    }
    if (ip == "0.0.0.0"){
      delay(1000);
      connection = false;
      connectionEstablished = false;
      ethernetStartup(itters+1);
      //resetFunc();
    }
    else if (connectionEstablished)
      Serial.println("Connection fine");
    else
      connectionEstablished = true;
  }
}

void setup() {
  delay(10000);
  pinMode(rstPin,OUTPUT);
  digitalWrite(rstPin,HIGH);
  for (int i = 0; i < socketCnt; i++){
    pinMode(socketPins[i], OUTPUT);
    #if inverseLogic
      digitalWrite(socketPins[i], LOW);
    #else
      digitalWrite(socketPins[i], HIGH);
    #endif
  }
  
  

  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  ethernetStartup();
}

void powerOnOff(int8_t pin, bool pinState){
  #if inverseLogic
    pinState = !pinState;
  #endif
  if (pin >= 0){
    Serial.print("setting pin #");
    Serial.println(socketPins[pin]);
    digitalWrite(socketPins[pin],pinState);
  }
}

String doCmd(String cmd){
  if (cmd == "0_on"){
    powerOnOff(0, HIGH);
    return "did a thing";
  }
  else if (cmd == "0_off"){
    powerOnOff(0, LOW);
    return "did a thing";
  }
  else if (cmd == "1_on"){
    powerOnOff(1, HIGH);
    return "did a thing";
  }
  else if (cmd == "1_off"){
    powerOnOff(1,LOW);
    return "did a thing";
  }
  else if (cmd == "2_on"){
    powerOnOff(2,HIGH);
    return "did a thing";
  }
  else if (cmd == "2_off"){
    powerOnOff(2,LOW);
    return "did a thing";
  }
  else if (cmd == "3_on"){
    powerOnOff(3,HIGH);
    return "did a thing";
  }
  else if (cmd == "3_off"){
    powerOnOff(3,LOW);
    return "did a thing";
  }
  return "waiting for things...";
}

String recv = "";
String lastRecv = "";

char int2Char(uint8_t in){
  char out = (char)in;
  return out;
}

uint16_t ethernetCheckupClock = 0;

void loop() {
  ethernetCheckupClock++;
  delay(1);
  if (ethernetCheckupClock == 0)//aproximately every minute
    ethernetStartup();
  // check for any new client connecting, and say hello (before any incoming data)
  EthernetClient newClient = server.accept();
  if (newClient) {
    for (byte i=0; i < 8; i++) {
      if (!clients[i]) {
        Serial.print("We have a new client #");
        Serial.println(i);
        newClient.print("Hello, client number: ");
        newClient.println(i);
        // Once we "accept", the client is no longer tracked by EthernetServer
        // so we must store it into our list of clients
        clients[i] = newClient;
        break;
      }
    }
  }

  // check for incoming data from all clients
  for (byte i=0; i < 8; i++) {
    String msg = "";
    if (clients[i].available() > 0){
      Serial.println("msg started...");
      while (true){
        int additionalMsg = clients[i].read();
        if (additionalMsg > 0){
          Serial.print("Recieved: ");
          Serial.println(additionalMsg);
          if (additionalMsg == 8){
            if (msg.length() > 0){
              msg.remove(msg.length()-1);
            }
          }
          else if (additionalMsg == 13){
            delay(100);
            uint8_t timeout = 10;
            uint8_t cnt = 0;
            while (clients[i].available() > 0 && cnt < timeout){
              //msg += int2Char(additionalMsg);
              delay(10);
              cnt++;
            }
            break;
          }
          else if (additionalMsg == 10){
            break;
          }
          else{
            msg += int2Char(additionalMsg);
          }
          Serial.print("Current msg: ");
          Serial.println(msg);
        }
      }
      //msg += "\n";
      if (msg != "")
        Serial.println(msg);
        recv = msg;
    }
    if (recv != lastRecv && recv != ""){
      Serial.println("doing cmd with string: ");
      Serial.println(recv);
      Serial.println(doCmd(recv));
      lastRecv = recv;
      break;
    }
  }

  //check for serial messages to send
  if (Serial.available()){
    String msg = Serial.readStringUntil("\n");
    for (uint8_t i = 0; i < 8; i++){
      if (clients[i].available()){
        clients[i].println(msg);
      }
    }
  }

  // stop any clients which disconnect
  for (byte i=0; i < 8; i++) {
    if (clients[i] && !clients[i].connected()) {
      Serial.print("disconnect client #");
      Serial.println(i);
      clients[i].stop();
    }
  }
}
