// @elvatis/openclaw-gpu-bridge
// TODO: implement plugin

export default function (api: any) {
  const config = api.config as { serviceUrl: string; timeout?: number; apiKey?: string };

  api.registerTool({
    name: "gpu_health",
    description: "Check if the remote GPU service is available",
    parameters: { type: "object", properties: {}, required: [] },
    async execute() {
      const res = await fetch(`${config.serviceUrl}/health`);
      const data = await res.json();
      return { content: [{ type: "text", text: JSON.stringify(data) }] };
    },
  });

  // TODO: bertscore_compute, embed_text
}
