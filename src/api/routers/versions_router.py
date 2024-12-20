from fastapi import APIRouter, Request
from fastapi.responses import Response
from hashlib import md5
from binascii import hexlify
from ..core.version_manager import VersionManager
import zipfile
import os

def router() -> APIRouter:
    zip_path = os.environ["VERSIONS_ZIP"]
    app = APIRouter()

    def get_checksum(data:bytes) -> str:
        hash = md5(data)
        return hexlify(hash.digest()).decode()

    def init() -> dict[str,str]:
        manifest:dict[str, str] = dict()
        with zipfile.ZipFile(zip_path, mode='r') as file:
            for entry in file.infolist():
                checksum = get_checksum(file.read(entry.filename))
                manifest[entry.filename] = checksum
            return manifest

    manifest = init()
        
    @app.get('/versions')
    def get_versions():
        return [{
          "logic_path": i,
          "file_checksum": manifest[i]  
        } for i in manifest]

    @app.post('/files/{path:path}')
    async def set_file(path:str, request:Request):
        with zipfile.ZipFile(zip_path, mode='r') as file:
            content = await request.body()
            checksum = get_checksum(content)
            src = file.getinfo(path) if path in file.namelist() else path
            with file.open(src, 'w') as fo:
                fo.write(content)
            manifest[path] = checksum
            return checksum

    @app.get('/versions/{checksum}')
    def get_version(checksum:str):
        with zipfile.ZipFile(zip_path, mode='r') as file:
            candidates = [i for i in manifest if manifest[i] == checksum]
            if len(candidates) == 0:
                return None
            with file.open(candidates[0], 'r') as fi:
                return Response(fi.read())

    return app