FROM python:3

ARG FIRMWARE="https://micropython.org/resources/firmware/ESP32_GENERIC-20241129-v1.24.1.bin"

WORKDIR /app

#Downloading the firmware
RUN mkdir ./firmware
RUN curl -o ./firmware/firmware.bin ${FIRMWARE}

#Installing requirements
COPY ./src/api/requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/api/core ./core
COPY ./src/api/server.py .
COPY ./src/api/routers ./routers


#TODO: Generate db instead
COPY ./src/api/data/database.db ./data/database.db
RUN mkdir ./versions

EXPOSE 8955

ENV USB_PORT="/dev/ttyUSB0"
ENV ESP32_TOOL="esptool.py"
ENV AMPY_TOOL="ampy"
ENV VERSIONS_ROOT="/app/versions"
ENV VERSIONS_DB="/app/data/database.db"

CMD [ "python", "/app/server.py" ]
