#include <WiFi.h>
#include <WebServer.h>
#include <WiFiClient.h>

#include "src/OV2640.h"
#include "src/OV2640Streamer.h"
#include "src/CRtspSession.h"

#include "src/wifi_config.h"

OV2640 cam;

WiFiServer rtspServer(8554);

void setup()
{
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  WiFi.config(ip, gatway, subnet);

  // attempt to connect to Wifi network:
  while (WiFi.status != WL_CONNECTED)
  {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    WiFi.begin(ssid, password);

    // wait 10 seconds for connection:
    delay(10000);
  }

  esp_err_t err = cam.init(esp32cam_aithinker_config);
  if (err != ESP_OK)
  {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  rtspServer.begin();
}

CStreamer *streamer;
CRtspSession *session;
WiFiClient client; // FIXME, support multiple clients

void loop()
{
  uint32_t msecPerFrame = 100;
  static uint32_t lastimage = millis();

  // If we have an active client connection, just service that until gone
  // (FIXME - support multiple simultaneous clients)
  if (session)
  {
    session->handleRequests(0); // we don't use a timeout here,
    // instead we send only if we have new enough frames

    uint32_t now = millis();
    if (now > lastimage + msecPerFrame || now < lastimage)
    { // handle clock rollover
      session->broadcastCurrentFrame(now);
      lastimage = now;

      // check if we are overrunning our max frame rate
      now = millis();
      if (now > lastimage + msecPerFrame)
        printf("warning exceeding max frame rate of %d ms\n", now - lastimage);
    }

    if (session->m_stopped)
    {
      delete session;
      delete streamer;
      session = NULL;
      streamer = NULL;
    }
  }
  else
  {
    client = rtspServer.accept();

    if (client)
    {
      //streamer = new SimStreamer(&client, true);             // our streamer for UDP/TCP based RTP transport
      streamer = new OV2640Streamer(&client, cam); // our streamer for UDP/TCP based RTP transport

      session = new CRtspSession(&client, streamer); // our threads RTSP session and state
    }
  }
}
