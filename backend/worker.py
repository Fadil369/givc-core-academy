"""
GIVC Core Academy Backend - Cloudflare Worker Entry Point
This is a lightweight API handler for Cloudflare Workers (Python)
"""

from js import Response, Headers
import json
from datetime import datetime
import random
import math

# =============================================
# MOCK SERVICES (simplified for Worker runtime)
# =============================================

class AuditService:
    """Simplified CHI Audit Service for Worker environment"""
    
    @staticmethod
    def simulate_audit(provider_id: str, sample_size: int = 50, sbs_version: str = "2.0"):
        """Simulate a CHI audit cycle"""
        # Generate mock audit results
        audit_id = f"CHI-AUDIT-{datetime.now().strftime('%Y%m%d')}-{provider_id[:8]}"
        
        # Random compliance score with realistic distribution
        base_score = random.gauss(85, 10)
        compliance_score = max(0, min(100, base_score))
        
        # Determine risk level
        if compliance_score >= 90:
            risk_level = "low"
        elif compliance_score >= 75:
            risk_level = "medium"
        elif compliance_score >= 60:
            risk_level = "high"
        else:
            risk_level = "critical"
        
        # Generate error distribution
        total_errors = int((100 - compliance_score) / 5)
        
        # Mock audit results
        audit_results = []
        error_types = [
            {"code": "SBS001", "desc_ar": "كود غير موجود", "desc_en": "Code not found"},
            {"code": "SBS002", "desc_ar": "عدم توافق التشخيص", "desc_en": "Diagnosis mismatch"},
            {"code": "SBS003", "desc_ar": "توثيق غير مكتمل", "desc_en": "Incomplete documentation"},
            {"code": "SBS004", "desc_ar": "فوترة مكررة", "desc_en": "Duplicate billing"},
            {"code": "SBS005", "desc_ar": "انتهاك التوقيت", "desc_en": "Timing violation"},
        ]
        
        for i in range(sample_size):
            has_error = random.random() < (total_errors / sample_size)
            audit_results.append({
                "claim_id": f"CLM-{random.randint(10000, 99999)}",
                "has_errors": has_error,
                "errors": [random.choice(error_types)] if has_error else [],
                "penalty_points": random.randint(1, 5) if has_error else 0
            })
        
        # Determine outcome
        if compliance_score >= 90:
            audit_outcome = "COMPLIANT"
        elif compliance_score >= 75:
            audit_outcome = "MINOR_ISSUES"
        elif compliance_score >= 60:
            audit_outcome = "REQUIRES_IMPROVEMENT"
        else:
            audit_outcome = "NON_COMPLIANT"
        
        return {
            "audit_id": audit_id,
            "audit_date": datetime.now().isoformat(),
            "provider_id": provider_id,
            "sbs_version": sbs_version,
            "compliance_score": round(compliance_score, 2),
            "risk_level": risk_level,
            "audit_outcome": audit_outcome,
            "sample_size": sample_size,
            "total_errors": total_errors,
            "audit_results": audit_results[:10],  # Return first 10 for demo
            "corrective_actions": AuditService._generate_corrective_actions(risk_level, compliance_score),
            "summary": {
                "ar": f"تدقيق CHI مكتمل. درجة الامتثال: {round(compliance_score, 1)}%",
                "en": f"CHI Audit complete. Compliance score: {round(compliance_score, 1)}%"
            }
        }
    
    @staticmethod
    def _generate_corrective_actions(risk_level: str, score: float):
        actions = []
        if risk_level in ["high", "critical"]:
            actions.append({
                "action_id": "CAP-001",
                "type": "mandatory_training",
                "title_ar": "تدريب إلزامي على معايير الترميز",
                "title_en": "Mandatory Coding Standards Training",
                "deadline_days": 30
            })
        if score < 85:
            actions.append({
                "action_id": "CAP-002",
                "type": "follow_up_audit",
                "title_ar": "مراجعة تدقيقية متابعة",
                "title_en": "Follow-up Compliance Audit",
                "deadline_days": 90 if score < 70 else 180
            })
        return actions


class LearningService:
    """Adaptive Learning Path Service"""
    
    @staticmethod
    def generate_learning_path(learner_profile: dict):
        """Generate personalized learning path based on profile"""
        target_cert = learner_profile.get("target_certification", "CCP-KSA")
        experience = learner_profile.get("years_of_experience", 0)
        
        # Base modules for all learners
        modules = [
            {"id": "M001", "title_ar": "أساسيات ICD-10-AM", "title_en": "ICD-10-AM Fundamentals", "hours": 8},
            {"id": "M002", "title_ar": "نظام الفوترة السعودي (SBS)", "title_en": "Saudi Billing System (SBS)", "hours": 12},
            {"id": "M003", "title_ar": "معايير التوثيق السريري", "title_en": "Clinical Documentation Standards", "hours": 6},
        ]
        
        # Add advanced modules based on experience
        if experience < 2:
            modules.extend([
                {"id": "M004", "title_ar": "أساسيات الترميز الطبي", "title_en": "Medical Coding Basics", "hours": 10},
                {"id": "M005", "title_ar": "المصطلحات الطبية", "title_en": "Medical Terminology", "hours": 8},
            ])
        else:
            modules.extend([
                {"id": "M006", "title_ar": "ترميز الإجراءات المتقدمة", "title_en": "Advanced Procedure Coding", "hours": 8},
                {"id": "M007", "title_ar": "إجراءات التدقيق", "title_en": "Audit Procedures", "hours": 6},
            ])
        
        # Add certification-specific modules
        if "CCP" in target_cert:
            modules.append({"id": "M008", "title_ar": "الإعداد لشهادة CCP", "title_en": "CCP Certification Prep", "hours": 15})
        
        total_hours = sum(m["hours"] for m in modules)
        success_probability = min(0.95, 0.6 + (experience * 0.05))
        
        return {
            "learning_path": {
                "total_modules": len(modules),
                "total_estimated_hours": total_hours,
                "modules": modules,
                "recommended_pace": "4 hours/week" if total_hours > 40 else "2 hours/week"
            },
            "skill_gaps": [
                {"skill": "ICD-10 Coding", "current_level": 60 + experience * 5, "target_level": 90},
                {"skill": "SBS Knowledge", "current_level": 50 + experience * 7, "target_level": 85},
                {"skill": "Documentation", "current_level": 70, "target_level": 95}
            ],
            "success_probability": {"overall_probability": round(success_probability, 2)},
            "estimated_completion_weeks": math.ceil(total_hours / 4)
        }


class FraudDetectionService:
    """Simplified Fraud Detection for Worker"""
    
    @staticmethod
    def analyze_audit_batch(audit_results: list):
        """Analyze audit results for fraud indicators"""
        fraud_indicators = []
        fraud_risk_score = 0
        
        # Count errors by type
        error_counts = {}
        for result in audit_results:
            for error in result.get("errors", []):
                code = error.get("code", "UNKNOWN")
                error_counts[code] = error_counts.get(code, 0) + 1
        
        # Detect patterns
        for code, count in error_counts.items():
            if count > len(audit_results) * 0.3:  # More than 30% have same error
                fraud_indicators.append({
                    "indicator": f"Systematic {code} errors",
                    "severity": "high",
                    "count": count
                })
                fraud_risk_score += 20
        
        # Cap at 100
        fraud_risk_score = min(100, fraud_risk_score)
        
        return {
            "fraud_risk_score": fraud_risk_score,
            "fraud_indicators": fraud_indicators,
            "requires_investigation": fraud_risk_score > 50,
            "analyzed_claims": len(audit_results)
        }


# =============================================
# REQUEST HANDLER
# =============================================

def json_response(data, status=200):
    """Create JSON response with CORS headers"""
    headers = Headers.new({
        "content-type": "application/json",
        "access-control-allow-origin": "*",
        "access-control-allow-methods": "GET, POST, OPTIONS",
        "access-control-allow-headers": "Content-Type, Authorization"
    })
    return Response.new(json.dumps(data, default=str), status=status, headers=headers)


async def on_fetch(request, env):
    """Main request handler for Cloudflare Worker"""
    try:
        url = str(request.url)
        method = str(request.method)
        
        # Extract path from URL
        path = "/" + url.split("/", 3)[-1].split("?")[0] if "/" in url else "/"
        
        # Handle CORS preflight
        if method == "OPTIONS":
            return json_response({})
        
        # ===== API Routes =====
        
        # Health check
        if path == "/api/health" or path == "/health":
            return json_response({
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "service": "givc-core-academy-backend"
            })
        
        # Audit simulation
        if path == "/api/audit/simulate" and method == "POST":
            try:
                body = await request.json()
                data = body.to_py() if hasattr(body, 'to_py') else dict(body)
            except:
                data = {}
            
            result = AuditService.simulate_audit(
                provider_id=data.get("provider_id", "PROVIDER-001"),
                sample_size=data.get("sample_size", 50),
                sbs_version=data.get("sbs_version", "2.0")
            )
            
            # Add fraud detection
            fraud_result = FraudDetectionService.analyze_audit_batch(result["audit_results"])
            result["fraud_detection"] = fraud_result
            
            # Store to D1 if available
            if hasattr(env, 'DB'):
                try:
                    await env.DB.prepare(
                        "INSERT INTO audit_logs (audit_id, provider_id, score, created_at) VALUES (?, ?, ?, datetime('now'))"
                    ).bind(result["audit_id"], result["provider_id"], result["compliance_score"]).run()
                except Exception as db_error:
                    result["db_status"] = f"Storage skipped: {str(db_error)}"
            
            return json_response(result)
        
        # Learning path generation
        if path == "/api/learning/path" and method == "POST":
            try:
                body = await request.json()
                data = body.to_py() if hasattr(body, 'to_py') else dict(body)
            except:
                data = {}
            
            result = LearningService.generate_learning_path(data)
            return json_response(result)
        
        # Fraud analysis endpoint
        if path == "/api/fraud/analyze" and method == "POST":
            try:
                body = await request.json()
                data = body.to_py() if hasattr(body, 'to_py') else dict(body)
            except:
                data = {}
            
            audit_results = data.get("audit_results", [])
            result = FraudDetectionService.analyze_audit_batch(audit_results)
            return json_response(result)
        
        # API info
        if path == "/api" or path == "/":
            return json_response({
                "name": "GIVC Core Academy API",
                "version": "1.0.0",
                "endpoints": [
                    {"path": "/api/health", "method": "GET", "description": "Health check"},
                    {"path": "/api/audit/simulate", "method": "POST", "description": "Simulate CHI audit"},
                    {"path": "/api/learning/path", "method": "POST", "description": "Generate learning path"},
                    {"path": "/api/fraud/analyze", "method": "POST", "description": "Analyze for fraud patterns"}
                ],
                "documentation": "https://github.com/Fadil369/givc-core-academy"
            })
        
        # 404 for unknown routes
        return json_response({"error": "Not Found", "path": path}, status=404)
        
    except Exception as e:
        return json_response({"error": str(e), "type": type(e).__name__}, status=500)
