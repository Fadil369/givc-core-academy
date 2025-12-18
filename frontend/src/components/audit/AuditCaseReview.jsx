import React from 'react';

const AuditCaseReview = ({ cases, totalErrors, language }) => {
  return (
    <div className="card audit-case-review">
      <h3>{language === 'ar' ? 'مراجعة الحالات' : 'Case Review'}</h3>
      <p>Total Errors: {totalErrors}</p>
    </div>
  );
};

export default AuditCaseReview;
