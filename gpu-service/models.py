"""Pydantic request/response models."""

from pydantic import BaseModel, Field


class BertScoreRequest(BaseModel):
    candidates: list[str]
    references: list[str]
    lang: str = "en"
    model_type: str = "roberta-large"


class BertScoreResponse(BaseModel):
    precision: list[float]
    recall: list[float]
    f1: list[float]
    model: str


class EmbedRequest(BaseModel):
    texts: list[str]
    model: str = "all-MiniLM-L6-v2"


class EmbedResponse(BaseModel):
    embeddings: list[list[float]]
    model: str
    dimensions: int


class HealthResponse(BaseModel):
    status: str = "ok"
    device: str


class InfoResponse(BaseModel):
    device: str
    device_name: str
    vram_total_mb: int | None = None
    vram_used_mb: int | None = None
    pytorch_version: str
    cuda_version: str | None = None
    loaded_models: list[str] = Field(default_factory=list)
