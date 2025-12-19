/**
 * GIVC Core Academy + LINC Agents - Cloudflare Containers Worker
 * Container-enabled Worker that routes requests to the Python FastAPI container
 * 
 * Note: Cloudflare Containers are in beta. This worker uses the Container class
 * from the cloudflare:container module.
 */

export interface Env {
  LINC_CONTAINER: DurableObjectNamespace;
  ENVIRONMENT?: string;
  DB?: D1Database;
}

// CORS headers
const CORS_HEADERS: Record<string, string> = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Request-ID",
  "Access-Control-Max-Age": "86400",
};

/**
 * Container Durable Object class
 * This class wraps the container and handles lifecycle events
 */
export class LincContainer {
  private state: DurableObjectState;
  private env: Env;

  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    // Container is accessed at localhost:8080 within the Durable Object
    const containerUrl = `http://localhost:8080${url.pathname}${url.search}`;
    
    try {
      const containerRequest = new Request(containerUrl, {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });

      // Forward to container
      const response = await fetch(containerRequest);
      
      // Add CORS headers
      const newResponse = new Response(response.body, response);
      Object.entries(CORS_HEADERS).forEach(([key, value]) => {
        newResponse.headers.set(key, value);
      });
      
      return newResponse;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      return new Response(
        JSON.stringify({ error: "Container error", message: errorMessage }),
        { status: 503, headers: { "Content-Type": "application/json", ...CORS_HEADERS } }
      );
    }
  }
}

// Main Worker
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
      // Edge-level health check
      if (path === "/health" || path === "/") {
        return jsonResponse({
          status: "healthy",
          service: "givc-linc-agents-container",
          edge: "cloudflare",
          environment: env.ENVIRONMENT || "production",
          timestamp: new Date().toISOString(),
          endpoints: {
            audit: "POST /api/audit/simulate",
            learning: "POST /api/learning/path",
            claims: "POST /api/v1/claims/analyze",
            translate: "POST /api/v1/translate",
            orchestrate: "POST /api/v1/orchestrate",
          },
        });
      }

      // Get container instance using a consistent ID
      const containerId = env.LINC_CONTAINER.idFromName("linc-agents-primary");
      const container = env.LINC_CONTAINER.get(containerId);

      // Forward the request to the container
      const containerRequest = new Request(request.url, {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });

      // Add edge headers
      containerRequest.headers.set("X-Edge-Location", "cloudflare-container");
      containerRequest.headers.set("X-Forwarded-For", request.headers.get("CF-Connecting-IP") || "");
      containerRequest.headers.set("X-Request-ID", crypto.randomUUID());

      // Forward to container Durable Object
      const response = await container.fetch(containerRequest);

      // Add CORS headers to response
      const newResponse = new Response(response.body, response);
      Object.entries(CORS_HEADERS).forEach(([key, value]) => {
        newResponse.headers.set(key, value);
      });
      newResponse.headers.set("X-Served-By", "cloudflare-container");

      return newResponse;

    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      console.error("Worker error:", error);
      
      return jsonResponse({
        error: "Container service error",
        message: errorMessage,
        timestamp: new Date().toISOString(),
      }, 503);
    }
  },
};

function jsonResponse(data: object, status: number = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...CORS_HEADERS,
    },
  });
}
