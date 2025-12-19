/**
 * GIVC Core Academy + LINC Agents - Cloudflare Workflows
 * 
 * Durable multi-step workflows for healthcare operations:
 * - Claims processing with AI analysis
 * - Audit simulations with corrective actions
 * - Learning path generation
 * - Medical translations
 */

import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from 'cloudflare:workers';

// Environment bindings
interface Env {
  CLAIMS_WORKFLOW: Workflow;
  AUDIT_WORKFLOW: Workflow;
  LEARNING_WORKFLOW: Workflow;
  DB?: D1Database;
  AI?: Ai;
  LINC_CACHE?: KVNamespace;
}

// ============================================================================
// WORKFLOW PARAMETERS
// ============================================================================

interface ClaimsParams {
  claimId: string;
  payerId: string;
  diagnosisCodes: string[];
  procedureCodes: string[];
  rejectionReason?: string;
  priority?: 'normal' | 'high' | 'urgent';
}

interface AuditParams {
  providerId: string;
  sampleSize: number;
  sbsVersion: string;
  auditType?: 'routine' | 'targeted' | 'comprehensive';
}

interface LearningParams {
  learnerId: string;
  targetCertification: string;
  yearsOfExperience: number;
  currentRole: string;
}

// ============================================================================
// CLAIMS PROCESSING WORKFLOW
// ============================================================================

export class ClaimsWorkflow extends WorkflowEntrypoint<Env, ClaimsParams> {
  async run(event: WorkflowEvent<ClaimsParams>, step: WorkflowStep) {
    const { claimId, payerId, diagnosisCodes, procedureCodes, rejectionReason } = event.payload;

    // Step 1: Validate claim data
    const validation = await step.do('validate-claim-data', async () => {
      const issues: string[] = [];
      
      if (!claimId) issues.push('Missing claim ID');
      if (!payerId) issues.push('Missing payer ID');
      if (!diagnosisCodes?.length) issues.push('Missing diagnosis codes');
      
      return {
        isValid: issues.length === 0,
        issues,
        claimId,
      };
    });

    if (!validation.isValid) {
      return { status: 'failed', reason: 'validation', issues: validation.issues };
    }

    // Step 2: Analyze rejection reason with AI
    const analysis = await step.do('ai-analyze-rejection', {
      retries: { limit: 3, delay: '5 seconds', backoff: 'exponential' },
      timeout: '2 minutes',
    }, async () => {
      const recommendations: Array<{ar: string, en: string}> = [];
      const rootCauses: string[] = [];

      if (rejectionReason) {
        if (rejectionReason.toLowerCase().includes('code')) {
          rootCauses.push('Incorrect or missing diagnosis/procedure codes');
          recommendations.push({
            ar: 'تحديث رموز ICD-10 أو CPT',
            en: 'Update ICD-10 or CPT codes'
          });
        }
        if (rejectionReason.toLowerCase().includes('authorization')) {
          rootCauses.push('Missing prior authorization');
          recommendations.push({
            ar: 'الحصول على تفويض مسبق من الدافع',
            en: 'Obtain prior authorization from payer'
          });
        }
        if (rejectionReason.toLowerCase().includes('documentation')) {
          rootCauses.push('Insufficient clinical documentation');
          recommendations.push({
            ar: 'تحسين التوثيق السريري',
            en: 'Improve clinical documentation'
          });
        }
      }

      // Default if no specific reasons found
      if (rootCauses.length === 0) {
        rootCauses.push('Requires manual review');
        recommendations.push({
          ar: 'مراجعة يدوية مطلوبة',
          en: 'Manual review required'
        });
      }

      return {
        confidenceScore: recommendations.length > 0 ? 0.85 : 0.5,
        rootCauses,
        recommendations,
        automationAvailable: recommendations.length > 0,
      };
    });

    // Step 3: Store analysis results
    await step.do('store-analysis-results', async () => {
      // In production, store to D1 database
      console.log(`Storing analysis for claim ${claimId}`);
      return { stored: true, timestamp: new Date().toISOString() };
    });

    // Step 4: Determine next actions
    const nextActions = await step.do('determine-next-actions', async () => {
      const actions: string[] = [];
      
      if (analysis.automationAvailable) {
        actions.push('Prepare corrected claim');
        actions.push('Submit for re-processing');
      } else {
        actions.push('Route to manual review queue');
        actions.push('Notify billing team');
      }
      
      return { actions, requiresHumanReview: !analysis.automationAvailable };
    });

    return {
      status: 'completed',
      claimId,
      analysis: {
        confidenceScore: analysis.confidenceScore,
        rootCauses: analysis.rootCauses,
        recommendations: analysis.recommendations,
      },
      nextActions: nextActions.actions,
      requiresHumanReview: nextActions.requiresHumanReview,
      processedAt: new Date().toISOString(),
    };
  }
}

// ============================================================================
// AUDIT SIMULATION WORKFLOW
// ============================================================================

export class AuditWorkflow extends WorkflowEntrypoint<Env, AuditParams> {
  async run(event: WorkflowEvent<AuditParams>, step: WorkflowStep) {
    const { providerId, sampleSize, sbsVersion, auditType = 'routine' } = event.payload;

    // Step 1: Initialize audit
    const auditInit = await step.do('initialize-audit', async () => {
      const auditId = `CHI-AUDIT-${new Date().toISOString().split('T')[0].replace(/-/g, '')}-${providerId.substring(0, 8)}`;
      return {
        auditId,
        startTime: new Date().toISOString(),
        providerId,
        sbsVersion,
        auditType,
      };
    });

    // Step 2: Gather sample claims
    const sampleData = await step.do('gather-sample-claims', {
      retries: { limit: 2, delay: '10 seconds', backoff: 'constant' },
    }, async () => {
      // Simulate gathering claims data
      const claims = [];
      for (let i = 0; i < sampleSize; i++) {
        claims.push({
          claimId: `CLM-${Date.now()}-${i}`,
          hasErrors: Math.random() > 0.85,
          errorType: Math.random() > 0.5 ? 'coding' : 'documentation',
        });
      }
      return { claims, totalSampled: sampleSize };
    });

    // Step 3: Analyze compliance
    const complianceAnalysis = await step.do('analyze-compliance', async () => {
      const errorCount = sampleData.claims.filter(c => c.hasErrors).length;
      const baseScore = ((sampleSize - errorCount) / sampleSize) * 100;
      const complianceScore = Math.max(0, Math.min(100, baseScore));

      let riskLevel: 'low' | 'medium' | 'high' | 'critical' = 'low';
      let auditOutcome = 'COMPLIANT';
      
      if (complianceScore < 90) { riskLevel = 'medium'; auditOutcome = 'MINOR_ISSUES'; }
      if (complianceScore < 75) { riskLevel = 'high'; auditOutcome = 'REQUIRES_IMPROVEMENT'; }
      if (complianceScore < 60) { riskLevel = 'critical'; auditOutcome = 'NON_COMPLIANT'; }

      return {
        complianceScore: Math.round(complianceScore * 100) / 100,
        riskLevel,
        auditOutcome,
        errorCount,
        sampleSize,
      };
    });

    // Step 4: Generate corrective actions
    const correctiveActions = await step.do('generate-corrective-actions', async () => {
      const actions: Array<{
        actionId: string;
        type: string;
        titleAr: string;
        titleEn: string;
        deadlineDays: number;
      }> = [];

      if (complianceAnalysis.riskLevel === 'high' || complianceAnalysis.riskLevel === 'critical') {
        actions.push({
          actionId: 'CAP-001',
          type: 'mandatory_training',
          titleAr: 'تدريب إلزامي على معايير الترميز',
          titleEn: 'Mandatory Coding Standards Training',
          deadlineDays: 30,
        });
      }

      if (complianceAnalysis.complianceScore < 85) {
        actions.push({
          actionId: 'CAP-002',
          type: 'follow_up_audit',
          titleAr: 'مراجعة تدقيقية متابعة',
          titleEn: 'Follow-up Compliance Audit',
          deadlineDays: complianceAnalysis.complianceScore < 70 ? 90 : 180,
        });
      }

      return { actions };
    });

    // Step 5: Store audit results
    await step.do('store-audit-results', async () => {
      console.log(`Storing audit ${auditInit.auditId} results`);
      return { stored: true };
    });

    return {
      auditId: auditInit.auditId,
      auditDate: auditInit.startTime,
      providerId,
      sbsVersion,
      auditType,
      complianceScore: complianceAnalysis.complianceScore,
      riskLevel: complianceAnalysis.riskLevel,
      auditOutcome: complianceAnalysis.auditOutcome,
      sampleSize: complianceAnalysis.sampleSize,
      totalErrors: complianceAnalysis.errorCount,
      correctiveActions: correctiveActions.actions,
      summary: {
        ar: `تدقيق CHI مكتمل. درجة الامتثال: ${Math.round(complianceAnalysis.complianceScore)}%`,
        en: `CHI Audit complete. Compliance score: ${Math.round(complianceAnalysis.complianceScore)}%`,
      },
    };
  }
}

// ============================================================================
// LEARNING PATH WORKFLOW
// ============================================================================

export class LearningWorkflow extends WorkflowEntrypoint<Env, LearningParams> {
  async run(event: WorkflowEvent<LearningParams>, step: WorkflowStep) {
    const { learnerId, targetCertification, yearsOfExperience, currentRole } = event.payload;

    // Step 1: Assess current skills
    const skillAssessment = await step.do('assess-current-skills', async () => {
      const baseLevel = 50 + yearsOfExperience * 5;
      return {
        icd10Coding: Math.min(100, baseLevel + 10),
        sbsKnowledge: Math.min(100, baseLevel),
        documentation: Math.min(100, baseLevel + 20),
        clinicalTerminology: Math.min(100, baseLevel + 15),
      };
    });

    // Step 2: Generate learning modules
    const modules = await step.do('generate-learning-modules', async () => {
      const moduleList: Array<{
        id: string;
        titleAr: string;
        titleEn: string;
        hours: number;
        priority: 'required' | 'recommended' | 'optional';
      }> = [
        { id: 'M001', titleAr: 'أساسيات ICD-10-AM', titleEn: 'ICD-10-AM Fundamentals', hours: 8, priority: 'required' },
        { id: 'M002', titleAr: 'نظام الفوترة السعودي (SBS)', titleEn: 'Saudi Billing System (SBS)', hours: 12, priority: 'required' },
        { id: 'M003', titleAr: 'معايير التوثيق السريري', titleEn: 'Clinical Documentation Standards', hours: 6, priority: 'required' },
      ];

      if (yearsOfExperience < 2) {
        moduleList.push(
          { id: 'M004', titleAr: 'أساسيات الترميز الطبي', titleEn: 'Medical Coding Basics', hours: 10, priority: 'required' },
          { id: 'M005', titleAr: 'المصطلحات الطبية', titleEn: 'Medical Terminology', hours: 8, priority: 'required' }
        );
      } else {
        moduleList.push(
          { id: 'M006', titleAr: 'ترميز الإجراءات المتقدمة', titleEn: 'Advanced Procedure Coding', hours: 8, priority: 'recommended' },
          { id: 'M007', titleAr: 'إجراءات التدقيق', titleEn: 'Audit Procedures', hours: 6, priority: 'recommended' }
        );
      }

      if (targetCertification.includes('CCP')) {
        moduleList.push(
          { id: 'M008', titleAr: 'الإعداد لشهادة CCP', titleEn: 'CCP Certification Prep', hours: 15, priority: 'required' }
        );
      }

      return { modules: moduleList };
    });

    // Step 3: Calculate success probability
    const prediction = await step.do('calculate-success-probability', async () => {
      const baseProbability = 0.6 + (yearsOfExperience * 0.05);
      const adjustedProbability = Math.min(0.95, baseProbability);
      
      return {
        overallProbability: Math.round(adjustedProbability * 100) / 100,
        factors: [
          { factor: 'Experience', impact: yearsOfExperience > 2 ? 'positive' : 'neutral' },
          { factor: 'Current Role', impact: currentRole.toLowerCase().includes('coder') ? 'positive' : 'neutral' },
        ],
      };
    });

    // Step 4: Create personalized schedule
    const schedule = await step.do('create-schedule', async () => {
      const totalHours = modules.modules.reduce((sum, m) => sum + m.hours, 0);
      const hoursPerWeek = 4;
      const estimatedWeeks = Math.ceil(totalHours / hoursPerWeek);

      return {
        totalModules: modules.modules.length,
        totalEstimatedHours: totalHours,
        recommendedPace: `${hoursPerWeek} hours/week`,
        estimatedCompletionWeeks: estimatedWeeks,
      };
    });

    return {
      learnerId,
      targetCertification,
      learningPath: {
        ...schedule,
        modules: modules.modules,
      },
      skillGaps: [
        { skill: 'ICD-10 Coding', currentLevel: skillAssessment.icd10Coding, targetLevel: 90 },
        { skill: 'SBS Knowledge', currentLevel: skillAssessment.sbsKnowledge, targetLevel: 85 },
        { skill: 'Documentation', currentLevel: skillAssessment.documentation, targetLevel: 95 },
      ],
      successProbability: prediction,
      generatedAt: new Date().toISOString(),
    };
  }
}

// ============================================================================
// MAIN WORKER - HTTP HANDLER
// ============================================================================

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    const path = url.pathname;

    // CORS preflight
    if (req.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    try {
      // Health check
      if (path === '/health' || path === '/') {
        return jsonResponse({
          status: 'healthy',
          service: 'givc-linc-workflows',
          version: '1.0.0',
          timestamp: new Date().toISOString(),
          workflows: ['claims', 'audit', 'learning'],
        });
      }

      // Trigger Claims Workflow
      if (path === '/api/v1/claims/analyze' && req.method === 'POST') {
        const params = await req.json() as ClaimsParams;
        const instance = await env.CLAIMS_WORKFLOW.create({
          params: params,
        });
        return jsonResponse({
          instanceId: instance.id,
          status: await instance.status(),
          message: 'Claims analysis workflow started',
        });
      }

      // Trigger Audit Workflow
      if (path === '/api/audit/simulate' && req.method === 'POST') {
        const params = await req.json() as AuditParams;
        const instance = await env.AUDIT_WORKFLOW.create({
          params: {
            providerId: params.providerId || 'PROVIDER-001',
            sampleSize: params.sampleSize || 50,
            sbsVersion: params.sbsVersion || '2.0',
            auditType: params.auditType || 'routine',
          },
        });
        return jsonResponse({
          instanceId: instance.id,
          status: await instance.status(),
          message: 'Audit simulation workflow started',
        });
      }

      // Trigger Learning Workflow
      if (path === '/api/learning/path' && req.method === 'POST') {
        const params = await req.json() as LearningParams;
        const instance = await env.LEARNING_WORKFLOW.create({
          params: {
            learnerId: params.learnerId || 'LEARNER-001',
            targetCertification: params.targetCertification || 'CCP-KSA',
            yearsOfExperience: params.yearsOfExperience || 1,
            currentRole: params.currentRole || 'Medical Coder',
          },
        });
        return jsonResponse({
          instanceId: instance.id,
          status: await instance.status(),
          message: 'Learning path workflow started',
        });
      }

      // Get workflow status by instance ID
      if (path.startsWith('/api/workflow/status/')) {
        const instanceId = path.split('/').pop();
        if (!instanceId) {
          return jsonResponse({ error: 'Missing instance ID' }, 400);
        }

        // Try to get from each workflow
        try {
          const instance = await env.CLAIMS_WORKFLOW.get(instanceId);
          return jsonResponse({ instanceId, status: await instance.status() });
        } catch {
          try {
            const instance = await env.AUDIT_WORKFLOW.get(instanceId);
            return jsonResponse({ instanceId, status: await instance.status() });
          } catch {
            try {
              const instance = await env.LEARNING_WORKFLOW.get(instanceId);
              return jsonResponse({ instanceId, status: await instance.status() });
            } catch {
              return jsonResponse({ error: 'Instance not found' }, 404);
            }
          }
        }
      }

      return jsonResponse({ error: 'Not found', path }, 404);

    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      return jsonResponse({ error: 'Internal server error', message }, 500);
    }
  },
};

function jsonResponse(data: object, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
