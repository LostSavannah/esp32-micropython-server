from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, Response
from fastapi import File
from typing import Annotated
import base64
import os
import uuid
import subprocess
import zipfile
from io import BytesIO

def run_command(command:str, callback = None):
    print(command)
    app, *args = command.split(" ")
    res = subprocess.run([app, *args], stdout=subprocess.PIPE)
    if callback is not None:
        callback(res.stdout.decode())
    return res.returncode

def ampy_args(**args):
    return {
        "port": os.environ["USB_PORT"],
        **args
    }

def run_ampy_command(command:str, callback = None, **args):
    std_args = ampy_args(**args)
    full_args = " ".join([f"--{a} {std_args[a]}" for a in std_args])
    tool = os.environ["AMPY_TOOL"]
    return run_command(f"{tool} {full_args} {command}", callback)

def ensure_directory(path:str):
    base = ""
    for part in path.split("/")[:-1]:
        base = "/".join([base, part])
        run_ampy_command(f"mkdir {base}")

def get_content(path:str):
    result = ""
    def set_result(value:str):
        nonlocal result
        result = value
    run_ampy_command(f"get {path}", callback=set_result)
    return result

def set_content(path:str, file:bytes):
    local_file = str(uuid.uuid4())
    with open(local_file, 'wb') as fi:
        fi.write(file)
    ensure_directory(path)
    run_ampy_command(f"put {local_file} {path}")
    os.remove(local_file)
    return path

def router() -> APIRouter:
    app = APIRouter()

    @app.get("/files/list:{path:path}")
    def list_directories(path:str):
        result = []
        def set_result(value:str):
            nonlocal result
            files = value.replace("\r\n", '\n').replace("\r", "\n").split("\n")
            result = [(i[2:] if i.startswith("/.") else i) for i in files if len(i) > 0]
        run_ampy_command(f"ls {path}", callback=set_result)
        return result

    @app.get("/files/download:{path:path}")
    def download_file(path:str):
        result = get_content(path)
        filename = path.split("/")[-1]
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        return Response(content=result, headers=headers)

    @app.get("/files/base64:{path:path}")
    def get_file_content_base64(path:str):
        result = base64.b64encode(get_content(path).encode()).decode()
        return Response(content=result)

    @app.get("/files/{path:path}")
    def get_file_content(path:str):
        return Response(content=get_content(path))

    @app.post("/files/zip:{path:path}")
    def upload_zip(path:str, file:Annotated[bytes, File()]):
        results = dict()
        with BytesIO(file) as bytes_io:
            zip_file = zipfile.ZipFile(bytes_io)
            files = [i for i in zip_file.infolist() if not i.is_dir()]
            for entry in files:
                try:
                    current_path = f"{path}/{entry.filename}"
                    current_bytes = zip_file.read(entry.filename)
                    set_content(current_path, current_bytes)
                    results[current_path] = True
                except:
                    results[current_path] = False
            return results

    @app.post("/files/write:{path:path}")
    async def write_file(path:str, request:Request):
        content = await request.body()
        return set_content(path, content)

    @app.post("/files/{path:path}")
    def upload_file(path:str, file:Annotated[bytes, File()]):
        return set_content(path, file)

    @app.delete("/files/{path:path}")
    def delete_directory(path:str):
        result = run_ampy_command(f"rm {path}")
        if result == 1:
            result = run_ampy_command(f"rmdir {path}")
        return path
        
    @app.delete("/files/{path:path}")
    def delete_directory(path:str):
        result = run_ampy_command(f"rm {path}")
        if result == 1:
            result = run_ampy_command(f"rmdir {path}")
        return path
    
    @app.post("/run")
    async def run_file(request:Request):
        path = str(uuid.uuid4())
        with open(path, 'wb') as fo:
            fo.write(await request.body())
        output = ""
        def callback(msg:str):
            nonlocal output
            output = msg
        result = run_ampy_command(f"run {path}", callback=callback)
        os.remove(path)
        return {
            "result": result,
            "output": output
        }
    
    @app.head("/reset")
    def resets_device():
        result = ""
        def callback(msg:str):
            nonlocal result
            result = msg
        result = run_ampy_command(f"reset", callback=callback)
        return result


    return app
