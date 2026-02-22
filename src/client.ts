// GPU Bridge — HTTP Client

import type {
  GpuBridgeConfig,
  HealthResponse,
  InfoResponse,
  BertScoreRequest,
  BertScoreResponse,
  EmbedRequest,
  EmbedResponse,
} from "./types.js";

export class GpuBridgeClient {
  private baseUrl: string;
  private timeout: number;
  private apiKey?: string;

  constructor(config: GpuBridgeConfig) {
    this.baseUrl = config.serviceUrl.replace(/\/+$/, "");
    this.timeout = (config.timeout ?? 45) * 1000;
    this.apiKey = config.apiKey;
  }

  private async request<T>(path: string, options?: RequestInit): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(this.apiKey ? { "X-API-Key": this.apiKey } : {}),
    };

    const timeoutMs = path === "/health" ? 5000 : this.timeout;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}${path}`, {
        ...options,
        headers: { ...headers, ...(options?.headers as Record<string, string>) },
        signal: controller.signal,
      });

      if (!res.ok) {
        const body = await res.text().catch(() => "");
        throw new Error(`GPU service ${path} returned ${res.status}: ${body}`);
      }

      return (await res.json()) as T;
    } finally {
      clearTimeout(timer);
    }
  }

  async health(): Promise<HealthResponse> {
    return this.request<HealthResponse>("/health");
  }

  async info(): Promise<InfoResponse> {
    return this.request<InfoResponse>("/info");
  }

  async bertscore(req: BertScoreRequest): Promise<BertScoreResponse> {
    return this.request<BertScoreResponse>("/bertscore", {
      method: "POST",
      body: JSON.stringify(req),
    });
  }

  async embed(req: EmbedRequest): Promise<EmbedResponse> {
    return this.request<EmbedResponse>("/embed", {
      method: "POST",
      body: JSON.stringify(req),
    });
  }
}
