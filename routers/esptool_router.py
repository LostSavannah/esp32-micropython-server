from fastapi import APIRouter
import os

def run_command(command:str):
    print(command)
    os.system(command)

def esptool_args(**args):
    return {
        "port": os.environ["USB_PORT"],
        **args
    }

def run_esptool_command(command:str, **args):
    std_args = esptool_args(**args)
    full_args = " ".join([f"--{a} {std_args[a]}" for a in std_args])
    tool = os.environ["ESP32_TOOL"]
    run_command(f"{tool} {full_args} {command}")

def router() -> APIRouter:
    app = APIRouter()

    @app.post("/flash")
    def flash_chip():
        run_esptool_command("erase_flash")
        return "Ok"

    @app.post("/upload_firmware")
    def upload_firmware():
        run_esptool_command("write_flash -z 0x1000 ./firmware/firmware.bin", chip="esp32", baud="460800")
        return "Ok"
    
    return app
