/**
 * GIVC Core Academy + LINC Agents - Cloudflare Agents SDK Implementation
 * 
 * AI-powered agents for healthcare operations using the Agents SDK:
 * - MasterLINC: Orchestration and routing
 * - ClaimLINC: Claims analysis and rejection resolution  
 * - HealthcareLINC: Healthcare operations
 * - PolicyLINC: Policy interpretation
 * - ClinicalLINC: Clinical terminology
 * - RadioLINC: Radiology analysis
 * - TTLINC: Translation services
 */

import { Agent, AgentNamespace, getAgentByName, routeAgentRequest } from 'agents';
import { Hono } from 'hono';
import { cors } from 'hono/cors';

// ============================================================================
// Environment Bindings
// ============================================================================
export interface Env {
  // Agent Namespaces (Durable Objects)
  MasterAgent: AgentNamespace<MasterLincAgent>;
  ClaimsAgent: AgentNamespace<ClaimsLincAgent>;
  AuditAgent: AgentNamespace<AuditLincAgent>;
  LearningAgent: AgentNamespace<LearningLincAgent>;
  
  // Workflow bindings
  CLAIMS_WORKFLOW?: Workflow;
  AUDIT_WORKFLOW?: Workflow;
  LEARNING_WORKFLOW?: Workflow;
  
  // Storage bindings
  DB?: D1Database;
  LINC_CACHE?: KVNamespace;
  
  // AI binding
  AI?: Ai;
  
  // Environment variables
  ENVIRONMENT?: string;
  OPENAI_API_KEY?: string;
}

// ============================================================================
// State Interfaces
// ============================================================================
interface AgentState {
  createdAt: string;
  lastActivity: string;
  requestCount: number;
}

interface ClaimsState extends AgentState {
  claimsAnalyzed: number;
  totalSavings: number;
  pendingClaims: string[];
}

interface AuditState extends AgentState {
  auditsCompleted: number;
  averageScore: number;
  correctiveActions: Array<{ id: string; status: string }>;
}

interface LearningState extends AgentState {
  pathsGenerated: number;
  activeModules: string[];
  completionRate: number;
}

// ============================================================================
// MASTER LINC AGENT - Orchestration Hub
// ============================================================================
export class MasterLincAgent extends Agent<Env, AgentState> {
  initialState: AgentState = {
    createdAt: new Date().toISOString(),
    lastActivity: new Date().toISOString(),
    requestCount: 0,
  };

  async onStart() {
    console.log(`MasterLINC Agent ${this.name} started`);
    this.sql`CREATE TABLE IF NOT EXISTS requests (
      id TEXT PRIMARY KEY,
      type TEXT,
      payload TEXT,
      response TEXT,
      created_at TEXT
    )`;
  }

  async onRequest(request: Request): Promise<Response> {
    const url = new URL(request.url);
    this.setState({
      ...this.state,
      lastActivity: new Date().toISOString(),
      requestCount: this.state.requestCount + 1,
    });

    // Health check
    if (url.pathname === '/health' || url.pathname === '/') {
      return this.jsonResponse({
        agent: 'MasterLINC',
        status: 'healthy',
        instanceId: this.name,
        state: this.state,
        capabilities: [
          'orchestrate',
          'route',
          'analyze',
          'schedule',
        ],
        timestamp: new Date().toISOString(),
      });
    }

    // Orchestration endpoint
    if (url.pathname === '/orchestrate' && request.method === 'POST') {
      return this.handleOrchestrate(request);
    }

    return this.jsonResponse({ error: 'Not found', path: url.pathname }, 404);
  }

  async handleOrchestrate(request: Request): Promise<Response> {
    try {
      const body = await request.json() as { action: string; payload: any };
      const { action, payload } = body;

      // Log request
      const requestId = crypto.randomUUID();
      this.sql`INSERT INTO requests (id, type, payload, created_at) 
               VALUES (${requestId}, ${action}, ${JSON.stringify(payload)}, ${new Date().toISOString()})`;

      let result: any;
      
      switch (action) {
        case 'analyze_claim':
          // Route to Claims Agent
          const claimsAgent = await getAgentByName<Env, ClaimsLincAgent>(
            this.env.ClaimsAgent,
            `claims-${payload.claimId || 'default'}`
          );
          result = await (await claimsAgent.fetch(new Request('http://internal/analyze', {
            method: 'POST',
            body: JSON.stringify(payload),
          }))).json();
          break;

        case 'run_audit':
          // Route to Audit Agent
          const auditAgent = await getAgentByName<Env, AuditLincAgent>(
            this.env.AuditAgent,
            `audit-${payload.providerId || 'default'}`
          );
          result = await (await auditAgent.fetch(new Request('http://internal/simulate', {
            method: 'POST',
            body: JSON.stringify(payload),
          }))).json();
          break;

        case 'generate_learning_path':
          // Route to Learning Agent
          const learningAgent = await getAgentByName<Env, LearningLincAgent>(
            this.env.LearningAgent,
            `learning-${payload.learnerId || 'default'}`
          );
          result = await (await learningAgent.fetch(new Request('http://internal/path', {
            method: 'POST',
            body: JSON.stringify(payload),
          }))).json();
          break;

        default:
          return this.jsonResponse({ error: 'Unknown action', action }, 400);
      }

      // Update request with response
      this.sql`UPDATE requests SET response = ${JSON.stringify(result)} WHERE id = ${requestId}`;

      return this.jsonResponse({
        requestId,
        action,
        result,
        processedAt: new Date().toISOString(),
      });

    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      return this.jsonResponse({ error: 'Orchestration failed', message }, 500);
    }
  }

  private jsonResponse(data: object, status = 200): Response {
    return new Response(JSON.stringify(data), {
      status,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

// ============================================================================
// CLAIMS LINC AGENT - Claims Analysis & Resolution
// ============================================================================
export class ClaimsLincAgent extends Agent<Env, ClaimsState> {
  initialState: ClaimsState = {
    createdAt: new Date().toISOString(),
    lastActivity: new Date().toISOString(),
    requestCount: 0,
    claimsAnalyzed: 0,
    totalSavings: 0,
    pendingClaims: [],
  };

  async onStart() {
    console.log(`ClaimsLINC Agent ${this.name} started`);
    this.sql`CREATE TABLE IF NOT EXISTS claims_analysis (
      id TEXT PRIMARY KEY,
      claim_id TEXT,
      payer_id TEXT,
      rejection_reason TEXT,
      root_causes TEXT,
      recommendations TEXT,
      confidence_score REAL,
      created_at TEXT
    )`;
  }

  async onRequest(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    this.setState({
      ...this.state,
      lastActivity: new Date().toISOString(),
      requestCount: this.state.requestCount + 1,
    });

    if (url.pathname === '/health') {
      return this.jsonResponse({
        agent: 'ClaimsLINC',
        status: 'healthy',
        instanceId: this.name,
        claimsAnalyzed: this.state.claimsAnalyzed,
        totalSavings: this.state.totalSavings,
      });
    }

    if ((url.pathname === '/analyze' || url.pathname === '/api/v1/claims/analyze') && request.method === 'POST') {
      return this.analyzeClaim(request);
    }

    return this.jsonResponse({ error: 'Not found' }, 404);
  }

  async analyzeClaim(request: Request): Promise<Response> {
    const payload = await request.json() as {
      claimId: string;
      payerId?: string;
      diagnosisCodes?: string[];
      procedureCodes?: string[];
      rejectionReason?: string;
    };

    const { claimId, payerId, diagnosisCodes = [], procedureCodes = [], rejectionReason } = payload;
    const analysisId = crypto.randomUUID();

    // Perform AI analysis
    const analysis = await this.performAnalysis(rejectionReason || '', diagnosisCodes, procedureCodes);

    // Store analysis
    this.sql`INSERT INTO claims_analysis (id, claim_id, payer_id, rejection_reason, root_causes, recommendations, confidence_score, created_at)
             VALUES (${analysisId}, ${claimId}, ${payerId || ''}, ${rejectionReason || ''}, 
                     ${JSON.stringify(analysis.rootCauses)}, ${JSON.stringify(analysis.recommendations)}, 
                     ${analysis.confidenceScore}, ${new Date().toISOString()})`;

    // Update state
    this.setState({
      ...this.state,
      claimsAnalyzed: this.state.claimsAnalyzed + 1,
      totalSavings: this.state.totalSavings + (analysis.estimatedSavings || 0),
    });

    // Trigger workflow if available
    if (this.env.CLAIMS_WORKFLOW) {
      try {
        const instance = await this.env.CLAIMS_WORKFLOW.create({
          params: payload,
        });
        analysis.workflowInstanceId = instance.id;
      } catch (e) {
        console.log('Workflow trigger skipped:', e);
      }
    }

    return this.jsonResponse({
      analysisId,
      claimId,
      ...analysis,
      processedAt: new Date().toISOString(),
    });
  }

  private async performAnalysis(rejectionReason: string, diagnosisCodes: string[], procedureCodes: string[]) {
    const rootCauses: string[] = [];
    const recommendations: Array<{ ar: string; en: string }> = [];
    let confidenceScore = 0.5;
    let estimatedSavings = 0;

    // Analyze based on rejection reason patterns
    const lowerReason = rejectionReason.toLowerCase();

    if (lowerReason.includes('code') || lowerReason.includes('invalid')) {
      rootCauses.push('Incorrect or missing diagnosis/procedure codes');
      recommendations.push({
        ar: 'تحديث رموز ICD-10 أو CPT المطلوبة',
        en: 'Update required ICD-10 or CPT codes'
      });
      confidenceScore = 0.85;
      estimatedSavings = 2500;
    }

    if (lowerReason.includes('authorization') || lowerReason.includes('prior auth')) {
      rootCauses.push('Missing prior authorization');
      recommendations.push({
        ar: 'الحصول على تفويض مسبق من الدافع',
        en: 'Obtain prior authorization from payer'
      });
      confidenceScore = 0.9;
      estimatedSavings = 5000;
    }

    if (lowerReason.includes('documentation') || lowerReason.includes('medical necessity')) {
      rootCauses.push('Insufficient clinical documentation');
      recommendations.push({
        ar: 'تحسين التوثيق السريري بالتفاصيل المطلوبة',
        en: 'Enhance clinical documentation with required details'
      });
      confidenceScore = 0.8;
      estimatedSavings = 3500;
    }

    if (lowerReason.includes('timely') || lowerReason.includes('deadline')) {
      rootCauses.push('Claim submitted after filing deadline');
      recommendations.push({
        ar: 'مراجعة مواعيد التقديم وتقديم استئناف',
        en: 'Review submission deadlines and file appeal'
      });
      confidenceScore = 0.7;
      estimatedSavings = 1500;
    }

    // Default if no patterns matched
    if (rootCauses.length === 0) {
      rootCauses.push('Requires manual review');
      recommendations.push({
        ar: 'مراجعة يدوية مطلوبة من المختص',
        en: 'Manual review required by specialist'
      });
    }

    return {
      rootCauses,
      recommendations,
      confidenceScore,
      estimatedSavings,
      automationAvailable: rootCauses.length > 0 && !rootCauses.includes('Requires manual review'),
      suggestedActions: recommendations.length > 0 ? ['Prepare corrected claim', 'Submit for re-processing'] : ['Route to manual review'],
    };
  }

  private jsonResponse(data: object, status = 200): Response {
    return new Response(JSON.stringify(data), {
      status,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

// ============================================================================
// AUDIT LINC AGENT - CHI Audit Simulation
// ============================================================================
export class AuditLincAgent extends Agent<Env, AuditState> {
  initialState: AuditState = {
    createdAt: new Date().toISOString(),
    lastActivity: new Date().toISOString(),
    requestCount: 0,
    auditsCompleted: 0,
    averageScore: 0,
    correctiveActions: [],
  };

  async onStart() {
    console.log(`AuditLINC Agent ${this.name} started`);
    this.sql`CREATE TABLE IF NOT EXISTS audit_results (
      id TEXT PRIMARY KEY,
      provider_id TEXT,
      sbs_version TEXT,
      compliance_score REAL,
      risk_level TEXT,
      audit_outcome TEXT,
      corrective_actions TEXT,
      created_at TEXT
    )`;
  }

  async onRequest(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    this.setState({
      ...this.state,
      lastActivity: new Date().toISOString(),
      requestCount: this.state.requestCount + 1,
    });

    if (url.pathname === '/health') {
      return this.jsonResponse({
        agent: 'AuditLINC',
        status: 'healthy',
        instanceId: this.name,
        auditsCompleted: this.state.auditsCompleted,
        averageScore: this.state.averageScore,
      });
    }

    if ((url.pathname === '/simulate' || url.pathname === '/api/audit/simulate') && request.method === 'POST') {
      return this.simulateAudit(request);
    }

    return this.jsonResponse({ error: 'Not found' }, 404);
  }

  async simulateAudit(request: Request): Promise<Response> {
    const payload = await request.json() as {
      providerId: string;
      sampleSize?: number;
      sbsVersion?: string;
      auditType?: string;
    };

    const { providerId, sampleSize = 50, sbsVersion = '2.0', auditType = 'routine' } = payload;
    const auditId = `CHI-AUDIT-${new Date().toISOString().split('T')[0].replace(/-/g, '')}-${providerId.substring(0, 8).toUpperCase()}`;

    // Simulate audit analysis
    const errorRate = Math.random() * 0.3; // 0-30% error rate
    const complianceScore = Math.round((1 - errorRate) * 100 * 100) / 100;
    const errorCount = Math.round(sampleSize * errorRate);

    let riskLevel: 'low' | 'medium' | 'high' | 'critical' = 'low';
    let auditOutcome = 'COMPLIANT';
    
    if (complianceScore < 90) { riskLevel = 'medium'; auditOutcome = 'MINOR_ISSUES'; }
    if (complianceScore < 75) { riskLevel = 'high'; auditOutcome = 'REQUIRES_IMPROVEMENT'; }
    if (complianceScore < 60) { riskLevel = 'critical'; auditOutcome = 'NON_COMPLIANT'; }

    // Generate corrective actions
    const correctiveActions: Array<{
      actionId: string;
      type: string;
      titleAr: string;
      titleEn: string;
      deadlineDays: number;
      priority: string;
    }> = [];

    if (riskLevel === 'high' || riskLevel === 'critical') {
      correctiveActions.push({
        actionId: 'CAP-001',
        type: 'mandatory_training',
        titleAr: 'تدريب إلزامي على معايير الترميز',
        titleEn: 'Mandatory Coding Standards Training',
        deadlineDays: 30,
        priority: 'high',
      });
    }

    if (complianceScore < 85) {
      correctiveActions.push({
        actionId: 'CAP-002',
        type: 'follow_up_audit',
        titleAr: 'مراجعة تدقيقية متابعة',
        titleEn: 'Follow-up Compliance Audit',
        deadlineDays: complianceScore < 70 ? 90 : 180,
        priority: 'medium',
      });
    }

    if (complianceScore < 75) {
      correctiveActions.push({
        actionId: 'CAP-003',
        type: 'documentation_review',
        titleAr: 'مراجعة إجراءات التوثيق',
        titleEn: 'Documentation Procedures Review',
        deadlineDays: 45,
        priority: 'high',
      });
    }

    // Store results
    this.sql`INSERT INTO audit_results (id, provider_id, sbs_version, compliance_score, risk_level, audit_outcome, corrective_actions, created_at)
             VALUES (${auditId}, ${providerId}, ${sbsVersion}, ${complianceScore}, ${riskLevel}, ${auditOutcome}, 
                     ${JSON.stringify(correctiveActions)}, ${new Date().toISOString()})`;

    // Update state
    const newAuditsCompleted = this.state.auditsCompleted + 1;
    const newAverageScore = ((this.state.averageScore * this.state.auditsCompleted) + complianceScore) / newAuditsCompleted;
    
    this.setState({
      ...this.state,
      auditsCompleted: newAuditsCompleted,
      averageScore: newAverageScore,
      correctiveActions: [...this.state.correctiveActions, ...correctiveActions.map(a => ({ id: a.actionId, status: 'pending' }))],
    });

    // Trigger workflow if available
    let workflowInstanceId: string | undefined;
    if (this.env.AUDIT_WORKFLOW) {
      try {
        const instance = await this.env.AUDIT_WORKFLOW.create({
          params: payload,
        });
        workflowInstanceId = instance.id;
      } catch (e) {
        console.log('Workflow trigger skipped:', e);
      }
    }

    return this.jsonResponse({
      auditId,
      auditDate: new Date().toISOString(),
      providerId,
      sbsVersion,
      auditType,
      complianceScore,
      riskLevel,
      auditOutcome,
      sampleSize,
      totalErrors: errorCount,
      correctiveActions,
      workflowInstanceId,
      summary: {
        ar: `تدقيق CHI مكتمل. درجة الامتثال: ${Math.round(complianceScore)}%`,
        en: `CHI Audit complete. Compliance score: ${Math.round(complianceScore)}%`,
      },
    });
  }

  private jsonResponse(data: object, status = 200): Response {
    return new Response(JSON.stringify(data), {
      status,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

// ============================================================================
// LEARNING LINC AGENT - Learning Path Generation
// ============================================================================
export class LearningLincAgent extends Agent<Env, LearningState> {
  initialState: LearningState = {
    createdAt: new Date().toISOString(),
    lastActivity: new Date().toISOString(),
    requestCount: 0,
    pathsGenerated: 0,
    activeModules: [],
    completionRate: 0,
  };

  async onStart() {
    console.log(`LearningLINC Agent ${this.name} started`);
    this.sql`CREATE TABLE IF NOT EXISTS learning_paths (
      id TEXT PRIMARY KEY,
      learner_id TEXT,
      target_certification TEXT,
      modules TEXT,
      skill_gaps TEXT,
      success_probability REAL,
      created_at TEXT
    )`;
  }

  async onRequest(request: Request): Promise<Response> {
    const url = new URL(request.url);
    
    this.setState({
      ...this.state,
      lastActivity: new Date().toISOString(),
      requestCount: this.state.requestCount + 1,
    });

    if (url.pathname === '/health') {
      return this.jsonResponse({
        agent: 'LearningLINC',
        status: 'healthy',
        instanceId: this.name,
        pathsGenerated: this.state.pathsGenerated,
        completionRate: this.state.completionRate,
      });
    }

    if ((url.pathname === '/path' || url.pathname === '/api/learning/path') && request.method === 'POST') {
      return this.generateLearningPath(request);
    }

    return this.jsonResponse({ error: 'Not found' }, 404);
  }

  async generateLearningPath(request: Request): Promise<Response> {
    const payload = await request.json() as {
      learnerId: string;
      targetCertification: string;
      yearsOfExperience?: number;
      currentRole?: string;
    };

    const { learnerId, targetCertification, yearsOfExperience = 1, currentRole = 'Medical Coder' } = payload;
    const pathId = crypto.randomUUID();

    // Calculate skill levels based on experience
    const baseLevel = 50 + yearsOfExperience * 5;
    const skillAssessment = {
      icd10Coding: Math.min(100, baseLevel + 10),
      sbsKnowledge: Math.min(100, baseLevel),
      documentation: Math.min(100, baseLevel + 20),
      clinicalTerminology: Math.min(100, baseLevel + 15),
    };

    // Generate personalized modules
    const modules: Array<{
      id: string;
      titleAr: string;
      titleEn: string;
      hours: number;
      priority: 'required' | 'recommended' | 'optional';
      order: number;
    }> = [
      { id: 'M001', titleAr: 'أساسيات ICD-10-AM', titleEn: 'ICD-10-AM Fundamentals', hours: 8, priority: 'required', order: 1 },
      { id: 'M002', titleAr: 'نظام الفوترة السعودي (SBS)', titleEn: 'Saudi Billing System (SBS)', hours: 12, priority: 'required', order: 2 },
      { id: 'M003', titleAr: 'معايير التوثيق السريري', titleEn: 'Clinical Documentation Standards', hours: 6, priority: 'required', order: 3 },
    ];

    if (yearsOfExperience < 2) {
      modules.push(
        { id: 'M004', titleAr: 'أساسيات الترميز الطبي', titleEn: 'Medical Coding Basics', hours: 10, priority: 'required', order: 4 },
        { id: 'M005', titleAr: 'المصطلحات الطبية', titleEn: 'Medical Terminology', hours: 8, priority: 'required', order: 5 }
      );
    } else {
      modules.push(
        { id: 'M006', titleAr: 'ترميز الإجراءات المتقدمة', titleEn: 'Advanced Procedure Coding', hours: 8, priority: 'recommended', order: 4 },
        { id: 'M007', titleAr: 'إجراءات التدقيق', titleEn: 'Audit Procedures', hours: 6, priority: 'recommended', order: 5 }
      );
    }

    if (targetCertification.toUpperCase().includes('CCP')) {
      modules.push(
        { id: 'M008', titleAr: 'الإعداد لشهادة CCP', titleEn: 'CCP Certification Prep', hours: 15, priority: 'required', order: 6 }
      );
    }

    // Calculate totals
    const totalHours = modules.reduce((sum, m) => sum + m.hours, 0);
    const hoursPerWeek = 4;
    const estimatedWeeks = Math.ceil(totalHours / hoursPerWeek);

    // Success probability
    const baseProbability = 0.6 + (yearsOfExperience * 0.05);
    const successProbability = Math.min(0.95, baseProbability);

    // Skill gaps
    const skillGaps = [
      { skill: 'ICD-10 Coding', currentLevel: skillAssessment.icd10Coding, targetLevel: 90 },
      { skill: 'SBS Knowledge', currentLevel: skillAssessment.sbsKnowledge, targetLevel: 85 },
      { skill: 'Documentation', currentLevel: skillAssessment.documentation, targetLevel: 95 },
      { skill: 'Clinical Terminology', currentLevel: skillAssessment.clinicalTerminology, targetLevel: 85 },
    ].filter(g => g.currentLevel < g.targetLevel);

    // Store path
    this.sql`INSERT INTO learning_paths (id, learner_id, target_certification, modules, skill_gaps, success_probability, created_at)
             VALUES (${pathId}, ${learnerId}, ${targetCertification}, ${JSON.stringify(modules)}, 
                     ${JSON.stringify(skillGaps)}, ${successProbability}, ${new Date().toISOString()})`;

    // Update state
    this.setState({
      ...this.state,
      pathsGenerated: this.state.pathsGenerated + 1,
      activeModules: [...new Set([...this.state.activeModules, ...modules.map(m => m.id)])],
    });

    // Trigger workflow if available
    let workflowInstanceId: string | undefined;
    if (this.env.LEARNING_WORKFLOW) {
      try {
        const instance = await this.env.LEARNING_WORKFLOW.create({
          params: payload,
        });
        workflowInstanceId = instance.id;
      } catch (e) {
        console.log('Workflow trigger skipped:', e);
      }
    }

    return this.jsonResponse({
      pathId,
      learnerId,
      targetCertification,
      learningPath: {
        totalModules: modules.length,
        totalEstimatedHours: totalHours,
        recommendedPace: `${hoursPerWeek} hours/week`,
        estimatedCompletionWeeks: estimatedWeeks,
        modules: modules.sort((a, b) => a.order - b.order),
      },
      skillAssessment,
      skillGaps,
      successProbability: {
        overallProbability: Math.round(successProbability * 100) / 100,
        factors: [
          { factor: 'Experience', impact: yearsOfExperience > 2 ? 'positive' : 'neutral' },
          { factor: 'Current Role', impact: currentRole.toLowerCase().includes('coder') ? 'positive' : 'neutral' },
        ],
      },
      workflowInstanceId,
      generatedAt: new Date().toISOString(),
    });
  }

  private jsonResponse(data: object, status = 200): Response {
    return new Response(JSON.stringify(data), {
      status,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

// ============================================================================
// MAIN WORKER - HTTP Router
// ============================================================================
const app = new Hono<{ Bindings: Env }>();

// CORS middleware
app.use('*', cors({
  origin: '*',
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
  maxAge: 86400,
}));

// Health check
app.get('/', (c) => c.json({
  service: 'givc-linc-agents',
  version: '2.0.0',
  framework: 'cloudflare-agents-sdk',
  environment: c.env.ENVIRONMENT || 'production',
  timestamp: new Date().toISOString(),
  agents: {
    master: '/agents/master-agent/:id',
    claims: '/agents/claims-agent/:id',
    audit: '/agents/audit-agent/:id',
    learning: '/agents/learning-agent/:id',
  },
  endpoints: {
    orchestrate: 'POST /api/v1/orchestrate',
    claimsAnalyze: 'POST /api/v1/claims/analyze',
    auditSimulate: 'POST /api/audit/simulate',
    learningPath: 'POST /api/learning/path',
  },
}));

app.get('/health', (c) => c.json({ status: 'healthy', timestamp: new Date().toISOString() }));

// API Routes - Direct to Agents
app.post('/api/v1/orchestrate', async (c) => {
  const agent = await getAgentByName<Env, MasterLincAgent>(c.env.MasterAgent, 'master-orchestrator');
  const newReq = new Request('http://internal/orchestrate', {
    method: 'POST',
    body: JSON.stringify(await c.req.json()),
    headers: c.req.raw.headers,
  });
  return agent.fetch(newReq);
});

app.post('/api/v1/claims/analyze', async (c) => {
  const body = await c.req.json() as { claimId?: string };
  const agentId = body.claimId || 'default';
  const agent = await getAgentByName<Env, ClaimsLincAgent>(c.env.ClaimsAgent, `claims-${agentId}`);
  const newReq = new Request('http://internal/analyze', {
    method: 'POST',
    body: JSON.stringify(body),
    headers: c.req.raw.headers,
  });
  return agent.fetch(newReq);
});

app.post('/api/audit/simulate', async (c) => {
  const body = await c.req.json() as { providerId?: string };
  const agentId = body.providerId || 'default';
  const agent = await getAgentByName<Env, AuditLincAgent>(c.env.AuditAgent, `audit-${agentId}`);
  const newReq = new Request('http://internal/simulate', {
    method: 'POST',
    body: JSON.stringify(body),
    headers: c.req.raw.headers,
  });
  return agent.fetch(newReq);
});

app.post('/api/learning/path', async (c) => {
  const body = await c.req.json() as { learnerId?: string };
  const agentId = body.learnerId || 'default';
  const agent = await getAgentByName<Env, LearningLincAgent>(c.env.LearningAgent, `learning-${agentId}`);
  const newReq = new Request('http://internal/path', {
    method: 'POST',
    body: JSON.stringify(body),
    headers: c.req.raw.headers,
  });
  return agent.fetch(newReq);
});

// Route to agents directly via URL pattern
app.all('/agents/*', async (c) => {
  return (await routeAgentRequest(c.req.raw, c.env)) || c.json({ error: 'Agent not found' }, 404);
});

// Export
export default app;
