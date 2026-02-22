// GPU Bridge — Shared TypeScript types

export interface GpuBridgeConfig {
  serviceUrl: string;
  timeout?: number;
  apiKey?: string;
  models?: {
    embed?: string;
    bertscore?: string;
  };
}

// --- Responses ---

export interface HealthResponse {
  status: "ok" | "error";
  device: string;
}

export interface InfoResponse {
  device: string;
  device_name: string;
  vram_total_mb?: number;
  vram_used_mb?: number;
  pytorch_version: string;
  cuda_version: string | null;
  loaded_models: string[];
}

export interface BertScoreRequest {
  candidates: string[];
  references: string[];
  lang?: string;
  model_type?: string;
}

export interface BertScoreResponse {
  precision: number[];
  recall: number[];
  f1: number[];
  model: string;
}

export interface EmbedRequest {
  texts: string[];
  model?: string;
}

export interface EmbedResponse {
  embeddings: number[][];
  model: string;
  dimensions: number;
}
