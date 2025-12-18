import React from 'react';

const CorrectiveActionsPanel = ({ actions, complianceScore, language }) => {
  return (
    <div className="card corrective-actions-panel">
      <h3>{language === 'ar' ? 'الإجراءات التصحيحية' : 'Corrective Actions'}</h3>
      <ul>
        {actions.map((action, i) => <li key={i}>{action}</li>)}
      </ul>
    </div>
  );
};

export default CorrectiveActionsPanel;
