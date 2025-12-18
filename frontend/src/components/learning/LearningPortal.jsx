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
              ? 'مسار تعلم شخصي مدعوم بالذكاء الاصطناعي للنجاح في الشهادات السعودية'
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
                    ? 'لا يوجد مسار تعلم مخصص. اضغط على "تحديث المسار" لإنشاء مسار شخصي.'
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
