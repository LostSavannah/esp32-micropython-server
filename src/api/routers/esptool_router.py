from fastapi import APIRouter
from typing import Callable
from threading import Thread
from .common import normalize_command_result
import subprocess
import os

def router(on_command_output:Callable[[list[str]],None] = None) -> APIRouter:

    def run_command(command:str, callback:Callable = None, post_step: Callable[[], None] = None):
        def inner():
            print(command)
            app, *args = command.split(" ")
            res = subprocess.run([app, *args], stdout=subprocess.PIPE)
            result = res.stdout.decode()
            print(result)
            if on_command_output is not None:
                on_command_output(normalize_command_result(result))
            if callback is not None:
                callback(result)
            if post_step is not None:
                post_step()
            return res.returncode
        result = Thread(target=inner)
        result.start()
        return result

    def esptool_args(**args):
        return {
            "port": os.environ["USB_PORT"],
            **args
        }

    def run_esptool_command(command:str, post_step: Callable[[], None] = None, **args,):
        std_args = esptool_args(**args)
        full_args = " ".join([f"--{a} {std_args[a]}" for a in std_args])
        tool = os.environ["ESP32_TOOL"]
        return run_command(f"{tool} {full_args} {command}", post_step=post_step)
    
    app = APIRouter()

    @app.post("/flash")
    def flash_chip():
        run_esptool_command("erase_flash")
        return {
            "message": "chip flash scheduled successfully"
        }

    @app.post("/upload_firmware")
    def upload_firmware():
        run_esptool_command("write_flash -z 0x1000 ./firmware/firmware.bin", chip="esp32", baud="460800")
        return {
            "message": "chip firmware upload scheduled successfully"
        }
    
    return app
