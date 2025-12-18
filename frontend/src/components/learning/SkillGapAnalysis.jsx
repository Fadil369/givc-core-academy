import React from 'react';

const SkillGapAnalysis = ({ skillGaps, language }) => {
  return (
    <div className="skill-gap-analysis">
      <h3>{language === 'ar' ? 'تحليل الفجوات' : 'Skill Gap Analysis'}</h3>
      {/* Visualization stub */}
    </div>
  );
};

export default SkillGapAnalysis;
