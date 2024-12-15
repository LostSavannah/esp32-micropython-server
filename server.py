from fastapi import FastAPI
import uvicorn
from routers.esptool_router import router as esptool_router
from routers.ampy_router import router as ampy_router

app = FastAPI()

app.include_router(esptool_router(), prefix="/device/esptools", tags=["Esptool"])
app.include_router(ampy_router(), prefix="/device/ampy", tags=["Ampy"])

if __name__=='__main__':
    uvicorn.run("server:app", port=8955, host='0.0.0.0', reload=True)
