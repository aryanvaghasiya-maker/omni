import os
import subprocess
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import gradio as gr
import spaces

@spaces.GPU
def dummy_gpu_function():
    pass

import threading

def setup_and_run_omniroute():
    print("--- Initializing Free OmniRoute Environment ---")
    try:
        print("Downloading Node.js v22...")
        subprocess.run("curl -fsSL https://nodejs.org/dist/v22.23.2/node-v22.23.2-linux-x64.tar.xz | tar -xJf - -C /tmp", shell=True, check=True)
        os.environ["PATH"] = f"/tmp/node-v22.23.2-linux-x64/bin:{os.environ['PATH']}"
        
        print("Installing OmniRoute...")
        subprocess.run("npm install omniroute", shell=True, check=True)
        print("✅ OmniRoute successfully installed via local NPM package.")
        
        print("Launching OmniRoute background engine...")
        env = os.environ.copy()
        env["PORT"] = "8080"
        subprocess.Popen(["./node_modules/.bin/omniroute", "--port", "8080", "--no-open"], env=env)
    except Exception as e:
        print(f"⚠️ Installation step notice: {e}")

# Start the setup in a background thread so app.py loads instantly
threading.Thread(target=setup_and_run_omniroute, daemon=True).start()

# 3. Create a FastAPI web proxy to pipe the background dashboard to port 7860
app = FastAPI()
client = httpx.AsyncClient(base_url="http://127.0.0.1:8080")

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

# Hugging Face looks for a 'demo' object to launch, but we launch our FastAPI app wrapper instead
if __name__ == "__main__":
    import uvicorn
    import time
    time.sleep(2) # Give OmniRoute time to bind to 8080
    # Expose the combined app on Hugging Face's mandatory web port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)