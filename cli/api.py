from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import subprocess
from typing import Literal
import json
import os
import logging
import consul

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(static_dir, "favicon.svg"))

@app.get("/sw.js")
async def service_worker():
    # Return empty response to prevent 404 errors
    return {}

def check_consul_connection():
    try:
        # Use consul:8500 instead of localhost:8500
        consul_result = subprocess.run(
            ['curl', '-s', '-f', 'http://consul:8500/v1/status/leader'],
            capture_output=True,
            text=True,
            timeout=2
        )
        return consul_result.returncode == 0 and consul_result.stdout.strip()
    except Exception:
        return False

@app.get("/api/status")
async def get_status():
    try:
        # Connect to Consul
        consul_client = consul.Consul(
            host=os.getenv('CONSUL_HTTP_ADDR', 'consul').split(':')[0],
            port=int(os.getenv('CONSUL_HTTP_ADDR', 'consul:8500').split(':')[1])
        )
        
        # Test Consul connection
        try:
            consul_client.kv.get('test')
            consul_status = True
        except Exception as e:
            logger.error(f"Consul error: {str(e)}")
            consul_status = False

        # Test S3 connection
        s3_status = os.getenv('S3_ENABLED', 'false').lower() == 'true'

        return {
            "success": True,
            "services": {
                "consul": consul_status,
                "s3": s3_status
            },
            "output": ""  # Add any additional output here
        }
    except Exception as e:
        logger.error(f"Status endpoint error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/start/{server_type}")
async def start_server(server_type: Literal['app', 'gpu']):
    try:
        result = subprocess.run(['***REMOVED***', 'start', server_type], 
                              capture_output=True, 
                              text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {
            "success": True,
            "output": result.stdout
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stop/{server_type}")
async def stop_server(server_type: Literal['app', 'gpu']):
    try:
        result = subprocess.run(['***REMOVED***', 'stop', server_type], 
                              capture_output=True, 
                              text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {
            "success": True,
            "output": result.stdout
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/settings")
async def get_settings():
    try:
        # Get all relevant environment variables with actual values
        env_vars = {
            'CONSUL_HTTP_ADDR': os.environ.get('CONSUL_HTTP_ADDR', ''),
            'HCLOUD_TOKEN': os.environ.get('HCLOUD_TOKEN', 'Not set'),
            'S3_ENABLED': os.environ.get('S3_ENABLED', 'false'),
            'S3_ACCESS_KEY': os.environ.get('S3_ACCESS_KEY', 'Not set'),
            'S3_SECRET_KEY': os.environ.get('S3_SECRET_KEY', 'Not set'),
            'S3_BUCKET': os.environ.get('S3_BUCKET', ''),
            'S3_ENDPOINT': os.environ.get('S3_ENDPOINT', ''),
            'S3_REGION': os.environ.get('S3_REGION', ''),
            'DEBUG': os.environ.get('DEBUG', 'false')
        }

        # Check Consul connection
        consul_connected = check_consul_connection()

        return {
            "success": True,
            "settings": {
                "env": env_vars,
                "services": {
                    "consul": {
                        "connected": consul_connected,
                        "url": "http://consul:8500"
                    }
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000) 