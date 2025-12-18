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
