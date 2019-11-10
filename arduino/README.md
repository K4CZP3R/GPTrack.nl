# Arduino GPTrack.nl

## How to setup ESP32 (drivers)?

* Download CH340 drivers. [Windows](http://www.wch.cn/download/CH341SER_EXE.html), [Linux](http://www.wch.cn/download/CH341SER_LINUX_ZIP.html)

## How to setup Arduino IDE?

* [Link to the guide]( https://github.com/espressif/arduino-esp32/blob/master/docs/arduino-ide/boards_manager.md )

## How to compile it?

1. Include every library in this repo `proftaak/arduino/include_me/*.zip` using Arduino IDE: `Sketch/Include Library/Add .ZIP library`
2. Setup ESP32 upload options:
   1. `Tools/Board` set to `WEMOS LOLIN32`
   2. `Tools/Upload Speed` set to `921600`
   3. `Tools/CPU frequency` set to `240MHz`
   4. `Tools/Flash frequency` set to `80Mhz`
   5. `Tools/Partition Scheme` set to `Default`

### Change WiFi settings (AP + Certificate)

* Go to `gpHttp.cpp` and change `const char* ssid` and `const char* password`
* You need to change the value of `const char* root_ca` to 
  * `root_ca_server` if you plan to be using `https://server.gptrack.nl`
  * `root_ca_debug` if you plan to be using git cloned server.

* You need to change `server_url` in `gpDevice.cpp` to 
  * `https://server.gptrack.nl/`, if you plan to be using our official server.
  * `https://<your ip>:<port>/`, if you plan to be using git cloned server.