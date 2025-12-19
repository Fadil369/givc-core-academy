/**
 * GIVC Core Academy + BrainSAIT LINC Agents - Unified Cloudflare Worker
 * Combines medical coding academy API with healthcare LINC agents
 */

// Configuration - reads from environment variables
const getConfig = (env) => ({
  agents: {
    masterlinc: env.MASTERLINC_URL || 'https://masterlinc.elfadil.com',
    healthcarelinc: env.HEALTHCARELINC_URL || 'https://healthcarelinc.elfadil.com',
    claimlinc: env.CLAIMLINC_URL || 'https://claimlinc.elfadil.com',
    ttlinc: env.TTLINC_URL || 'https://ttlinc.elfadil.com',
    policylinc: env.POLICYLINC_URL || 'https://policylinc.elfadil.com',
    clinicallinc: env.CLINICALLINC_URL || 'https://clinicallinc.elfadil.com',
    radiolinc: env.RADIOLINC_URL || 'https://radiolinc.elfadil.com',
  },
  cache: {
    ttl: 3600, // 1 hour
    translations: 86400, // 24 hours for translations
  },
  rateLimit: {
    requests: 100,
    window: 60, // 60 seconds
  },
});

// CORS headers
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Request-ID',
  'Access-Control-Max-Age': '86400',
};

/**
 * Main request handler - ES Module format
 */
export default {
  async fetch(request, env, ctx) {
    return handleRequest(request, env, ctx);
  }
};

/**
 * Handle incoming request
 */
async function handleRequest(request, env, ctx) {
  const CONFIG = getConfig(env);
  
  // Handle CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: CORS_HEADERS });
  }

  try {
    const url = new URL(request.url);
    const path = url.pathname;

    // ===== GIVC CORE ACADEMY ENDPOINTS =====
    
    // Health check
    if (path === '/health' || path === '/api/health') {
      return jsonResponse({
        status: 'healthy',
        version: '1.0.0',
        service: 'givc-core-academy-unified',
        environment: env.ENVIRONMENT || 'development',
        timestamp: new Date().toISOString(),
        modules: {
          audit: 'active',
          learning: 'active',
          linc_agents: 'active'
        }
      });
    }

    // API Documentation / Root
    if (path === '/docs' || path === '/' || path === '/api') {
      return jsonResponse({
        name: 'GIVC Core Academy + LINC Agents Unified API',
        version: '1.0.0',
        environment: env.ENVIRONMENT || 'development',
        endpoints: {
          // Academy endpoints
          health: '/api/health',
          audit_simulate: 'POST /api/audit/simulate',
          learning_path: 'POST /api/learning/path',
          fraud_analyze: 'POST /api/fraud/analyze',
          
          // LINC Agent endpoints
          orchestrate: 'POST /api/v1/orchestrate',
          healthcare: '/api/v1/healthcare/*',
          claims: '/api/v1/claims/*',
          translate: '/api/v1/translate/*',
          policy: '/api/v1/policy/*',
          clinical: '/api/v1/clinical/*',
          radiology: '/api/v1/radiology/*'
        }
      });
    }

    // ===== ACADEMY SERVICES =====
    
    // Audit simulation
    if (path === '/api/audit/simulate' && request.method === 'POST') {
      const data = await getRequestBody(request);
      const result = simulateAudit(
        data.provider_id || 'PROVIDER-001',
        data.sample_size || 50,
        data.sbs_version || '2.0'
      );
      
      // Store to D1 if available
      if (env.DB) {
        try {
          await env.DB.prepare(
            "INSERT INTO audit_logs (audit_id, provider_id, score, created_at) VALUES (?, ?, ?, datetime('now'))"
          ).bind(result.audit_id, result.provider_id, result.compliance_score).run();
        } catch (e) {
          result.db_status = `Storage skipped: ${e.message}`;
        }
      }
      
      return jsonResponse(result);
    }

    // Learning path generation
    if (path === '/api/learning/path' && request.method === 'POST') {
      const data = await getRequestBody(request);
      const result = generateLearningPath(data);
      return jsonResponse(result);
    }

    // Fraud analysis
    if (path === '/api/fraud/analyze' && request.method === 'POST') {
      const data = await getRequestBody(request);
      const result = analyzeFraud(data.audit_results || []);
      return jsonResponse(result);
    }

    // ===== LINC AGENT ROUTING =====
    
    // Route to appropriate LINC agent
    const agent = determineAgent(path);
    if (agent) {
      // Check rate limit with KV if available
      if (env.LINC_CACHE) {
        const rateLimitOk = await checkRateLimit(request, env);
        if (!rateLimitOk) {
          return jsonResponse({ error: 'Rate limit exceeded' }, 429);
        }
      }

      // Check cache for GET requests
      if (request.method === 'GET' && env.LINC_CACHE) {
        const cached = await getFromCache(request, env);
        if (cached) return cached;
      }

      // Forward to backend agent
      const response = await forwardToAgent(request, agent, CONFIG, env);

      // Cache successful GET responses
      if (request.method === 'GET' && response.status === 200 && env.LINC_CACHE) {
        ctx.waitUntil(cacheResponse(request, response.clone(), env));
      }

      return response;
    }

    // 404 for unknown routes
    return jsonResponse({ 
      error: 'Not Found', 
      path,
      available_routes: [
        '/api/health',
        '/api/audit/simulate',
        '/api/learning/path',
        '/api/fraud/analyze',
        '/api/v1/orchestrate',
        '/api/v1/healthcare/*',
        '/api/v1/claims/*'
      ]
    }, 404);

  } catch (error) {
    console.error('Worker error:', error);
    return jsonResponse({
      error: 'Internal server error',
      message: error.message,
      environment: env.ENVIRONMENT || 'unknown'
    }, 500);
  }
}

// ===== ACADEMY SERVICE FUNCTIONS =====

function simulateAudit(providerId, sampleSize, sbsVersion) {
  const auditId = `CHI-AUDIT-${new Date().toISOString().split('T')[0].replace(/-/g, '')}-${providerId.substring(0, 8)}`;
  
  // Random compliance score with realistic distribution
  const baseScore = 85 + (Math.random() - 0.5) * 20;
  const complianceScore = Math.max(0, Math.min(100, baseScore));
  
  // Determine risk level
  let riskLevel = 'low';
  if (complianceScore < 90) riskLevel = 'medium';
  if (complianceScore < 75) riskLevel = 'high';
  if (complianceScore < 60) riskLevel = 'critical';
  
  const totalErrors = Math.floor((100 - complianceScore) / 5);
  
  // Determine outcome
  let auditOutcome = 'COMPLIANT';
  if (complianceScore < 90) auditOutcome = 'MINOR_ISSUES';
  if (complianceScore < 75) auditOutcome = 'REQUIRES_IMPROVEMENT';
  if (complianceScore < 60) auditOutcome = 'NON_COMPLIANT';
  
  return {
    audit_id: auditId,
    audit_date: new Date().toISOString(),
    provider_id: providerId,
    sbs_version: sbsVersion,
    compliance_score: Math.round(complianceScore * 100) / 100,
    risk_level: riskLevel,
    audit_outcome: auditOutcome,
    sample_size: sampleSize,
    total_errors: totalErrors,
    corrective_actions: generateCorrectiveActions(riskLevel, complianceScore),
    summary: {
      ar: `تدقيق CHI مكتمل. درجة الامتثال: ${Math.round(complianceScore)}%`,
      en: `CHI Audit complete. Compliance score: ${Math.round(complianceScore)}%`
    }
  };
}

function generateCorrectiveActions(riskLevel, score) {
  const actions = [];
  if (riskLevel === 'high' || riskLevel === 'critical') {
    actions.push({
      action_id: 'CAP-001',
      type: 'mandatory_training',
      title_ar: 'تدريب إلزامي على معايير الترميز',
      title_en: 'Mandatory Coding Standards Training',
      deadline_days: 30
    });
  }
  if (score < 85) {
    actions.push({
      action_id: 'CAP-002',
      type: 'follow_up_audit',
      title_ar: 'مراجعة تدقيقية متابعة',
      title_en: 'Follow-up Compliance Audit',
      deadline_days: score < 70 ? 90 : 180
    });
  }
  return actions;
}

function generateLearningPath(learnerProfile) {
  const targetCert = learnerProfile.target_certification || 'CCP-KSA';
  const experience = learnerProfile.years_of_experience || 0;
  
  const modules = [
    { id: 'M001', title_ar: 'أساسيات ICD-10-AM', title_en: 'ICD-10-AM Fundamentals', hours: 8 },
    { id: 'M002', title_ar: 'نظام الفوترة السعودي (SBS)', title_en: 'Saudi Billing System (SBS)', hours: 12 },
    { id: 'M003', title_ar: 'معايير التوثيق السريري', title_en: 'Clinical Documentation Standards', hours: 6 },
  ];
  
  if (experience < 2) {
    modules.push(
      { id: 'M004', title_ar: 'أساسيات الترميز الطبي', title_en: 'Medical Coding Basics', hours: 10 },
      { id: 'M005', title_ar: 'المصطلحات الطبية', title_en: 'Medical Terminology', hours: 8 }
    );
  } else {
    modules.push(
      { id: 'M006', title_ar: 'ترميز الإجراءات المتقدمة', title_en: 'Advanced Procedure Coding', hours: 8 },
      { id: 'M007', title_ar: 'إجراءات التدقيق', title_en: 'Audit Procedures', hours: 6 }
    );
  }
  
  if (targetCert.includes('CCP')) {
    modules.push({ id: 'M008', title_ar: 'الإعداد لشهادة CCP', title_en: 'CCP Certification Prep', hours: 15 });
  }
  
  const totalHours = modules.reduce((sum, m) => sum + m.hours, 0);
  const successProbability = Math.min(0.95, 0.6 + (experience * 0.05));
  
  return {
    learning_path: {
      total_modules: modules.length,
      total_estimated_hours: totalHours,
      modules,
      recommended_pace: totalHours > 40 ? '4 hours/week' : '2 hours/week'
    },
    skill_gaps: [
      { skill: 'ICD-10 Coding', current_level: 60 + experience * 5, target_level: 90 },
      { skill: 'SBS Knowledge', current_level: 50 + experience * 7, target_level: 85 },
      { skill: 'Documentation', current_level: 70, target_level: 95 }
    ],
    success_probability: { overall_probability: Math.round(successProbability * 100) / 100 },
    estimated_completion_weeks: Math.ceil(totalHours / 4)
  };
}

function analyzeFraud(auditResults) {
  const fraudIndicators = [];
  let fraudRiskScore = 0;
  
  const errorCounts = {};
  for (const result of auditResults) {
    for (const error of (result.errors || [])) {
      const code = error.code || 'UNKNOWN';
      errorCounts[code] = (errorCounts[code] || 0) + 1;
    }
  }
  
  for (const [code, count] of Object.entries(errorCounts)) {
    if (count > auditResults.length * 0.3) {
      fraudIndicators.push({
        indicator: `Systematic ${code} errors`,
        severity: 'high',
        count
      });
      fraudRiskScore += 20;
    }
  }
  
  fraudRiskScore = Math.min(100, fraudRiskScore);
  
  return {
    fraud_risk_score: fraudRiskScore,
    fraud_indicators: fraudIndicators,
    requires_investigation: fraudRiskScore > 50,
    analyzed_claims: auditResults.length
  };
}

// ===== LINC AGENT FUNCTIONS =====

function determineAgent(path) {
  if (path.startsWith('/api/v1/orchestrate')) return 'masterlinc';
  if (path.startsWith('/api/v1/healthcare')) return 'healthcarelinc';
  if (path.startsWith('/api/v1/claims') || path.startsWith('/api/v1/analyze')) return 'claimlinc';
  if (path.startsWith('/api/v1/translate')) return 'ttlinc';
  if (path.startsWith('/api/v1/policy') || path.startsWith('/api/v1/interpret-policy')) return 'policylinc';
  if (path.startsWith('/api/v1/clinical')) return 'clinicallinc';
  if (path.startsWith('/api/v1/radiology') || path.startsWith('/api/v1/analyze-report')) return 'radiolinc';
  return null;
}

async function forwardToAgent(request, agentName, CONFIG, env) {
  const agentUrl = CONFIG.agents[agentName];
  const url = new URL(request.url);
  const targetUrl = `${agentUrl}${url.pathname}${url.search}`;

  const modifiedRequest = new Request(targetUrl, {
    method: request.method,
    headers: request.headers,
    body: request.body,
  });

  modifiedRequest.headers.set('X-Edge-Location', 'cloudflare');
  modifiedRequest.headers.set('X-Forwarded-For', request.headers.get('CF-Connecting-IP') || '');
  modifiedRequest.headers.set('X-Request-ID', crypto.randomUUID());
  modifiedRequest.headers.set('X-Environment', env.ENVIRONMENT || 'unknown');

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);
    
    const response = await fetch(modifiedRequest, { signal: controller.signal });
    clearTimeout(timeoutId);

    const modifiedResponse = new Response(response.body, response);
    Object.entries(CORS_HEADERS).forEach(([key, value]) => {
      modifiedResponse.headers.set(key, value);
    });
    modifiedResponse.headers.set('X-Agent', agentName);

    return modifiedResponse;
  } catch (error) {
    console.error(`Failed to forward to ${agentName}:`, error);
    return jsonResponse({
      error: 'Backend unavailable',
      agent: agentName,
      message: error.message
    }, 503);
  }
}

async function checkRateLimit(request, env) {
  if (!env.LINC_CACHE) return true;
  
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const key = `ratelimit:${ip}`;
  
  try {
    const current = await env.LINC_CACHE.get(key);
    const count = current ? parseInt(current) : 0;
    
    if (count >= 100) return false;
    
    await env.LINC_CACHE.put(key, (count + 1).toString(), { expirationTtl: 60 });
    return true;
  } catch (error) {
    console.error('Rate limit check failed:', error);
    return true;
  }
}

async function getFromCache(request, env) {
  const cache = caches.default;
  const response = await cache.match(request);
  
  if (response) {
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('X-Cache', 'HIT');
    return newResponse;
  }
  
  return null;
}

async function cacheResponse(request, response, env) {
  const cache = caches.default;
  const url = new URL(request.url);
  
  let ttl = 3600;
  if (url.pathname.includes('/translate')) {
    ttl = 86400;
  }
  
  const cachedResponse = new Response(response.body, response);
  cachedResponse.headers.set('Cache-Control', `public, max-age=${ttl}`);
  cachedResponse.headers.set('X-Cache', 'MISS');
  
  await cache.put(request, cachedResponse);
}

// ===== UTILITY FUNCTIONS =====

async function getRequestBody(request) {
  try {
    return await request.json();
  } catch {
    return {};
  }
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...CORS_HEADERS,
    },
  });
}
