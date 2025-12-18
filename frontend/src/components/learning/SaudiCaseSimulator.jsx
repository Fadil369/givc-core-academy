import React from 'react';

const SaudiCaseSimulator = ({ sbsVersion, region, language }) => {
  return (
    <div className="saudi-case-simulator">
      <h3>{language === 'ar' ? 'محاكي الحالات' : 'Case Simulator'}</h3>
      <p>SBS Version: {sbsVersion}</p>
      <p>Region: {region}</p>
    </div>
  );
};

export default SaudiCaseSimulator;
