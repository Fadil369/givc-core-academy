import React from 'react';

const LearningPathVisualizer = ({ path, language, onModuleClick }) => {
  return (
    <div className="learning-path-visualizer">
      <h3>{language === 'ar' ? 'مسار التعلم' : 'Learning Path'}</h3>
      {/* Visualization stub */}
    </div>
  );
};

export default LearningPathVisualizer;
