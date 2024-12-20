from fastapi import APIRouter, Request
from fastapi.responses import Response
from hashlib import md5
from binascii import hexlify
from core.version_manager import VersionManager
import zipfile
import os

def router() -> APIRouter:
    app = APIRouter()
    
    version_manager = VersionManager(
        os.environ.get("VERSIONS_ROOT"),
        os.environ.get("VERSIONS_DB")
    )   

    @app.get('/versions')
    def get_versions():
        versions = version_manager.get_version()
        return [{
          "logic_path": i,
          "file_checksum": versions[i]  
        } for i in versions]

    @app.post('/files/{path:path}')
    async def set_file(path:str, request:Request):
        return version_manager.set_file(path, await request.body())

    @app.get('/versions/{checksum}')
    def get_version(checksum:str):
        return Response(version_manager.get_by_hash(checksum))

    return app