import React from 'react';
import { useLanguage } from '../../contexts/LanguageContext';
import PropTypes from 'prop-types';

const SaudiRTLWrapper = ({ children, className = '', forceDirection }) => {
  const { direction, language } = useLanguage();
  
  const actualDirection = forceDirection || direction;
  
  return (
    <div 
      dir={actualDirection}
      lang={language}
      className={`saudi-rtl-wrapper ${actualDirection === 'rtl' ? 'arabic-mode' : 'english-mode'} ${className}`}
    >
      {children}
    </div>
  );
};

SaudiRTLWrapper.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  forceDirection: PropTypes.oneOf(['ltr', 'rtl'])
};

export default SaudiRTLWrapper;
