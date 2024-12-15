FROM python:3

ARG FIRMWARE="https://micropython.org/resources/firmware/ESP32_GENERIC-20241129-v1.24.1.bin"

WORKDIR /app

#Downloading the firmware
RUN mkdir ./firmware
RUN curl -o ./firmware/firmware.bin ${FIRMWARE}

#Installing requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./server.py .
COPY ./routers ./routers

EXPOSE 8955

ENV USB_PORT="/dev/ttyUSB0"
ENV ESP32_TOOL="esptool.py"
ENV AMPY_TOOL="ampy"

CMD [ "python", "/app/server.py" ]
