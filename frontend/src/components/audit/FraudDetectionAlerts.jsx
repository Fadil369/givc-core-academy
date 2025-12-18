import React from 'react';

const FraudDetectionAlerts = ({ fraudIndicators, riskScore, language }) => {
  return (
    <div className="card fraud-detection-alerts">
      <h3>{language === 'ar' ? 'تنبيهات الغش' : 'Fraud Alerts'}</h3>
      <p>Risk Score: {riskScore}</p>
    </div>
  );
};

export default FraudDetectionAlerts;
