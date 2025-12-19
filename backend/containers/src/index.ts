/**
 * GIVC Core Academy + LINC Agents - Cloudflare Containers Worker
 * Container-enabled Worker that routes requests to the Python FastAPI container
 * and integrates with Cloudflare Workflows.
 */

import { Workflow } from '@cloudflare/workers-types';

export interface Env {
  LINC_CONTAINER: DurableObjectNamespace;
  ENVIRONMENT?: string;
  DB?: D1Database;
  
  // Workflow bindings
  CLAIMS_WORKFLOW?: Workflow;
  AUDIT_WORKFLOW?: Workflow;
  LEARNING_WORKFLOW?: Workflow;
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
    
    // Intercept Workflow requests
    if (url.pathname.startsWith('/api/workflows/')) {
      return this.handleWorkflowRequest(request, url);
    }
    
    // Forward everything else to Container at localhost:8080
    const containerUrl = `http://localhost:8080${url.pathname}${url.search}`;
    
    try {
      const containerRequest = new Request(containerUrl, {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });

      const response = await fetch(containerRequest);
      
      const newResponse = new Response(response.body, response);
      Object.entries(CORS_HEADERS).forEach(([key, value]) => {
        newResponse.headers.set(key, value);
      });
      
      return newResponse;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      // Fallback: if container is down, check if we can handle via workflow
      return new Response(
        JSON.stringify({ 
          error: "Container error", 
          message: errorMessage,
          hint: "Try /api/workflows/* endpoints for durable execution" 
        }),
        { status: 503, headers: { "Content-Type": "application/json", ...CORS_HEADERS } }
      );
    }
  }
  
  async handleWorkflowRequest(request: Request, url: URL): Promise<Response> {
    const path = url.pathname;
    let workflowInstance;
    
    try {
      const payload = await request.json();
      
      if (path.includes('/claims') && this.env.CLAIMS_WORKFLOW) {
        workflowInstance = await this.env.CLAIMS_WORKFLOW.create({ params: payload });
      } else if (path.includes('/audit') && this.env.AUDIT_WORKFLOW) {
        workflowInstance = await this.env.AUDIT_WORKFLOW.create({ params: payload });
      } else if (path.includes('/learning') && this.env.LEARNING_WORKFLOW) {
        workflowInstance = await this.env.LEARNING_WORKFLOW.create({ params: payload });
      } else {
         return new Response(JSON.stringify({ error: "Workflow not found or disabled" }), {
           status: 404, headers: { "Content-Type": "application/json", ...CORS_HEADERS }
         });
      }
      
      return new Response(JSON.stringify({
        status: "started",
        workflowId: workflowInstance.id,
        timestamp: new Date().toISOString()
      }), {
        status: 202,
        headers: { "Content-Type": "application/json", ...CORS_HEADERS }
      });
      
    } catch (e: any) {
      return new Response(JSON.stringify({ error: e.message }), {
        status: 500, headers: { "Content-Type": "application/json", ...CORS_HEADERS }
      });
    }
  }
}

// Main Worker
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
      if (path === "/health" || path === "/") {
        return jsonResponse({
          status: "healthy",
          service: "givc-linc-agents-container",
          deployment: "container-workflow-hybrid",
          timestamp: new Date().toISOString(),
          endpoints: {
             container_api: "/* (forwarded to container)",
             workflows: {
               claims: "POST /api/workflows/claims",
               audit: "POST /api/workflows/audit",
               learning: "POST /api/workflows/learning"
             }
          },
        });
      }

      const containerId = env.LINC_CONTAINER.idFromName("linc-agents-primary");
      const container = env.LINC_CONTAINER.get(containerId);

      const containerRequest = new Request(request.url, {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });

      containerRequest.headers.set("X-Edge-Location", "cloudflare-container");
      containerRequest.headers.set("X-Forwarded-For", request.headers.get("CF-Connecting-IP") || "");

      const response = await container.fetch(containerRequest);

      const newResponse = new Response(response.body, response);
      Object.entries(CORS_HEADERS).forEach(([key, value]) => {
        newResponse.headers.set(key, value);
      });
      newResponse.headers.set("X-Served-By", "cloudflare-container-hybrid");

      return newResponse;

    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      console.error("Worker error:", error);
      
      return jsonResponse({
        error: "Service error",
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
