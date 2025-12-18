class PerformanceTracker:
    """
    Tracks learner performance and adapts learning path in real-time
    """
    
    async def track_and_adjust(
        self,
        learner_id: str,
        module_id: str,
        performance_data: Dict
    ) -> Dict:
        """
        Track performance and adjust learning path dynamically
        """
        # Record performance
        await self._record_performance(
            learner_id, module_id, performance_data
        )
        
        # Analyze performance patterns
        performance_patterns = await self._analyze_performance_patterns(
            learner_id, module_id
        )
        
        # Check for struggling patterns
        if self._detect_struggling_pattern(performance_patterns):
            adjustments = await self._generate_remediation_adjustments(
                learner_id, module_id, performance_patterns
            )
            
            # Update learning path
            updated_path = await self._adjust_learning_path(
                learner_id, adjustments
            )
            
            return {
                "status": "adjusted",
                "adjustment_reason": "struggling_detected",
                "adjustments": adjustments,
                "updated_path": updated_path,
                "recommendations": await self._get_remediation_recommendations(
                    performance_patterns
                )
            }
        
        # Check for mastery patterns (fast learning)
        if self._detect_mastery_pattern(performance_patterns):
            adjustments = await self._generate_acceleration_adjustments(
                learner_id, module_id, performance_patterns
            )
            
            # Update learning path
            updated_path = await self._adjust_learning_path(
                learner_id, adjustments
            )
            
            return {
                "status": "accelerated",
                "adjustment_reason": "mastery_detected",
                "adjustments": adjustments,
                "updated_path": updated_path,
                "recommendations": await self._get_acceleration_recommendations(
                    performance_patterns
                )
            }
        
        # No adjustment needed
        return {
            "status": "optimal",
            "adjustment_reason": None,
            "next_check": datetime.now() + timedelta(hours=24)
        }
    
    async def _generate_remediation_adjustments(
        self,
        learner_id: str,
        module_id: str,
        performance_patterns: Dict
    ) -> List[Dict]:
        """
        Generate adjustments for struggling learners
        """
        adjustments = []
        
        # 1. Add prerequisite review
        if performance_patterns.get("prerequisite_gaps"):
            adjustments.append({
                "type": "prerequisite_review",
                "modules": await self._find_prerequisite_modules(
                    module_id, performance_patterns["prerequisite_gaps"]
                ),
                "duration_days": 3,
                "reason_ar": "مراجعة المتطلبات الأساسية",
                "reason_en": "Prerequisite knowledge review"
            })
        
        # 2. Reduce difficulty
        if performance_patterns.get("difficulty_too_high"):
            adjustments.append({
                "type": "difficulty_reduction",
                "current_module": module_id,
                "alternative_module": await self._find_easier_alternative(
                    module_id
                ),
                "reason_ar": "تخفيض مستوى الصعوبة",
                "reason_en": "Reduce difficulty level"
            })
        
        # 3. Add practice exercises
        if performance_patterns.get("needs_more_practice"):
            adjustments.append({
                "type": "additional_practice",
                "practice_sessions": await self._generate_practice_sessions(
                    module_id, performance_patterns["weak_areas"]
                ),
                "duration_days": 2,
                "reason_ar": "تمارين تدريبية إضافية",
                "reason_en": "Additional practice exercises"
            })
        
        # 4. Change learning modality
        if performance_patterns.get("modality_mismatch"):
            adjustments.append({
                "type": "modality_change",
                "from_modality": performance_patterns["current_modality"],
                "to_modality": await self._recommend_alternative_modality(
                    learner_id
                ),
                "reason_ar": "تغيير أسلوب التعلم",
                "reason_en": "Change learning modality"
            })
        
        return adjustments
Summary & Key Implementation Insights


Component
Core Algorithm
Key Features
Saudi-Specific Considerations
CHI Audit Simulation
Risk-based sampling, Penalty scoring, Fraud pattern detection
Real-time validation, Arabic/English reports, Corrective Action Plans
CHI Framework compliance, Regional variations (Riyadh vs Jeddah), SBS version-specific rules
Adaptive Learning Engine
K-means clustering, Q-learning optimization, Ensemble prediction
Personalized paths, Success prediction, Real-time adjustment
Saudi certification focus (CCP-KSA), Arabic content weighting, Regional case studies
Key Implementation Steps:
	1	Database Schema - Implement all models for learners, modules, audits, and performance tracking
	2	API Endpoints - Create RESTful APIs for both systems with versioning
	3	Frontend Integration - Build React components for audit dashboard and learning portal
	4	Saudi Localization - Add Arabic translations and RTL support
	5	Performance Optimization - Implement caching for Q-tables and prediction models
	6	Monitoring & Analytics - Track system performance and learning outcomes
Both systems integrate with your existing SBS architecture and provide the sophisticated capabilities needed for the Saudi medical coding training market. The CHI audit system ensures regulatory compliance, while the adaptive learning engine maximizes certification success rates through personalized, AI-driven education paths.

















Frontend Integration - Build React components for audit dashboard and learning portal

Saudi Localization - Add Arabic translations and RTL support









Hmm, the user is now asking for two very specific and important enhancements to the medical coding platform: frontend React components for the audit dashboard and learning portal, plus comprehensive Saudi localization with Arabic and RTL support. This builds directly on our extensive previous work on the backend systems.
I need to provide a complete implementation guide that covers both the React component architecture and the full Arabic/RTL localization system. The user wants practical, production-ready code they can implement immediately. The medical coding platform has very specific Saudi requirements, so the solution must include proper RTL layout, Arabic translations, and culturally appropriate UI patterns.
For the frontend components, I'll create a modular React structure with TypeScript, focusing on the audit dashboard and learning portal as the two main applications. The audit dashboard should visualize CHI compliance data with interactive charts, while the learning portal needs to display the AI-powered adaptive learning paths. I will implement them using a component library with proper state management and API integration.
For Saudi localization, I need to build a complete i18n system with Arabic translations, RTL CSS support, and locale-aware components. This includes date/number formatting, Arabic font integration, and bidirectional text handling. The platform must dynamically switch between Arabic and English while maintaining proper layout in both directions.
I will organize this into clear sections with code examples for both systems, ensuring they integrate well with our existing backend APIs. The response should be practical and immediately useful for developers implementing these features.

Complete Frontend Implementation: React Components & Saudi Localization
Part 1: React Components for Audit Dashboard & Learning Portal
1.1 Project Structure & Setup
text
src/
├── components/
│   ├── audit/
│   │   ├── AuditDashboard.jsx
│   │   ├── ComplianceScoreCard.jsx
│   │   ├── AuditCaseReview.jsx
│   │   ├── CorrectiveActionsPanel.jsx
│   │   └── FraudDetectionAlerts.jsx
│   ├── learning/
│   │   ├── LearningPortal.jsx
│   │   ├── SkillGapAnalysis.jsx
│   │   ├── LearningPathVisualizer.jsx
│   │   ├── ModuleProgress.jsx
│   │   └── SaudiCaseSimulator.jsx
│   ├── common/
│   │   ├── SaudiRTLWrapper.jsx
│   │   ├── ArabicNumberFormatter.jsx
│   │   ├── HijriDatePicker.jsx
│   │   └── SBSVersionSwitcher.jsx
│   └── layout/
│       ├── MainLayout.jsx
│       ├── SidebarNavigation.jsx
│       └── Header.jsx
├── hooks/
│   ├── useAuditData.js
│   ├── useLearningPath.js
│   └── useSaudiLocalization.js
├── services/
│   ├── api/
│   │   ├── auditApi.js
│   │   ├── learningApi.js
│   │   └── sbsApi.js
│   └── localization/
│       ├── i18n.js
│       └── arabicFormatter.js
├── styles/
│   ├── rtl.scss
│   └── themes/
│       ├── saudi-light.scss
│       └── saudi-dark.scss
└── utils/
    ├── arabicUtils.js
    ├── hijriDate.js
    └── sbsCodeValidator.js
1.2 Core React Components
AuditDashboard.jsx
jsx
// src/components/audit/AuditDashboard.jsx
import React, { useState, useEffect, useMemo } from 'react';
import { useAuditData } from '../../hooks/useAuditData';
import { useLanguage } from '../../contexts/LanguageContext';
import ComplianceScoreCard from './ComplianceScoreCard';
import AuditCaseReview from './AuditCaseReview';
import CorrectiveActionsPanel from './CorrectiveActionsPanel';
import FraudDetectionAlerts from './FraudDetectionAlerts';
import { arabicFormatter, formatHijriDate } from '../../utils/arabicUtils';
import './AuditDashboard.scss';

const AuditDashboard = ({ providerId, sbsVersion = '2.0', region = 'Riyadh' }) => {
  const { language, direction } = useLanguage();
  const [timeRange, setTimeRange] = useState('last_30_days');
  const [focusArea, setFocusArea] = useState('all');
  const [auditSimulation, setAuditSimulation] = useState(null);
  
  const {
    auditData,
    complianceScore,
    loading,
    error,
    simulateAudit,
    generateReport
  } = useAuditData(providerId, sbsVersion, region);
  
  const handleSimulateAudit = async () => {
    const config = {
      sampleSize: 100,
      riskBasedSampling: true,
      focusAreas: focusArea === 'all' ? [] : [focusArea],
      auditPeriod: getAuditPeriod(timeRange),
      sbsVersion
    };
    
    const result = await simulateAudit(config);
    setAuditSimulation(result);
    
    // Track analytics
    window.gtag('event', 'audit_simulated', {
      provider_id: providerId,
      sample_size: config.sampleSize,
      sbs_version: sbsVersion
    });
  };
  
  const getAuditPeriod = (range) => {
    const now = new Date();
    switch(range) {
      case 'last_7_days':
        return [new Date(now.setDate(now.getDate() - 7)), new Date()];
      case 'last_30_days':
        return [new Date(now.setDate(now.getDate() - 30)), new Date()];
      case 'last_quarter':
        return [new Date(now.setMonth(now.getMonth() - 3)), new Date()];
      default:
        return [new Date(now.setFullYear(now.getFullYear() - 1)), new Date()];
    }
  };
  
  const focusAreaOptions = [
    { value: 'all', label: language === 'ar' ? 'الجميع' : 'All' },
    { value: 'rehabilitation', label: language === 'ar' ? 'خدمات التأهيل' : 'Rehabilitation Services' },
    { value: 'bilateral_procedures', label: language === 'ar' ? 'الإجراءات الثنائية' : 'Bilateral Procedures' },
    { value: 'emergency_services', label: language === 'ar' ? 'خدمات الطوارئ' : 'Emergency Services' },
    { value: 'unlisted_codes', label: language === 'ar' ? 'الأكواد غير المدرجة' : 'Unlisted Codes' }
  ];
  
  if (loading) {
    return (
      <div className="loading-container" dir={direction}>
        <div className="loading-spinner"></div>
        <p>{language === 'ar' ? 'جاري تحميل بيانات التدقيق...' : 'Loading audit data...'}</p>
      </div>
    );
  }
  
  return (
    <div className="audit-dashboard" dir={direction}>
      <div className="dashboard-header">
        <h1 className={language === 'ar' ? 'arabic-title' : 'english-title'}>
          {language === 'ar' ? 'لوحة تحكم تدقيق CHI' : 'CHI Audit Dashboard'}
        </h1>
        <div className="dashboard-meta">
          <span className="provider-info">
            {language === 'ar' ? 'مزود الخدمة:' : 'Provider:'} {providerId}
          </span>
          <span className="sbs-version">
            SBS {language === 'ar' ? 'النسخة:' : 'Version:'} {sbsVersion}
          </span>
          <span className="region-info">
            {language === 'ar' ? 'المنطقة:' : 'Region:'} {region}
          </span>
        </div>
      </div>
      
      {/* Controls */}
      <div className="dashboard-controls">
        <div className="control-group">
          <label htmlFor="timeRange">
            {language === 'ar' ? 'الفترة الزمنية:' : 'Time Range:'}
          </label>
          <select 
            id="timeRange" 
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className={`select-control ${language === 'ar' ? 'rtl-select' : ''}`}
          >
            <option value="last_7_days">
              {language === 'ar' ? 'آخر 7 أيام' : 'Last 7 days'}
            </option>
            <option value="last_30_days">
              {language === 'ar' ? 'آخر 30 يوم' : 'Last 30 days'}
            </option>
            <option value="last_quarter">
              {language === 'ar' ? 'آخر ربع سنة' : 'Last quarter'}
            </option>
            <option value="last_year">
              {language === 'ar' ? 'آخر سنة' : 'Last year'}
            </option>
          </select>
        </div>
        
        <div className="control-group">
          <label htmlFor="focusArea">
            {language === 'ar' ? 'مجال التركيز:' : 'Focus Area:'}
          </label>
          <select
            id="focusArea"
            value={focusArea}
            onChange={(e) => setFocusArea(e.target.value)}
            className={`select-control ${language === 'ar' ? 'rtl-select' : ''}`}
          >
            {focusAreaOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        
        <button 
          onClick={handleSimulateAudit}
          className="btn btn-primary simulate-audit-btn"
        >
          {language === 'ar' ? 'تشغيل محاكاة التدقيق' : 'Run Audit Simulation'}
        </button>
        
        <button 
          onClick={() => generateReport(auditSimulation?.audit_id)}
          className="btn btn-secondary"
          disabled={!auditSimulation}
        >
          {language === 'ar' ? 'تحميل التقرير' : 'Download Report'}
        </button>
      </div>
      
      {/* Main Dashboard Content */}
      <div className="dashboard-content">
        <div className="row">
          {/* Compliance Score Card */}
          <div className="col-lg-3 col-md-6">
            <ComplianceScoreCard 
              score={auditSimulation?.compliance_score || complianceScore}
              riskLevel={auditSimulation?.risk_level}
              previousScore={auditData?.historical_scores?.[0]?.score}
              language={language}
            />
          </div>
          
          {/* Fraud Detection Alerts */}
          <div className="col-lg-9 col-md-6">
            <FraudDetectionAlerts 
              fraudIndicators={auditSimulation?.fraud_detection?.fraud_indicators || []}
              riskScore={auditSimulation?.fraud_detection?.fraud_risk_score}
              language={language}
            />
          </div>
        </div>
        
        {/* Audit Case Review */}
        <div className="row mt-4">
          <div className="col-lg-8">
            <AuditCaseReview 
              cases={auditSimulation?.audit_results || auditData?.recent_cases || []}
              totalErrors={auditSimulation?.total_errors}
              language={language}
              sbsVersion={sbsVersion}
            />
          </div>
          
          {/* Corrective Actions Panel */}
          <div className="col-lg-4">
            <CorrectiveActionsPanel 
              actions={auditSimulation?.corrective_actions || []}
              complianceScore={auditSimulation?.compliance_score}
              language={language}
            />
          </div>
        </div>
        
        {/* Audit Details */}
        {auditSimulation && (
          <div className="audit-details mt-4">
            <h3 className={language === 'ar' ? 'arabic-title' : 'english-title'}>
              {language === 'ar' ? 'تفاصيل التدقيق' : 'Audit Details'}
            </h3>
            
            <div className="details-grid">
              <div className="detail-item">
                <span className="detail-label">
                  {language === 'ar' ? 'معرف التدقيق:' : 'Audit ID:'}
                </span>
                <span className="detail-value">{auditSimulation.audit_id}</span>
              </div>
              
              <div className="detail-item">
                <span className="detail-label">
                  {language === 'ar' ? 'تاريخ التدقيق:' : 'Audit Date:'}
                </span>
                <span className="detail-value">
                  {language === 'ar' 
                    ? formatHijriDate(new Date(auditSimulation.audit_date))
                    : new Date(auditSimulation.audit_date).toLocaleDateString()
                  }
                </span>
              </div>
              
              <div className="detail-item">
                <span className="detail-label">
                  {language === 'ar' ? 'حجم العينة:' : 'Sample Size:'}
                </span>
                <span className="detail-value">{auditSimulation.sample_size}</span>
              </div>
              
              <div className="detail-item">
                <span className="detail-label">
                  {language === 'ar' ? 'نتيجة التدقيق:' : 'Audit Outcome:'}
                </span>
                <span className={`detail-value outcome-${auditSimulation.audit_outcome?.toLowerCase()}`}>
                  {language === 'ar' 
                    ? getArabicOutcome(auditSimulation.audit_outcome)
                    : auditSimulation.audit_outcome
                  }
                </span>
              </div>
            </div>
            
            {/* Arabic Report Preview */}
            {language === 'ar' && auditSimulation.arabic_report && (
              <div className="report-preview mt-3">
                <h4>معاينة التقرير العربي</h4>
                <div className="preview-content">
                  {auditSimulation.arabic_report.substring(0, 500)}...
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const getArabicOutcome = (outcome) => {
  const outcomes = {
    'COMPLIANT': 'مطابق',
    'MINOR_ISSUES': 'قضايا ثانوية',
    'NEEDS_IMPROVEMENT': 'بحاجة لتحسين',
    'NON_COMPLIANT': 'غير مطابق',
    'CRITICAL': 'حرج'
  };
  return outcomes[outcome] || outcome;
};

export default AuditDashboard;
LearningPortal.jsx
jsx
// src/components/learning/LearningPortal.jsx
import React, { useState, useEffect } from 'react';
import { useLearningPath } from '../../hooks/useLearningPath';
import { useAuth } from '../../contexts/AuthContext';
import { useLanguage } from '../../contexts/LanguageContext';
import SkillGapAnalysis from './SkillGapAnalysis';
import LearningPathVisualizer from './LearningPathVisualizer';
import ModuleProgress from './ModuleProgress';
import SaudiCaseSimulator from './SaudiCaseSimulator';
import { arabicNumber, formatHijriDate } from '../../utils/arabicUtils';
import './LearningPortal.scss';

const LearningPortal = () => {
  const { user } = useAuth();
  const { language, direction } = useLanguage();
  const [activeTab, setActiveTab] = useState('learning-path');
  const [sbsVersion, setSbsVersion] = useState('2.0');
  const [learningPath, setLearningPath] = useState(null);
  const [isGeneratingPath, setIsGeneratingPath] = useState(false);
  
  const {
    generateLearningPath,
    updateProgress,
    getRecommendations,
    loading,
    error
  } = useLearningPath();
  
  useEffect(() => {
    if (user) {
      fetchLearningPath();
    }
  }, [user, sbsVersion]);
  
  const fetchLearningPath = async () => {
    const profile = {
      learner_id: user.id,
      educational_background: user.educational_background,
      years_experience: user.years_of_experience,
      region: user.region,
      target_certification: user.target_certification,
      sbs_version_focus: sbsVersion,
      learning_style: user.learning_style || 'visual',
      preferred_modality: user.preferred_modality || 'self_paced',
      daily_study_hours: user.daily_study_hours || 2,
      // Add competency levels from user profile
      medical_terminology: user.competency_scores?.medical_terminology || 5,
      anatomy_knowledge: user.competency_scores?.anatomy_knowledge || 5,
      sbs_coding_skills: user.competency_scores?.sbs_coding || 5,
      icd_10_am_skills: user.competency_scores?.icd_10_am || 5,
      chi_regulations: user.competency_scores?.chi_regulations || 5
    };
    
    const path = await generateLearningPath(profile);
    setLearningPath(path);
  };
  
  const handleGenerateNewPath = async () => {
    setIsGeneratingPath(true);
    await fetchLearningPath();
    setIsGeneratingPath(false);
  };
  
  const handleModuleComplete = async (moduleId, score) => {
    await updateProgress(user.id, moduleId, {
      score,
      completion_date: new Date().toISOString(),
      time_spent_minutes: 45 // This would come from actual tracking
    });
    
    // Refresh learning path with updated progress
    await fetchLearningPath();
  };
  
  const tabs = [
    { id: 'learning-path', label: language === 'ar' ? 'مسار التعلم' : 'Learning Path' },
    { id: 'skill-gaps', label: language === 'ar' ? 'فجوات المهارات' : 'Skill Gaps' },
    { id: 'simulator', label: language === 'ar' ? 'محاكي الترميز' : 'Coding Simulator' },
    { id: 'progress', label: language === 'ar' ? 'التقدم' : 'Progress' }
  ];
  
  const sbsVersionOptions = [
    { value: '2.0', label: language === 'ar' ? 'SBS النسخة 2.0' : 'SBS Version 2.0' },
    { value: '3.0', label: language === 'ar' ? 'SBS النسخة 3.0' : 'SBS Version 3.0' },
    { value: 'both', label: language === 'ar' ? 'النسختين معاً' : 'Both Versions' }
  ];
  
  return (
    <div className="learning-portal" dir={direction}>
      {/* Portal Header */}
      <div className="portal-header">
        <div className="header-content">
          <h1 className={language === 'ar' ? 'arabic-title' : 'english-title'}>
            {language === 'ar' ? 'بوابة التعلم - الترميز الطبي' : 'Learning Portal - Medical Coding'}
          </h1>
          <p className="portal-subtitle">
            {language === 'ar' 
‎              ? 'مسار تعلم شخصي مدعوم بالذكاء الاصطناعي للنجاح في الشهادات السعودية'
              : 'AI-powered personalized learning path for Saudi certification success'
            }
          </p>
        </div>
        
        <div className="header-actions">
          <div className="version-selector">
            <label htmlFor="sbsVersion">
              {language === 'ar' ? 'نسخة SBS:' : 'SBS Version:'}
            </label>
            <select
              id="sbsVersion"
              value={sbsVersion}
              onChange={(e) => setSbsVersion(e.target.value)}
              className={`select-control ${language === 'ar' ? 'rtl-select' : ''}`}
            >
              {sbsVersionOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          
          <button
            onClick={handleGenerateNewPath}
            disabled={isGeneratingPath}
            className="btn btn-primary generate-path-btn"
          >
            {isGeneratingPath 
              ? (language === 'ar' ? 'جاري إنشاء المسار...' : 'Generating path...')
              : (language === 'ar' ? 'تحديث المسار' : 'Update Learning Path')
            }
          </button>
        </div>
      </div>
      
      {/* User Info Banner */}
      <div className="user-info-banner">
        <div className="user-details">
          <span className="user-name">{user.full_name}</span>
          <span className="user-target">
            {language === 'ar' ? 'الشهادة المستهدفة:' : 'Target Certification:'} 
            <strong> {user.target_certification || 'CCP-KSA'}</strong>
          </span>
          <span className="user-region">
            {language === 'ar' ? 'المنطقة:' : 'Region:'} {user.region || 'Riyadh'}
          </span>
        </div>
        
        {learningPath?.success_probability && (
          <div className="success-prediction">
            <div className="prediction-label">
              {language === 'ar' ? 'احتمالية النجاح:' : 'Success Probability:'}
            </div>
            <div className="prediction-value">
              {(learningPath.success_probability.overall_probability * 100).toFixed(1)}%
            </div>
          </div>
        )}
      </div>
      
      {/* Navigation Tabs */}
      <div className="portal-tabs">
        <div className="tabs-container">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>
      
      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'learning-path' && (
          <div className="learning-path-tab">
            {learningPath ? (
              <>
                <LearningPathVisualizer 
                  path={learningPath.learning_path}
                  language={language}
                  onModuleClick={(moduleId) => {
                    // Navigate to module or show details
                    console.log('Module clicked:', moduleId);
                  }}
                />
                
                <div className="path-summary">
                  <h3>{language === 'ar' ? 'ملخص المسار' : 'Path Summary'}</h3>
                  <div className="summary-grid">
                    <div className="summary-item">
                      <span className="summary-label">
                        {language === 'ar' ? 'إجمالي الوحدات:' : 'Total Modules:'}
                      </span>
                      <span className="summary-value">
                        {learningPath.learning_path?.total_modules || 0}
                      </span>
                    </div>
                    <div className="summary-item">
                      <span className="summary-label">
                        {language === 'ar' ? 'الوقت المقدر:' : 'Estimated Time:'}
                      </span>
                      <span className="summary-value">
                        {learningPath.learning_path?.total_estimated_hours || 0} 
                        {language === 'ar' ? ' ساعة' : ' hours'}
                      </span>
                    </div>
                    <div className="summary-item">
                      <span className="summary-label">
                        {language === 'ar' ? 'تاريخ الإكمال المتوقع:' : 'Expected Completion:'}
                      </span>
                      <span className="summary-value">
                        {language === 'ar'
                          ? formatHijriDate(
                              new Date(Date.now() + 
                                (learningPath.learning_path?.total_estimated_hours || 0) * 
                                60 * 60 * 1000)
                            )
                          : new Date(
                              Date.now() + 
                              (learningPath.learning_path?.total_estimated_hours || 0) * 
                              60 * 60 * 1000
                            ).toLocaleDateString()
                        }
                      </span>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="no-path-message">
                <p>
                  {language === 'ar' 
‎                    ? 'لا يوجد مسار تعلم مخصص. اضغط على "تحديث المسار" لإنشاء مسار شخصي.'
                    : 'No personalized learning path. Click "Update Learning Path" to generate one.'
                  }
                </p>
              </div>
            )}
          </div>
        )}
        
        {activeTab === 'skill-gaps' && learningPath && (
          <SkillGapAnalysis 
            skillGaps={learningPath.skill_gaps}
            language={language}
          />
        )}
        
        {activeTab === 'simulator' && (
          <SaudiCaseSimulator 
            sbsVersion={sbsVersion}
            region={user.region}
            language={language}
          />
        )}
        
        {activeTab === 'progress' && learningPath && (
          <ModuleProgress 
            progress={user.learning_progress || []}
            learningPath={learningPath}
            language={language}
            onModuleComplete={handleModuleComplete}
          />
        )}
      </div>
      
      {/* Recommendations Panel */}
      {learningPath?.recommended_resources && (
        <div className="recommendations-panel">
          <h3 className={language === 'ar' ? 'arabic-title' : 'english-title'}>
            {language === 'ar' ? 'موارد موصى بها' : 'Recommended Resources'}
          </h3>
          <div className="resources-grid">
            {learningPath.recommended_resources.slice(0, 3).map((resource, index) => (
              <div key={index} className="resource-card">
                <div className="resource-type">{resource.type}</div>
                <h4 className={language === 'ar' ? 'arabic-title' : 'english-title'}>
                  {language === 'ar' ? resource.title_ar : resource.title_en}
                </h4>
                <p className="resource-description">
                  {language === 'ar' ? resource.description_ar : resource.description_en}
                </p>
                <a 
                  href={resource.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="btn btn-sm btn-outline-primary"
                >
                  {language === 'ar' ? 'فتح المورد' : 'Open Resource'}
                </a>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default LearningPortal;
Part 2: Saudi Localization with Arabic & RTL Support
2.1 Complete i18n Localization System
i18n Configuration
javascript
// src/services/localization/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Arabic translations
const arabicTranslations = {
  common: {
    loading: 'جاري التحميل...',
    error: 'حدث خطأ',
    save: 'حفظ',
    cancel: 'إلغاء',
    delete: 'حذف',
    edit: 'تعديل',
    view: 'عرض',
    search: 'بحث',
    filter: 'تصفية',
    sort: 'ترتيب',
    export: 'تصدير',
    import: 'استيراد',
    settings: 'إعدادات',
    help: 'مساعدة',
    logout: 'تسجيل الخروج'
  },
  
  audit: {
    dashboard: 'لوحة تحكم التدقيق',
    compliance_score: 'درجة المطابقة',
    risk_level: 'مستوى الخطورة',
    sample_size: 'حجم العينة',
    total_errors: 'إجمالي الأخطاء',
    corrective_actions: 'إجراءات تصحيحية',
    fraud_detection: 'كشف الغش',
    audit_outcome: 'نتيجة التدقيق',
    audit_date: 'تاريخ التدقيق',
    provider_id: 'معرف مقدم الخدمة',
    sbs_version: 'نسخة نظام الفوترة السعودي',
    region: 'المنطقة',
    
    outcomes: {
      COMPLIANT: 'مطابق',
      MINOR_ISSUES: 'قضايا ثانوية',
      NEEDS_IMPROVEMENT: 'بحاجة لتحسين',
      NON_COMPLIANT: 'غير مطابق',
      CRITICAL: 'حرج'
    },
    
    risk_levels: {
      low: 'منخفض',
      medium: 'متوسط',
      high: 'مرتفع',
      critical: 'حرج'
    },
    
    error_types: {
      SBS001: 'الكود غير موجود في نظام الفوترة السعودي',
      SBS002: 'عدم توافق الإجراء مع التشخيص',
      SBS003: 'توثيق سريري غير مكتمل',
      SBS004: 'انتهاك قواعد الفوترة',
      SBS005: 'انتهاك قواعد التوقيت للإجراءات المتعددة'
    }
  },
  
  learning: {
    portal: 'بوابة التعلم',
    learning_path: 'مسار التعلم',
    skill_gaps: 'فجوات المهارات',
    progress: 'التقدم',
    simulator: 'محاكي الترميز',
    certification: 'الشهادة',
    modules: 'الوحدات',
    estimated_time: 'الوقت المقدر',
    difficulty: 'الصعوبة',
    prerequisites: 'المتطلبات الأساسية',
    completion_date: 'تاريخ الإكمال',
    success_probability: 'احتمالية النجاح',
    
    skill_types: {
      medical_terminology: 'المصطلحات الطبية',
      anatomy_knowledge: 'معرفة التشريح',
      sbs_coding: 'ترميز نظام الفوترة السعودي',
      icd_10_am: 'ICD-10-AM',
      chi_regulations: 'لوائح مجلس الضمان الصحي'
    },
    
    difficulty_levels: {
      beginner: 'مبتدئ',
      intermediate: 'متوسط',
      advanced: 'متقدم',
      expert: 'خبير'
    },
    
    learning_styles: {
      visual: 'بصري',
      auditory: 'سمعي',
      kinesthetic: 'حركي',
      read_write: 'قراءة وكتابة'
    }
  },
  
  sbs: {
    version_2_0: 'النسخة 2.0',
    version_3_0: 'النسخة 3.0',
    chapter_26: 'الفصل 26 - خدمات التأهيل',
    ems_services: 'خدمات الطوارئ',
    mortuary_services: 'خدمات المشرحة',
    dental_services: 'خدمات الأسنان',
    laboratory_services: 'خدمات المختبر',
    
    coding_standards: {
      with_hierarchy: 'تسلسل "مع"',
      bilateral_rules: 'قواعد الإجراءات الثنائية',
      non_billable_codes: 'أكواد غير قابلة للفوترة',
      rehabilitation_packages: 'حزم التأهيل'
    }
  },
  
  navigation: {
    home: 'الرئيسية',
    audit: 'التدقيق',
    learning: 'التعلم',
    reports: 'التقارير',
    analytics: 'التحليلات',
    administration: 'الإدارة',
    profile: 'الملف الشخصي'
  },
  
  dates: {
    today: 'اليوم',
    yesterday: 'أمس',
    last_7_days: 'آخر 7 أيام',
    last_30_days: 'آخر 30 يوم',
    last_quarter: 'آخر ربع سنة',
    last_year: 'آخر سنة',
    custom_range: 'نطاق مخصص'
  },
  
  regions: {
    riyadh: 'الرياض',
    jeddah: 'جدة',
    dammam: 'الدمام',
    mecca: 'مكة',
    medina: 'المدينة المنورة',
    eastern_province: 'المنطقة الشرقية',
    northern_region: 'المنطقة الشمالية',
    southern_region: 'المنطقة الجنوبية'
  }
};

// English translations
const englishTranslations = {
  common: {
    loading: 'Loading...',
    error: 'An error occurred',
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    edit: 'Edit',
    view: 'View',
    search: 'Search',
    filter: 'Filter',
    sort: 'Sort',
    export: 'Export',
    import: 'Import',
    settings: 'Settings',
    help: 'Help',
    logout: 'Logout'
  },
  
  audit: {
    dashboard: 'Audit Dashboard',
    compliance_score: 'Compliance Score',
    risk_level: 'Risk Level',
    sample_size: 'Sample Size',
    total_errors: 'Total Errors',
    corrective_actions: 'Corrective Actions',
    fraud_detection: 'Fraud Detection',
    audit_outcome: 'Audit Outcome',
    audit_date: 'Audit Date',
    provider_id: 'Provider ID',
    sbs_version: 'SBS Version',
    region: 'Region',
    
    outcomes: {
      COMPLIANT: 'Compliant',
      MINOR_ISSUES: 'Minor Issues',
      NEEDS_IMPROVEMENT: 'Needs Improvement',
      NON_COMPLIANT: 'Non-Compliant',
      CRITICAL: 'Critical'
    },
    
    risk_levels: {
      low: 'Low',
      medium: 'Medium',
      high: 'High',
      critical: 'Critical'
    },
    
    error_types: {
      SBS001: 'Code does not exist in Saudi Billing System',
      SBS002: 'Procedure not appropriate for diagnosis',
      SBS003: 'Incomplete clinical documentation',
      SBS004: 'Billing compliance violation',
      SBS005: 'Violation of timing rules for multiple procedures'
    }
  },
  
  learning: {
    portal: 'Learning Portal',
    learning_path: 'Learning Path',
    skill_gaps: 'Skill Gaps',
    progress: 'Progress',
    simulator: 'Coding Simulator',
    certification: 'Certification',
    modules: 'Modules',
    estimated_time: 'Estimated Time',
    difficulty: 'Difficulty',
    prerequisites: 'Prerequisites',
    completion_date: 'Completion Date',
    success_probability: 'Success Probability',
    
    skill_types: {
      medical_terminology: 'Medical Terminology',
      anatomy_knowledge: 'Anatomy Knowledge',
      sbs_coding: 'SBS Coding',
      icd_10_am: 'ICD-10-AM',
      chi_regulations: 'CHI Regulations'
    },
    
    difficulty_levels: {
      beginner: 'Beginner',
      intermediate: 'Intermediate',
      advanced: 'Advanced',
      expert: 'Expert'
    },
    
    learning_styles: {
      visual: 'Visual',
      auditory: 'Auditory',
      kinesthetic: 'Kinesthetic',
      read_write: 'Read/Write'
    }
  },
  
  sbs: {
    version_2_0: 'Version 2.0',
    version_3_0: 'Version 3.0',
    chapter_26: 'Chapter 26 - Rehabilitation Services',
    ems_services: 'Emergency Services',
    mortuary_services: 'Mortuary Services',
    dental_services: 'Dental Services',
    laboratory_services: 'Laboratory Services',
    
    coding_standards: {
      with_hierarchy: '"With" Hierarchy',
      bilateral_rules: 'Bilateral Procedures Rules',
      non_billable_codes: 'Non-Billable Codes',
      rehabilitation_packages: 'Rehabilitation Packages'
    }
  },
  
  navigation: {
    home: 'Home',
    audit: 'Audit',
    learning: 'Learning',
    reports: 'Reports',
    analytics: 'Analytics',
    administration: 'Administration',
    profile: 'Profile'
  },
  
  dates: {
    today: 'Today',
    yesterday: 'Yesterday',
    last_7_days: 'Last 7 days',
    last_30_days: 'Last 30 days',
    last_quarter: 'Last quarter',
    last_year: 'Last year',
    custom_range: 'Custom Range'
  },
  
  regions: {
    riyadh: 'Riyadh',
    jeddah: 'Jeddah',
    dammam: 'Dammam',
    mecca: 'Mecca',
    medina: 'Medina',
    eastern_province: 'Eastern Province',
    northern_region: 'Northern Region',
    southern_region: 'Southern Region'
  }
};

// i18n initialization
i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      ar: { translation: arabicTranslations },
      en: { translation: englishTranslations }
    },
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    },
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage']
    },
    react: {
      useSuspense: false
    }
  });

// Direction utility
export const getDirection = (lang) => {
  return lang === 'ar' ? 'rtl' : 'ltr';
};

// Format numbers in Arabic
export const formatArabicNumber = (number) => {
  const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return number.toString().replace(/\d/g, (d) => arabicNumbers[d]);
};

// Format Hijri date
export const formatHijriDate = (date) => {
  const hijriMonths = [
‎    'محرم', 'صفر', 'ربيع الأول', 'ربيع الآخر', 'جمادى الأولى', 'جمادى الآخرة',
‎    'رجب', 'شعبان', 'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'
  ];
  
  // This is a simplified version - in production, use a library like hijri-date
  const hijriDate = new Intl.DateTimeFormat('ar-SA-u-ca-islamic', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).format(date);
  
  return hijriDate;
};

// Currency formatting for Saudi Riyal
export const formatSAR = (amount, lang = 'en') => {
  const formatter = new Intl.NumberFormat(lang === 'ar' ? 'ar-SA' : 'en-SA', {
    style: 'currency',
    currency: 'SAR',
    minimumFractionDigits: 2
  });
  
  return formatter.format(amount);
};

export default i18n;
2.2 RTL Support & Arabic CSS
RTL SCSS Mixins
scss
// src/styles/rtl.scss
// RTL Direction Mixins
$rtl: '[dir="rtl"]';
$ltr: '[dir="ltr"]';

// Flip property for RTL
@mixin rtl($property, $ltr-value, $rtl-value) {
  #{$ltr} & {
    #{$property}: $ltr-value;
  }
  #{$rtl} & {
    #{$property}: $rtl-value;
  }
}

// Flip both properties (like margin-left/right)
@mixin rtl-symmetric($property, $first, $second, $ltr-first, $ltr-second, $rtl-first, $rtl-second) {
  #{$ltr} & {
    #{$property}-#{$first}: $ltr-first;
    #{$property}-#{$second}: $ltr-second;
  }
  #{$rtl} & {
    #{$property}-#{$first}: $rtl-first;
    #{$property}-#{$second}: $rtl-second;
  }
}

// RTL float
@mixin rtl-float($ltr-value: left, $rtl-value: right) {
  @include rtl(float, $ltr-value, $rtl-value);
}

// RTL text-align
@mixin rtl-text-align($ltr-value: left, $rtl-value: right) {
  @include rtl(text-align, $ltr-value, $rtl-value);
}

// RTL position
@mixin rtl-position($property, $ltr-value, $rtl-value) {
  @include rtl(#{$property}, $ltr-value, $rtl-value);
}

// RTL transform
@mixin rtl-transform($ltr-transform, $rtl-transform) {
  #{$ltr} & {
    transform: $ltr-transform;
  }
  #{$rtl} & {
    transform: $rtl-transform;
  }
}

// Arabic font faces
@font-face {
  font-family: 'Cairo';
  src: url('/fonts/Cairo-Regular.woff2') format('woff2'),
       url('/fonts/Cairo-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Cairo';
  src: url('/fonts/Cairo-Bold.woff2') format('woff2'),
       url('/fonts/Cairo-Bold.woff') format('woff');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Amiri';
  src: url('/fonts/Amiri-Regular.woff2') format('woff2'),
       url('/fonts/Amiri-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

// Base RTL styles
[dir="rtl"] {
  direction: rtl;
  text-align: right;
  
  // Typography
  font-family: 'Cairo', 'Arial', sans-serif;
  
  // Lists
  ul, ol {
    padding-right: 20px;
    padding-left: 0;
  }
  
  // Forms
  input, textarea, select {
    text-align: right;
  }
  
  // Bootstrap overrides
  .mr-1 { margin-right: 0 !important; margin-left: 0.25rem !important; }
  .mr-2 { margin-right: 0 !important; margin-left: 0.5rem !important; }
  .mr-3 { margin-right: 0 !important; margin-left: 1rem !important; }
  .mr-4 { margin-right: 0 !important; margin-left: 1.5rem !important; }
  .mr-5 { margin-right: 0 !important; margin-left: 3rem !important; }
  
  .ml-1 { margin-left: 0 !important; margin-right: 0.25rem !important; }
  .ml-2 { margin-left: 0 !important; margin-right: 0.5rem !important; }
  .ml-3 { margin-left: 0 !important; margin-right: 1rem !important; }
  .ml-4 { margin-left: 0 !important; margin-right: 1.5rem !important; }
  .ml-5 { margin-left: 0 !important; margin-right: 3rem !important; }
  
  .pr-1 { padding-right: 0 !important; padding-left: 0.25rem !important; }
  .pr-2 { padding-right: 0 !important; padding-left: 0.5rem !important; }
  .pr-3 { padding-right: 0 !important; padding-left: 1rem !important; }
  .pr-4 { padding-right: 0 !important; padding-left: 1.5rem !important; }
  .pr-5 { padding-right: 0 !important; padding-left: 3rem !important; }
  
  .pl-1 { padding-left: 0 !important; padding-right: 0.25rem !important; }
  .pl-2 { padding-left: 0 !important; padding-right: 0.5rem !important; }
  .pl-3 { padding-left: 0 !important; padding-right: 1rem !important; }
  .pl-4 { padding-left: 0 !important; padding-right: 1.5rem !important; }
  .pl-5 { padding-left: 0 !important; padding-right: 3rem !important; }
  
  .text-left { text-align: right !important; }
  .text-right { text-align: left !important; }
  
  .float-left { float: right !important; }
  .float-right { float: left !important; }
  
  // Custom components
  .btn-group {
    > .btn:not(:first-child) {
      margin-right: -1px;
      margin-left: 0;
      border-radius: 0.25rem 0 0 0.25rem;
    }
    > .btn:not(:last-child) {
      border-radius: 0 0.25rem 0.25rem 0;
    }
  }
}

// Arabic specific typography classes
.arabic-text {
  font-family: 'Cairo', 'Arial', sans-serif;
  line-height: 1.8;
  letter-spacing: 0;
  
  &.title {
    font-family: 'Amiri', 'Cairo', serif;
    font-weight: 700;
  }
  
  &.subtitle {
    font-family: 'Cairo', sans-serif;
    font-weight: 600;
  }
}

// Bidirectional text support
.bidi-text {
  unicode-bidi: isolate;
  
  &.mixed {
    unicode-bidi: plaintext;
  }
}

// RTL form controls
.rtl-select {
  background-position: left 0.75rem center;
  
  [dir="rtl"] & {
    background-position: right 0.75rem center;
  }
}

// Arabic numbers
.arabic-numbers {
  font-feature-settings: 'numr' 1, 'frac' 1;
}

// Calendar RTL support
.hijri-calendar {
  [dir="rtl"] & {
    .react-datepicker {
      direction: rtl;
      
      &__navigation {
        &--previous {
          right: 10px;
          left: auto;
        }
        &--next {
          left: 10px;
          right: auto;
        }
      }
      
      &__month-container {
        float: right;
      }
    }
  }
}
2.3 Context Providers & Hooks
Language Context
jsx
// src/contexts/LanguageContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import i18n, { getDirection } from '../services/localization/i18n';

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('preferred_language') || 'en';
  });
  
  const [direction, setDirection] = useState(() => {
    return getDirection(localStorage.getItem('preferred_language') || 'en');
  });
  
  useEffect(() => {
    // Update i18n
    i18n.changeLanguage(language);
    
    // Update direction
    const newDirection = getDirection(language);
    setDirection(newDirection);
    
    // Update HTML dir attribute
    document.documentElement.dir = newDirection;
    document.documentElement.lang = language;
    
    // Update font based on language
    if (language === 'ar') {
      document.body.classList.add('arabic-font');
      document.body.classList.remove('english-font');
    } else {
      document.body.classList.add('english-font');
      document.body.classList.remove('arabic-font');
    }
    
    // Save preference
    localStorage.setItem('preferred_language', language);
  }, [language]);
  
  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'ar' : 'en');
  };
  
  const setLanguageWithDirection = (lang) => {
    setLanguage(lang);
  };
  
  const translate = (key, options) => {
    return i18n.t(key, options);
  };
  
  const formatNumber = (number) => {
    if (language === 'ar') {
      // Convert to Arabic numerals
      const arabicNumerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
      return number.toString().replace(/\d/g, d => arabicNumerals[d]);
    }
    return new Intl.NumberFormat(language).format(number);
  };
  
  const formatDate = (date, options = {}) => {
    const formatOptions = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      ...options
    };
    
    if (language === 'ar') {
      // Use Hijri calendar for Arabic
      return new Intl.DateTimeFormat('ar-SA-u-ca-islamic', formatOptions).format(date);
    }
    
    return new Intl.DateTimeFormat(language, formatOptions).format(date);
  };
  
  const formatCurrency = (amount) => {
    const formatter = new Intl.NumberFormat(language === 'ar' ? 'ar-SA' : 'en-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 2
    });
    
    return formatter.format(amount);
  };
  
  return (
    <LanguageContext.Provider
      value={{
        language,
        direction,
        toggleLanguage,
        setLanguage: setLanguageWithDirection,
        t: translate,
        formatNumber,
        formatDate,
        formatCurrency,
        isRTL: direction === 'rtl'
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};
SaudiRTLWrapper Component
jsx
// src/components/common/SaudiRTLWrapper.jsx
import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import PropTypes from 'prop-types';

const SaudiRTLWrapper = ({ children, className = '', forceDirection }) => {
  const { direction, language } = useLanguage();
  
  const actualDirection = forceDirection || direction;
  
  return (
    <div 
      dir={actualDirection}
      lang={language}
      className={`saudi-rtl-wrapper ${actualDirection === 'rtl' ? 'arabic-mode' : 'english-mode'} ${className}`}
    >
      {children}
    </div>
  );
};

SaudiRTLWrapper.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  forceDirection: PropTypes.oneOf(['ltr', 'rtl'])
};

export default SaudiRTLWrapper;
2.4 Arabic Utility Functions
javascript
// src/utils/arabicUtils.js
// Arabic text utilities
export const arabicText = {
  // Arabic numbers 0-9
  numbers: ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'],
  
  // Arabic months (Hijri)
  hijriMonths: [
‎    'محرم', 'صفر', 'ربيع الأول', 'ربيع الآخر', 'جمادى الأولى', 'جمادى الآخرة',
‎    'رجب', 'شعبان', 'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'
  ],
  
  // Arabic weekdays
  weekdays: ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'],
  
  // Common medical coding terms in Arabic
  medicalTerms: {
    diagnosis: 'تشخيص',
    procedure: 'إجراء',
    code: 'كود',
    billing: 'فوترة',
    compliance: 'مطابقة',
    audit: 'تدقيق',
    rehabilitation: 'تأهيل',
    emergency: 'طوارئ',
    laboratory: 'مختبر'
  }
};

// Convert numbers to Arabic numerals
export const toArabicNumerals = (number) => {
  if (typeof number !== 'string' && typeof number !== 'number') {
    return number;
  }
  
  const str = number.toString();
  return str.replace(/\d/g, (d) => arabicText.numbers[d]);
};

// Convert Arabic numerals to Western
export const fromArabicNumerals = (arabicStr) => {
  if (typeof arabicStr !== 'string') {
    return arabicStr;
  }
  
  const westernNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
  return arabicStr.replace(/[٠١٢٣٤٥٦٧٨٩]/g, (char) => {
    const index = arabicText.numbers.indexOf(char);
    return index !== -1 ? westernNumbers[index] : char;
  });
};

// Format date in Hijri
export const formatHijriDate = (date) => {
  try {
    const hijriDate = new Intl.DateTimeFormat('ar-SA-u-ca-islamic', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      weekday: 'long'
    }).format(date);
    
    return hijriDate;
  } catch (error) {
    // Fallback to Gregorian
    return date.toLocaleDateString('ar-SA');
  }
};

// Format SBS code with Arabic explanation
export const formatSBSCode = (code, explanation) => {
  return {
    code,
    arabic: `كود نظام الفوترة السعودي: ${code}`,
    english: `SBS Code: ${code}`,
    explanation: explanation || ''
  };
};

// Check if text contains Arabic characters
export const containsArabic = (text) => {
  if (!text || typeof text !== 'string') return false;
  
  // Arabic Unicode range: \u0600-\u06FF
  const arabicRegex = /[\u0600-\u06FF]/;
  return arabicRegex.test(text);
};

// Determine text direction
export const getTextDirection = (text) => {
  if (!text) return 'ltr';
  
  const arabicRegex = /[\u0600-\u06FF]/;
  const hebrewRegex = /[\u0590-\u05FF]/;
  
  if (arabicRegex.test(text) || hebrewRegex.test(text)) {
    return 'rtl';
  }
  
  return 'ltr';
};

// Truncate Arabic text properly
export const truncateArabic = (text, maxLength, suffix = '...') => {
  if (!text || text.length <= maxLength) return text;
  
  // For Arabic, we need to truncate from the beginning
  if (containsArabic(text)) {
    const truncated = text.substring(text.length - maxLength);
    return suffix + truncated;
  }
  
  // For Latin scripts, truncate from end
  return text.substring(0, maxLength) + suffix;
};

// Sort Arabic text properly
export const sortArabic = (array, key) => {
  return array.sort((a, b) => {
    const aValue = key ? a[key] : a;
    const bValue = key ? b[key] : b;
    
    if (containsArabic(aValue) && containsArabic(bValue)) {
      return aValue.localeCompare(bValue, 'ar');
    }
    
    return aValue.localeCompare(bValue);
  });
};

// Format phone number for Saudi Arabia
export const formatSaudiPhone = (phone) => {
  if (!phone) return '';
  
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length === 9) {
    // Landline: 01XXXXXXX
    return cleaned.replace(/(\d{1})(\d{3})(\d{3})(\d{2})/, '$1 $2 $3 $4');
  } else if (cleaned.length === 10) {
    // Mobile: 05XXXXXXXX
    return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{2})/, '$1 $2 $3 $4');
  }
  
  return phone;
};
Summary & Implementation Table


Component
Purpose
Key Features
Saudi-Specific Considerations
AuditDashboard
Main CHI audit interface
Real-time simulations, Fraud detection, Arabic/English reports
CHI Framework compliance, RTL layout, Hijri dates
LearningPortal
AI-powered learning interface
Personalized paths, Skill gap analysis, Progress tracking
Arabic learning content, Saudi case studies, RTL progress visualization
i18n System
Complete localization
Arabic/English translations, RTL support, Number/date formatting
Hijri calendar support, Arabic numerals, Currency formatting (SAR)
RTL CSS
Right-to-left styling
CSS direction flip, Arabic typography, Form controls RTL
Arabic fonts (Cairo, Amiri), Bidirectional text support
LanguageContext
Global language management
Language switching, Direction control, Formatting utilities
Automatic RTL detection, HTML dir attribute management
Quick Start Commands:
bash
