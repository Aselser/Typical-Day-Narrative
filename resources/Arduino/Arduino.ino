const int pinSalida = 2;      // Pin de salida para el pulso
const int duracionPulso = 500; // Duración del pulso en milisegundos

bool habilitarInterrupcion = false;

void setup() {
  pinMode(pinSalida, OUTPUT);         // Configura el pin de salida
  digitalWrite(pinSalida, LOW);
  Serial.begin(115200);  // Inicia la comunicación serie
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    
    if (receivedChar == 'P') {
      habilitarInterrupcion = true;
    }
  }

  if (habilitarInterrupcion) {
    generarPulso();
    habilitarInterrupcion = false;
  }
}

void generarPulso() {
  digitalWrite(pinSalida, HIGH);           
  delay(duracionPulso);  // Espera la duración del pulso
  digitalWrite(pinSalida, LOW);   
}

