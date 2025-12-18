import React from 'react';

const ComplianceScoreCard = ({ score, riskLevel, previousScore, language }) => {
  return (
    <div className="card compliance-score-card">
      <h3>{language === 'ar' ? 'درجة المطابقة' : 'Compliance Score'}</h3>
      <div className="score">{score}%</div>
      <div className="risk">{riskLevel}</div>
    </div>
  );
};

export default ComplianceScoreCard;
