from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import logging
import time

from routers import emotion, adaptive, wellness

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mentraai")

app = FastAPI(title="MentraAI Backend", version="0.1.0")

# CORS - adjust origins for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = f"{time.time_ns()}"
    logger.info(f"start request id={idem} path={request.url.path}")
    start = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.exception(f"error id={idem} path={request.url.path} error={exc}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
    process_time = (time.time() - start) * 1000
    logger.info(f"completed id={idem} status_code={response.status_code} time_ms={process_time:.2f}")
    response.headers["X-Process-Time-Ms"] = str(process_time)
    return response

# Routers
app.include_router(emotion.router, prefix="/api/emotion", tags=["emotion"])
app.include_router(adaptive.router, prefix="/api/adaptive", tags=["adaptive"])
app.include_router(wellness.router, prefix="/api/wellness", tags=["wellness"])

# Root
@app.get("/")
async def root():
    return {"service": "MentraAI Backend", "status": "ok"}