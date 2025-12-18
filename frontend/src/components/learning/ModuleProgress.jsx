import React from 'react';

const ModuleProgress = ({ progress, language }) => {
  return (
    <div className="module-progress">
      <h3>{language === 'ar' ? 'التقدم' : 'Progress'}</h3>
      {/* Progress stub */}
    </div>
  );
};

export default ModuleProgress;
