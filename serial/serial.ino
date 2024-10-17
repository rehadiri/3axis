
int val = 512;
  
void setup()
{
  Serial.begin(115200); /* Seri haberlesme baslatildi */
  while(!Serial){ /* Wait for Serial port */ }
}

void loop()
{
 Serial.println(val);
 delay (1000);
}
 