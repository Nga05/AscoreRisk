from api_views import ascore_fastapi  #ascore_fastapi_debug, 
import uvicorn

if __name__ == "__main__":
    uvicorn.run(ascore_fastapi.app, host="127.0.0.1", port=8000)
