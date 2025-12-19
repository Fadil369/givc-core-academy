/**
 * GIVC Core Academy + LINC Agents - Cloudflare Containers Worker
 * Routes requests to backend containers
 */

// CORS headers
const CORS_HEADERS: Record<string, string> = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Request-ID",
  "Access-Control-Max-Age": "86400",
};

export interface Env {
  CONTAINERS?: Fetcher;
  ENVIRONMENT?: string;
  MASTERLINC_URL?: string;
  HEALTHCARELINC_URL?: string;
  CLAIMLINC_URL?: string;
  TTLINC_URL?: string;
  POLICYLINC_URL?: string;
  CLINICALLINC_URL?: string;
  RADIOLINC_URL?: string;
  DB?: D1Database;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
      // Health check
      if (path === "/health" || path === "/") {
        return jsonResponse({
          status: "healthy",
          service: "givc-linc-agents-container-worker",
          environment: env.ENVIRONMENT || "production",
          timestamp: new Date().toISOString(),
          endpoints: {
            audit: "/api/audit/simulate",
            learning: "/api/learning/path",
            claims: "/api/v1/claims/analyze",
            translate: "/api/v1/translate",
          },
        });
      }

      // Route to container if available
      if (env.CONTAINERS) {
        const containerResponse = await env.CONTAINERS.fetch(request);
        
        const response = new Response(containerResponse.body, containerResponse);
        Object.entries(CORS_HEADERS).forEach(([key, value]) => {
          response.headers.set(key, value);
        });
        
        return response;
      }

      // Fallback: handle requests directly in worker
      return await handleRequest(request, env);

    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error("Worker error:", error);
      return jsonResponse(
        {
          error: "Internal server error",
          message: errorMessage,
        },
        500
      );
    }
  },
};

async function handleRequest(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const path = url.pathname;

  // Audit simulation
  if (path === "/api/audit/simulate" && request.method === "POST") {
    const data = await getRequestBody(request);
    const result = simulateAudit(
      data.provider_id || "PROVIDER-001",
      data.sample_size || 50,
      data.sbs_version || "2.0"
    );
    return jsonResponse(result);
  }

  // Learning path
  if (path === "/api/learning/path" && request.method === "POST") {
    const data = await getRequestBody(request);
    const result = generateLearningPath(data);
    return jsonResponse(result);
  }

  // Claims analysis
  if (path === "/api/v1/claims/analyze" && request.method === "POST") {
    const data = await getRequestBody(request);
    return jsonResponse({
      claim_id: data.claim_id || "CLAIM-001",
      confidence_score: 0.85,
      recommendations: [
        { ar: "تحديث رمز ICD-10", en: "Update ICD-10 code" },
      ],
      ai_model_used: "gpt-4-medical",
    });
  }

  // Translation
  if (path === "/api/v1/translate" && request.method === "POST") {
    const data = await getRequestBody(request);
    const translations: Record<string, string> = {
      hypertension: "ارتفاع ضغط الدم",
      diabetes: "السكري",
    };
    const text = data.text || "";
    return jsonResponse({
      original: text,
      translated: translations[text.toLowerCase()] || text,
      confidence: 0.95,
    });
  }

  // 404
  return jsonResponse({ error: "Not Found", path }, 404);
}

function simulateAudit(providerId: string, sampleSize: number, sbsVersion: string) {
  const auditId = `CHI-AUDIT-${new Date().toISOString().split("T")[0].replace(/-/g, "")}-${providerId.substring(0, 8)}`;
  const baseScore = 85 + (Math.random() - 0.5) * 20;
  const complianceScore = Math.max(0, Math.min(100, baseScore));

  let riskLevel = "low";
  let auditOutcome = "COMPLIANT";
  if (complianceScore < 90) { riskLevel = "medium"; auditOutcome = "MINOR_ISSUES"; }
  if (complianceScore < 75) { riskLevel = "high"; auditOutcome = "REQUIRES_IMPROVEMENT"; }
  if (complianceScore < 60) { riskLevel = "critical"; auditOutcome = "NON_COMPLIANT"; }

  return {
    audit_id: auditId,
    audit_date: new Date().toISOString(),
    provider_id: providerId,
    sbs_version: sbsVersion,
    compliance_score: Math.round(complianceScore * 100) / 100,
    risk_level: riskLevel,
    audit_outcome: auditOutcome,
    sample_size: sampleSize,
    summary: {
      ar: `تدقيق CHI مكتمل. درجة الامتثال: ${Math.round(complianceScore)}%`,
      en: `CHI Audit complete. Compliance score: ${Math.round(complianceScore)}%`,
    },
  };
}

function generateLearningPath(profile: Record<string, unknown>) {
  const experience = (profile.years_of_experience as number) || 0;
  const modules = [
    { id: "M001", title_en: "ICD-10-AM Fundamentals", hours: 8 },
    { id: "M002", title_en: "Saudi Billing System (SBS)", hours: 12 },
  ];

  if (experience < 2) {
    modules.push({ id: "M003", title_en: "Medical Coding Basics", hours: 10 });
  } else {
    modules.push({ id: "M004", title_en: "Advanced Procedure Coding", hours: 8 });
  }

  const totalHours = modules.reduce((sum, m) => sum + m.hours, 0);

  return {
    learning_path: {
      total_modules: modules.length,
      total_hours: totalHours,
      modules,
    },
    estimated_weeks: Math.ceil(totalHours / 4),
  };
}

async function getRequestBody(request: Request): Promise<Record<string, unknown>> {
  try {
    return await request.json();
  } catch {
    return {};
  }
}

function jsonResponse(data: object, status: number = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...CORS_HEADERS,
    },
  });
}
