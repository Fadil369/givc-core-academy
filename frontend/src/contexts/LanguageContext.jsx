'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import i18n, { getDirection } from '../services/localization/i18n';

const LanguageContext = createContext();

// Helper to safely access localStorage
const getStoredLanguage = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('preferred_language') || 'en';
  }
  return 'en';
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('en');
  const [direction, setDirection] = useState('ltr');
  const [mounted, setMounted] = useState(false);
  
  // Initialize on client side only
  useEffect(() => {
    const storedLang = getStoredLanguage();
    setLanguage(storedLang);
    setDirection(getDirection(storedLang));
    setMounted(true);
  }, []);
  
  useEffect(() => {
    if (!mounted) return;
    
    // Update i18n
    i18n.changeLanguage(language);
    
    // Update direction
    const newDirection = getDirection(language);
    setDirection(newDirection);
    
    // Update HTML dir attribute
    document.documentElement.dir = newDirection;
    document.documentElement.lang = language;
    
    // Update font based on language
    if (language === 'ar') {
      document.body.classList.add('arabic-font');
      document.body.classList.remove('english-font');
    } else {
      document.body.classList.add('english-font');
      document.body.classList.remove('arabic-font');
    }
    
    // Save preference
    localStorage.setItem('preferred_language', language);
  }, [language, mounted]);
  
  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'ar' : 'en');
  };
  
  const setLanguageWithDirection = (lang) => {
    setLanguage(lang);
  };
  
  const translate = (key, options) => {
    return i18n.t(key, options);
  };
  
  const formatNumber = (number) => {
    if (language === 'ar') {
      // Convert to Arabic numerals
      const arabicNumerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
      return number.toString().replace(/\d/g, d => arabicNumerals[d]);
    }
    return new Intl.NumberFormat(language).format(number);
  };
  
  const formatDate = (date, options = {}) => {
    const formatOptions = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      ...options
    };
    
    if (language === 'ar') {
      // Use Hijri calendar for Arabic
      return new Intl.DateTimeFormat('ar-SA-u-ca-islamic', formatOptions).format(date);
    }
    
    return new Intl.DateTimeFormat(language, formatOptions).format(date);
  };
  
  const formatCurrency = (amount) => {
    const formatter = new Intl.NumberFormat(language === 'ar' ? 'ar-SA' : 'en-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 2
    });
    
    return formatter.format(amount);
  };
  
  return (
    <LanguageContext.Provider
      value={{
        language,
        direction,
        toggleLanguage,
        setLanguage: setLanguageWithDirection,
        t: translate,
        formatNumber,
        formatDate,
        formatCurrency,
        isRTL: direction === 'rtl'
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};
