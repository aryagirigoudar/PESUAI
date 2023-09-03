from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve static files (e.g., images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Use Jinja2 templates for HTML rendering
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Endpoint to request microphone permission
@app.post("/request_microphone_permission")
async def request_microphone_permission():
    # Your permission handling logic here
    # You can use JavaScript to request the actual browser permission
    return {"message": "Microphone permission requested"}
