const int LX = A3, LY = A4, RX = A0, RY = A1, LPRESS = 3, RPRESS = 2;
const int A = 7, B =  6, X = 5, Y = 4;
const int UP = 9, DOWN = 10, RIGHT = 8, LEFT = 11;
const int LT = 1, LB = 0, RT = A2, RB = A5;
const int START = 13, BACK = 12;
const int NUM_BUTTONS = 16;
const int BUTTONS[NUM_BUTTONS] = { A, B, X, Y, UP, DOWN, LEFT, RIGHT, LT, LB, RT, RB, LPRESS, RPRESS, START, BACK };

void setup() {
 pinMode(LX, INPUT);
 pinMode(LY, INPUT);
 pinMode(RX, INPUT);
 pinMode(RY, INPUT);

 for (int i=0;i<NUM_BUTTONS;i++) {
   pinMode(BUTTONS[i], INPUT_PULLUP);
 }

 Serial.begin(115200);
}

void loop() {
 int lx = analogRead(LX) - 512;
 int ly = analogRead(LY) - 512;

 int rx = analogRead(RX) - 512;
 int ry = analogRead(RY) - 512;
 
 int button_vals = 0;
 for (int i=0;i<NUM_BUTTONS;i++) {
   int button_val = !digitalRead(BUTTONS[i]);
   button_vals += (button_val << i);
 }

 delay(25);
}
