"""FastAPI GPU service — BERTScore + Embeddings."""

import asyncio
import logging
import os
import time
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from device import get_device, get_device_info
from models import (
    BertScoreRequest, BertScoreResponse,
    EmbedRequest, EmbedResponse,
    HealthResponse, InfoResponse,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("gpu-service")


def _vram_mb() -> str:
    """Return current VRAM usage string, e.g. '412 MB / 11264 MB'."""
    if not torch.cuda.is_available():
        return "CPU"
    used = round(torch.cuda.memory_allocated(0) / 1024 / 1024)
    total = round(torch.cuda.get_device_properties(0).total_memory / 1024 / 1024)
    return f"{used} MB / {total} MB VRAM"

# --- Concurrency guard ---
MAX_CONCURRENT = int(os.environ.get("GPU_MAX_CONCURRENT", "2"))
semaphore = asyncio.Semaphore(MAX_CONCURRENT)

# --- Auth ---
API_KEY = os.environ.get("API_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load models at startup."""
    device = get_device()
    app.state.device = device
    app.state.loaded_models = []

    # Load BERTScore (lazy — bert_score caches internally, but we warm it)
    model_bertscore = os.environ.get("MODEL_BERTSCORE", "roberta-large")
    logger.info(f"Loading BERTScore model: {model_bertscore} ...")
    t0 = time.time()
    from bert_score import BERTScorer
    app.state.bert_scorer = BERTScorer(
        model_type=model_bertscore, device=str(device), lang="en"
    )
    app.state.bertscore_model_name = model_bertscore
    app.state.loaded_models.append(f"bertscore:{model_bertscore}")
    logger.info(f"BERTScore ready ({time.time()-t0:.1f}s) — {_vram_mb()}")

    # Load embedding model
    model_embed = os.environ.get("MODEL_EMBED", "all-MiniLM-L6-v2")
    logger.info(f"Loading embedding model: {model_embed} ...")
    t0 = time.time()
    from sentence_transformers import SentenceTransformer
    app.state.embedder = SentenceTransformer(model_embed, device=str(device))
    app.state.embed_model_name = model_embed
    app.state.loaded_models.append(f"embed:{model_embed}")
    logger.info(f"Embedder ready ({time.time()-t0:.1f}s) — {_vram_mb()}")

    logger.info("=" * 55)
    logger.info(f"  OpenClaw GPU Bridge ready!")
    logger.info(f"  Device : {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")
    logger.info(f"  Models : {', '.join(app.state.loaded_models)}")
    logger.info(f"  VRAM   : {_vram_mb()}")
    logger.info(f"  URL    : http://0.0.0.0:8765")
    logger.info("=" * 55)
    yield


app = FastAPI(title="OpenClaw GPU Bridge Service", version="0.1.0", lifespan=lifespan)


# --- Middleware: API key auth ---
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if API_KEY and request.url.path != "/health":
        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)


# --- Endpoints ---

@app.get("/health", response_model=HealthResponse)
async def health(request: Request):
    return HealthResponse(status="ok", device=str(request.app.state.device))


@app.get("/info", response_model=InfoResponse)
async def info(request: Request):
    di = get_device_info(request.app.state.device)
    di["loaded_models"] = request.app.state.loaded_models
    return InfoResponse(**di)


@app.post("/bertscore", response_model=BertScoreResponse)
async def bertscore(req: BertScoreRequest, request: Request):
    if len(req.candidates) != len(req.references):
        raise HTTPException(400, "candidates and references must have equal length")

    try:
        await asyncio.wait_for(semaphore.acquire(), timeout=1.0)
    except asyncio.TimeoutError:
        raise HTTPException(503, "GPU busy — retry later", headers={"Retry-After": "5"})

    try:
        scorer: "BERTScorer" = request.app.state.bert_scorer  # noqa: F821
        n = len(req.candidates)
        logger.info(f"[bertscore] {n} pair(s) — {_vram_mb()}")
        t0 = time.time()
        P, R, F1 = await asyncio.to_thread(scorer.score, req.candidates, req.references)
        elapsed = time.time() - t0
        avg_f1 = sum(F1.tolist()) / len(F1)
        logger.info(f"[bertscore] done in {elapsed:.2f}s — avg F1={avg_f1:.4f} — {_vram_mb()}")
        return BertScoreResponse(
            precision=P.tolist(),
            recall=R.tolist(),
            f1=F1.tolist(),
            model=request.app.state.bertscore_model_name,
        )
    finally:
        semaphore.release()


@app.post("/embed", response_model=EmbedResponse)
async def embed(req: EmbedRequest, request: Request):
    try:
        await asyncio.wait_for(semaphore.acquire(), timeout=1.0)
    except asyncio.TimeoutError:
        raise HTTPException(503, "GPU busy — retry later", headers={"Retry-After": "5"})

    try:
        embedder = request.app.state.embedder
        n = len(req.texts)
        logger.info(f"[embed] {n} text(s) — {_vram_mb()}")
        t0 = time.time()
        vecs = await asyncio.to_thread(embedder.encode, req.texts, convert_to_numpy=True)
        elapsed = time.time() - t0
        logger.info(f"[embed] done in {elapsed:.2f}s — {vecs.shape[1]}d vectors — {_vram_mb()}")
        return EmbedResponse(
            embeddings=vecs.tolist(),
            model=request.app.state.embed_model_name,
            dimensions=vecs.shape[1],
        )
    finally:
        semaphore.release()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
