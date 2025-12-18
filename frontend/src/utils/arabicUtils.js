// Arabic text utilities
export const arabicText = {
  // Arabic numbers 0-9
  numbers: ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'],
  
  // Arabic months (Hijri)
  hijriMonths: [
    'محرم', 'صفر', 'ربيع الأول', 'ربيع الآخر', 'جمادى الأولى', 'جمادى الآخرة',
    'رجب', 'شعبان', 'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'
  ],
  
  // Arabic weekdays
  weekdays: ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'],
  
  // Common medical coding terms in Arabic
  medicalTerms: {
    diagnosis: 'تشخيص',
    procedure: 'إجراء',
    code: 'كود',
    billing: 'فوترة',
    compliance: 'مطابقة',
    audit: 'تدقيق',
    rehabilitation: 'تأهيل',
    emergency: 'طوارئ',
    laboratory: 'مختبر'
  }
};

// Convert numbers to Arabic numerals
export const toArabicNumerals = (number) => {
  if (typeof number !== 'string' && typeof number !== 'number') {
    return number;
  }
  
  const str = number.toString();
  return str.replace(/\d/g, (d) => arabicText.numbers[d]);
};

// Convert Arabic numerals to Western
export const fromArabicNumerals = (arabicStr) => {
  if (typeof arabicStr !== 'string') {
    return arabicStr;
  }
  
  const westernNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
  return arabicStr.replace(/[٠١٢٣٤٥٦٧٨٩]/g, (char) => {
    const index = arabicText.numbers.indexOf(char);
    return index !== -1 ? westernNumbers[index] : char;
  });
};

// Format date in Hijri
export const formatHijriDate = (date) => {
  try {
    const hijriDate = new Intl.DateTimeFormat('ar-SA-u-ca-islamic', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      weekday: 'long'
    }).format(date);
    
    return hijriDate;
  } catch (error) {
    // Fallback to Gregorian
    return date.toLocaleDateString('ar-SA');
  }
};

// Format SBS code with Arabic explanation
export const formatSBSCode = (code, explanation) => {
  return {
    code,
    arabic: `كود نظام الفوترة السعودي: ${code}`,
    english: `SBS Code: ${code}`,
    explanation: explanation || ''
  };
};

// Check if text contains Arabic characters
export const containsArabic = (text) => {
  if (!text || typeof text !== 'string') return false;
  
  // Arabic Unicode range: \u0600-\u06FF
  const arabicRegex = /[\u0600-\u06FF]/;
  return arabicRegex.test(text);
};

// Determine text direction
export const getTextDirection = (text) => {
  if (!text) return 'ltr';
  
  const arabicRegex = /[\u0600-\u06FF]/;
  const hebrewRegex = /[\u0590-\u05FF]/;
  
  if (arabicRegex.test(text) || hebrewRegex.test(text)) {
    return 'rtl';
  }
  
  return 'ltr';
};

// Truncate Arabic text properly
export const truncateArabic = (text, maxLength, suffix = '...') => {
  if (!text || text.length <= maxLength) return text;
  
  // For Arabic, we need to truncate from the beginning
  if (containsArabic(text)) {
    const truncated = text.substring(text.length - maxLength);
    return suffix + truncated;
  }
  
  // For Latin scripts, truncate from end
  return text.substring(0, maxLength) + suffix;
};

// Sort Arabic text properly
export const sortArabic = (array, key) => {
  return array.sort((a, b) => {
    const aValue = key ? a[key] : a;
    const bValue = key ? b[key] : b;
    
    if (containsArabic(aValue) && containsArabic(bValue)) {
      return aValue.localeCompare(bValue, 'ar');
    }
    
    return aValue.localeCompare(bValue);
  });
};

// Format phone number for Saudi Arabia
export const formatSaudiPhone = (phone) => {
  if (!phone) return '';
  
  const cleaned = phone.replace(/\D/g, '');
  
  if (cleaned.length === 9) {
    // Landline: 01XXXXXXX
    return cleaned.replace(/(\d{1})(\d{3})(\d{3})(\d{2})/, '$1 $2 $3 $4');
  } else if (cleaned.length === 10) {
    // Mobile: 05XXXXXXXX
    return cleaned.replace(/(\d{2})(\d{3})(\d{3})(\d{2})/, '$1 $2 $3 $4');
  }
  
  return phone;
};
