#include <LiquidCrystal.h>


#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnRIGHT  4
#define btnSELECT 5
#define btnNONE   6

String potionsName[6];
int potionsNumber[6];

int choix = 0;
bool tour = false;

// Initialise l'afficheur
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
 
void setup() {
   lcd.begin(16, 2);
   
   Serial.begin(9600);
   
   lcd.clear();
}
 
void loop() {
  potionsName[0] = "fov-increase"; potionsNumber[0] = 0;
  potionsName[1] = "magnet";       potionsNumber[1] = 0;
  potionsName[2] = "happy-hour";   potionsNumber[2] = 0;
  potionsName[3] = "immunity";     potionsNumber[3] = 0;
  potionsName[4] = "taxman";       potionsNumber[4] = 0;
  potionsName[5] = "lottery-win";  potionsNumber[5] = 0;  
  
  lcd.clear();
  String retour = serialRead(); 
  
  if (retour == "START") {
    tour = true;
    returnMainMenu();
    //Call the main menu.
    mainMenu();
  }
  else {
    waiting();
  }
  
}

int read_LCD_buttons(){
    int adc_key_in = analogRead(0);
    
    if (adc_key_in > 1000) return btnNONE; 
 
    if (adc_key_in < 50)   return btnRIGHT;  
    if (adc_key_in < 250)  return btnUP; 
    if (adc_key_in < 450)  return btnDOWN; 
    if (adc_key_in < 650)  return btnLEFT; 
    if (adc_key_in < 850)  return btnSELECT;  
 
    return btnNONE;
}
 
void mainMenu() {
  while(tour) {
    
    String retour = serialRead(); 
  
    if (retour == "WAIT") {
      lcd.clear();
      tour = false;
      break;
    }
    
    String entete = retour.substring(0, retour.indexOf(';'));
    
    if (entete == "POTIONS") {
      updateInventory(retour.substring(retour.indexOf(';') + 1));
    }
    
    //Refresh the button pressed.
    int x = analogRead (0);
    //Set the Row 0, Col 0 position.
    lcd.setCursor(0,0);
    
    int lcd_key = -1;
    //do {
      lcd_key = read_LCD_buttons();   // read the buttons
      //Check analog values from LCD Keypad Shield
      switch (lcd_key){               // depending on which button was pushed, we perform an action
           case btnDOWN:{
                 lcd.clear();
                 lcd.setCursor(0,0);  
                 lcd.print("   Se Deplacer");
                 lcd.setCursor(0,1); 
                 lcd.print("-> Inventaire");
                 lcd.setCursor(0,1);
                 choix = 2;
                 break;
           }
           case btnUP:{
                 lcd.clear();
                 lcd.setCursor(0,0);  
                 lcd.print("-> Se Deplacer");
                 lcd.setCursor(0,1); 
                 lcd.print("   Inventaire");
                 lcd.setCursor(0,1);
                 choix = 1;
                 break;
           }
           case btnRIGHT:{
                 selectMenu(choix);
                 break;
           }   
           case btnSELECT:{
                 returnMainMenu();
                 break;
           }
       }
     //} while (lcd_key == btnNONE);
     //Small delay
     delay(100);
  }
}

void returnMainMenu() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("   Se Deplacer");
  lcd.setCursor(0,1); 
  lcd.print("   Inventaire");
}
 
//Show the selection on Screen.
void selectMenu(int x) {
   int lcd_key = 0;
   switch (x) {
      case 1:
        lcd.clear();
        lcd.print("-> Se Deplacer");
        lcd.setCursor(0,1);
        delay(500);
        do {
          lcd_key = read_LCD_buttons();       
          switch (lcd_key){
               case btnUP:{
                     Serial.println("DEPLACEMENT;1" + '\0');
                     lcd.clear();
                     lcd.print("HAUT");
                     delay(1000);
                     break;
               }
               case btnDOWN:{
                     Serial.println("DEPLACEMENT;2" + '\0');
                     lcd.clear();
                     lcd.print("BAS");
                     delay(1000);
                     break;
               }
               case btnLEFT:{
                     Serial.println("DEPLACEMENT;3" + '\0');
                     lcd.clear();
                     lcd.print("GAUCHE");
                     delay(1000);
                     break;
               } 
               case btnRIGHT:{
                     Serial.println("DEPLACEMENT;4" + '\0');
                     lcd.clear();
                     lcd.print("DROITE");
                     delay(1000);
                     break;
               }
          }
        } while (lcd_key == btnNONE);
        returnMainMenu();
        break;
      case 2:
        lcd.clear();
        delay(500);
        int i = 0;
        int j = 0;
        lcd.print(potionsName[i] + " : " + potionsNumber[i]);
        lcd.setCursor(0,1);
        lcd.print(potionsName[i+1] + " : " + potionsNumber[i+1]);
        lcd.setCursor(0, 0);
        lcd.blink();
        do {
          lcd_key = read_LCD_buttons();       
          switch (lcd_key){
               case btnDOWN:{
                     if (j == 0) {
                       j++;
                       lcd.clear();
                       lcd.setCursor(0,0);
                       lcd.print(potionsName[i] + " : " + potionsNumber[i]);
                       lcd.setCursor(0,1);
                       lcd.print(potionsName[i+1] + " : " + potionsNumber[i+1]);
                     }
                     else if (j == 1) {
                        if (i <= 2) {
                          j--;
                          i+=2;
                          lcd.clear();
                          lcd.setCursor(0,0);
                          lcd.print(potionsName[i] + " : " + potionsNumber[i]);
                          lcd.setCursor(0,1);
                          lcd.print(potionsName[i+1] + " : " + potionsNumber[i+1]); 
                        }
                     }
                     break;
               }
               case btnUP:{
                     if (j == 1) {
                       j--;
                       lcd.clear();
                       lcd.setCursor(0,0);
                       lcd.print(potionsName[i] + " : " + potionsNumber[i]);
                       lcd.setCursor(0,1);
                       lcd.print(potionsName[i+1] + " : " + potionsNumber[i+1]);                       
                     }
                     else if (j == 0) {
                        if (i >= 2) {
                          j++;
                          i-=2;
                          lcd.clear();
                          lcd.setCursor(0,0);
                          lcd.print(potionsName[i] + " : " + potionsNumber[i]);
                          lcd.setCursor(0,1);
                          lcd.print(potionsName[i+1] + " : " + potionsNumber[i+1]);
                        }
                     }
                     break;
               }
               case btnRIGHT:{
                 Serial.println("POTION;" + (String)i + '\0');
                 break;
               }
               default: {
                 lcd.setCursor(0,j);
                 lcd.blink();
                 break;
               }
          }
          delay(75);
        } while (lcd_key != btnSELECT && lcd_key != btnRIGHT );
        lcd.noBlink();
        returnMainMenu();
        break;
    }
}

void updateInventaire(String name, int number) {
  for(int i = 0; i < 6; i++) {
    if (name == potionsName[i])
    {
      potionsNumber[i] = number;  
    }
  }  
}

String serialRead() {
  String dest = "";
  if (Serial.available()) {
     delay(100);
     char lastChar = Serial.read();
     while (lastChar != '\0' && lastChar != '\n') {
        dest += lastChar;
        lastChar = Serial.read();
     }
  }
  return dest; 
}

void waiting() {
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Attente");
    delay(100);
    lcd.setCursor(0,0);
    lcd.print("Attente.");
    delay(100);
    lcd.setCursor(0,0);
    lcd.print("Attente..");
    delay(100);
    lcd.setCursor(0,0);
    lcd.print("Attente...");
    delay(100);
}

void updateInventory(String trame) {
    if (trame != "") {
      String potion = trame.substring(0, trame.indexOf(':'));
      int nombre = 0;
      if (trame.indexOf(';') != -1) {
        nombre =  trame.substring(trame.indexOf(':') + 1, trame.indexOf(';')).toInt();
      }
      else {
        nombre =  trame.substring(trame.indexOf(':') + 1).toInt();
      }
      if (potion == "fov-increase") {
          potionsNumber[0] = nombre;
      }
      else if (potion == "magnet") {
          potionsNumber[1] = nombre;
      }
      else if (potion == "happy-hour") {
          potionsNumber[2] = nombre;
      }
      else if (potion == "immunity") {
          potionsNumber[3] = nombre;
      }
      else if (potion == "taxman") {
          potionsNumber[4] = nombre;
      }
      else if (potion == "lottery-win") {
          potionsNumber[5] = nombre;
      }
      if (trame.indexOf(';') != -1) {
        updateInventory(trame.substring(trame.indexOf(';') + 1));
      }
    }
}  
