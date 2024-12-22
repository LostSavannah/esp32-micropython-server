from fastapi import FastAPI, Request, Response
import uvicorn
from routers.esptool_router import router as esptool_router
from routers.ampy_router import router as ampy_router
from routers.versions_router import router as versions_router
from routers.webhook_router import router as webhook_router
from routers.sse_router import router as sse_router

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


sse_router_obj, callback = sse_router()

app.include_router(esptool_router(callback), prefix="/device/esptools", tags=["Esptool"])
app.include_router(ampy_router(callback), prefix="/device/ampy", tags=["Ampy"])
app.include_router(versions_router(), prefix="/core", tags=["Core versions"])
app.include_router(webhook_router(), prefix="/webhook", tags=["Webhook router"])
app.include_router(sse_router_obj, prefix="/sse", tags=["SSE router"])

if __name__=='__main__':
    uvicorn.run("server:app", port=8955, host='0.0.0.0', reload=True)
