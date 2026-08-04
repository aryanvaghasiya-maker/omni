import os
import subprocess
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import gradio as gr

# 1. Install Node 22 and OmniRoute locally during Space startup
print("--- Initializing Free OmniRoute Environment ---")
try:
    # Download Node 22 directly to a user-writable directory (/tmp)
    print("Downloading Node.js v22...")
    subprocess.run("curl -fsSL https://nodejs.org/dist/v22.23.2/node-v22.23.2-linux-x64.tar.xz | tar -xJf - -C /tmp", shell=True, check=True)
    
    # Add Node 22 to the current PATH
    os.environ["PATH"] = f"/tmp/node-v22.23.2-linux-x64/bin:{os.environ['PATH']}"
    
    # Install the official omniroute tool locally
    print("Installing OmniRoute...")
    subprocess.run("npm install omniroute", shell=True, check=True)
    print("✅ OmniRoute successfully installed via local NPM package.")
except Exception as e:
    print(f"⚠️ Installation step notice: {e}")

# 2. Boot up OmniRoute in the background on private local port 8000
print("Launching OmniRoute background engine...")
subprocess.Popen(["npx", "omniroute", "--port", "8000", "--no-open"])

# 3. Create a FastAPI web proxy to pipe the background dashboard to port 7860
app = FastAPI()
client = httpx.AsyncClient(base_url="http://127.0.0.1:8000")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy_traffic(request: Request, path: str):
    """Intercepts HF Space URL requests and forwards them to the OmniRoute Dashboard"""
    url = f"/{path}"
    if request.query_params:
        url += f"?{request.query_params}"
        
    headers = dict(request.headers)
    # Clean up hosting specific headers to avoid loop blocks
    headers.pop("host", None)
    
    # Read the request body payload
    body = await request.body()
    
    # Forward the exact web request directly to the local OmniRoute server
    req = client.build_request(
        method=request.method,
        url=url,
        headers=headers,
        content=body
    )
    res = await client.send(req, stream=True)
    
    return StreamingResponse(
        res.aiter_raw(),
        status_code=res.status_code,
        headers=dict(res.headers)
    )

# 4. Attach a dummy Gradio mount point so Hugging Face registers the Space SDK happily
with gr.Blocks() as demo:
    gr.Markdown("OmniRoute core initialized.")

# Mount gradio to a subpath to prevent it from overlapping the root dashboard UI
app = gr.mount_gradio_app(app, demo, path="/_hf_status")
