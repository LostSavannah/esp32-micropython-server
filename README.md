# esp32-micropython-server
Simple esp32 micropython server

## Configuration

```bash
docker run -it -p 8955:8955 \
--device /dev/ttyUSB0 \
--restart unless-stopped \
--name esp32-micropython-server \
coderookieerick/esp32-micropython-server:linux-arm64
```
