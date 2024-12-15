from fastapi import FastAPI, Request, Response
import uvicorn
from routers.esptool_router import router as esptool_router
from routers.ampy_router import router as ampy_router

def configure_cors(api:FastAPI) -> FastAPI:
    async def inner(request:Request, call_next):
        response:Response = Response() if request.method == "OPTIONS" else await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = '*'
        response.headers["Access-Control-Allow-Methods"] = 'GET, POST, OPTIONS, PUT, DELETE, PATCH'
        response.headers["Access-Control-Allow-Headers"] = '*'
        return response
    api.middleware("http")(inner)
    return api

app = configure_cors(FastAPI())

app.include_router(esptool_router(), prefix="/device/esptools", tags=["Esptool"])
app.include_router(ampy_router(), prefix="/device/ampy", tags=["Ampy"])

if __name__=='__main__':
    uvicorn.run("server:app", port=8955, host='0.0.0.0', reload=True)
