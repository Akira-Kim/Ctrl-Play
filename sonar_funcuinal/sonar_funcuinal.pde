import processing.serial.*;
import java.util.ArrayList;

Serial myPort;

int iAngle = 0;
int iDistance = 0;

ArrayList<RedLine> redLines = new ArrayList<RedLine>();

int radarRadius;
int centerX, centerY;

void setup() {
  size(1000, 750);
  smooth();

  centerX = width/2;
  centerY = height - 80;
  radarRadius = width/2 - 120;

  println(Serial.list());
  myPort = new Serial(this, "COM4", 9600); // TROQUE AQUI
  myPort.bufferUntil('.');
}

void draw() {

  background(5, 15, 10);

  drawGrid();
  drawSweep();
  drawLiveBeam();
  updateRedLines();
  drawHUD();
}

void serialEvent(Serial myPort) {

  String data = myPort.readStringUntil('.');

  if (data != null) {

    data = trim(data);
    data = data.substring(0, data.length()-1);

    int index = data.indexOf(",");

    if (index > 0) {

      iAngle = int(data.substring(0, index));
      iDistance = int(data.substring(index+1));

      if (iDistance > 0 && iDistance < 200) {
        redLines.add(new RedLine(iAngle, iDistance));
      }
    }
  }
}

void drawGrid() {

  stroke(0, 255, 120, 80);
  noFill();

  for (int i = 1; i <= 5; i++) {
    arc(centerX, centerY,
        radarRadius*i/5*2,
        radarRadius*i/5*2,
        PI, TWO_PI);
  }

  for (int a = 0; a <= 180; a += 15) {

    float corrected = 180 - a;

    float x = centerX + radarRadius * cos(radians(corrected));
    float y = centerY - radarRadius * sin(radians(corrected));

    line(centerX, centerY, x, y);
  }
}

void drawSweep() {

  float corrected = 180 - iAngle;

  noStroke();
  fill(0, 255, 100, 40);

  beginShape();
  vertex(centerX, centerY);

  for (int a = int(corrected-10); a <= corrected; a++) {

    float x = centerX + radarRadius * cos(radians(a));
    float y = centerY - radarRadius * sin(radians(a));

    vertex(x, y);
  }

  endShape(CLOSE);
}

void drawLiveBeam() {

  float corrected = 180 - iAngle;

  float mappedDist = map(iDistance, 0, 200, 0, radarRadius);

  float xObj = centerX + mappedDist * cos(radians(corrected));
  float yObj = centerY - mappedDist * sin(radians(corrected));

  strokeWeight(3);

  // Parte verde até o objeto
  stroke(0, 255, 0);
  line(centerX, centerY, xObj, yObj);
}

void updateRedLines() {

  for (int i = redLines.size()-1; i >= 0; i--) {

    RedLine r = redLines.get(i);
    r.display();

    if (r.dead()) {
      redLines.remove(i);
    }
  }
}

void drawHUD() {

  fill(0, 255, 120);
  textSize(18);
  text("ANG: " + iAngle + "°", 30, 40);
  text("DIST: " + iDistance + " cm", 30, 70);
}

class RedLine {

  float angle;
  float distance;
  float birth;
  float duration = 5000; // 5 segundos

  RedLine(float a, float d) {
    angle = 180 - a;
    distance = map(d, 0, 200, 0, radarRadius);
    birth = millis();
  }

  void display() {

    float age = millis() - birth;
    float alpha = map(age, 0, duration, 255, 0);

    float xObj = centerX + distance * cos(radians(angle));
    float yObj = centerY - distance * sin(radians(angle));

    float xMax = centerX + radarRadius * cos(radians(angle));
    float yMax = centerY - radarRadius * sin(radians(angle));

    stroke(255, 0, 0, alpha);
    strokeWeight(3);

    // Linha vermelha do objeto até o fim
    line(xObj, yObj, xMax, yMax);
  }

  boolean dead() {
    return millis() - birth > duration;
  }
}
