from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from typing import Callable
import uuid
import time

def router() -> tuple[APIRouter, Callable[[list[str]],None]]:

    app = APIRouter()
    outputs:list[str] = []

    def on_command_output(items:list[str]):
        outputs.extend(items)

    async def get_outputs(req:Request):
        index = 0 if len(outputs) <= 10 else len(outputs) - 10
        print("SSE connected...")
        try:
            while not await req.is_disconnected():
                while index < len(outputs):
                    yield event(outputs[index])
                    index += 1
                time.sleep(1)
        except:
            pass
        print("SSE disconnected...")

    def event(data:str, name:str = "Update"):
        return f"event: {name}\ndata: {data}\n\n"

    @app.get("/connect")
    def upload_firmware(request:Request):
        return StreamingResponse(get_outputs(request), media_type="text/event-stream")
    
    return app, on_command_output
