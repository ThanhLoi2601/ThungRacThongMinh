#include <LiquidCrystal_I2C.h>
#include <Servo.h>

#include <Blynk.h>
#include<ESP8266WiFi.h>
#define WIFI_SSID "Redmi Note 11"
#define WIFI_PASSWORD "hahahaha"

//kết nối blynkchar 
char ssid[] = "Redmi Note 11";
char pass[] = "hahahaha";
char auth[] = "uEXyRDz6wti8V6F3l7RTndWJI3yHzSlx";
#include <BlynkSimpleEsp8266.h>
BlynkTimer timer;
#define FaceInput V0
int face = 0;

//
int pos = 0;
int pos_temp = 0;

Servo servo_9;

int cm = 0;
int count[4];
int ct=0;
LiquidCrystal_I2C lcd(0x27, 16, 2);
long readUltrasonicDistance(int triggerPin, int echoPin)
{
  pinMode(triggerPin, OUTPUT); 
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  return pulseIn(echoPin, HIGH);
}

void setup()
{
  for(int i=0; i<4; i++) 
    count[i]=0;
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Blynk.begin(auth, ssid, pass);
  servo_9.attach(0);
  lcd.init(); 
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Count: ");
  lcd.setCursor(7, 0);
  lcd.print(ct);
}


BLYNK_CONNECTED() {
  Blynk.syncVirtual(V0);
}

BLYNK_WRITE(V0) {
  face = param.asInt();
}

void loop()
{
  // while (WiFi.status() != WL_CONNECTED){
  //   delay(500);
  //   Serial.print(".");
  // }
  cm = 0.01723 * readUltrasonicDistance(13, 12);
  if (cm <= 25 && cm != 0) {
    Serial.println(cm);
    servo_9.write(180);
    lcd.setCursor(7, 1);
    lcd.print("       "); 
    lcd.setCursor(7, 1);
    Blynk.virtualWrite(V0, face);
    if(face == 1)
    {
      count[0]++;
      lcd.print("Khoa");
      ct=count[0];
    }
    else if (face == 2)
    {
      count[1]++;
      lcd.print("Duc");
      ct=count[1];
    }
    else if (face == 3)
    {
      count[2]++;
      lcd.print("Loi");
      ct=count[2];
    }
    else
    {
      count[3]++;
      ct=count[3];
      lcd.print("None");
    }
    lcd.setCursor(7, 0);
    lcd.print("    "); 
    lcd.setCursor(7, 0);
    lcd.print(ct);
    delay(2000);
    lcd.setCursor(7, 1);
    lcd.print("Total"); 
    lcd.setCursor(7, 1);
    ct = count[0]+count[1]+count[2]+count[3];
    lcd.setCursor(7, 0);
    lcd.print("    "); 
    lcd.setCursor(7, 0);
    lcd.print(ct);
  } else {
    servo_9.write(0);
  }
}

