import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Arabic translations
const arabicTranslations = {
  common: {
    loading: 'جاري التحميل...',
    error: 'حدث خطأ',
    save: 'حفظ',
    cancel: 'إلغاء',
    delete: 'حذف',
    edit: 'تعديل',
    view: 'عرض',
    search: 'بحث',
    filter: 'تصفية',
    sort: 'ترتيب',
    export: 'تصدير',
    import: 'استيراد',
    settings: 'إعدادات',
    help: 'مساعدة',
    logout: 'تسجيل الخروج'
  },
  
  audit: {
    dashboard: 'لوحة تحكم التدقيق',
    compliance_score: 'درجة المطابقة',
    risk_level: 'مستوى الخطورة',
    sample_size: 'حجم العينة',
    total_errors: 'إجمالي الأخطاء',
    corrective_actions: 'إجراءات تصحيحية',
    fraud_detection: 'كشف الغش',
    audit_outcome: 'نتيجة التدقيق',
    audit_date: 'تاريخ التدقيق',
    provider_id: 'معرف مقدم الخدمة',
    sbs_version: 'نسخة نظام الفوترة السعودي',
    region: 'المنطقة',
    
    outcomes: {
      COMPLIANT: 'مطابق',
      MINOR_ISSUES: 'قضايا ثانوية',
      NEEDS_IMPROVEMENT: 'بحاجة لتحسين',
      NON_COMPLIANT: 'غير مطابق',
      CRITICAL: 'حرج'
    },
    
    risk_levels: {
      low: 'منخفض',
      medium: 'متوسط',
      high: 'مرتفع',
      critical: 'حرج'
    },
    
    error_types: {
      SBS001: 'الكود غير موجود في نظام الفوترة السعودي',
      SBS002: 'عدم توافق الإجراء مع التشخيص',
      SBS003: 'توثيق سريري غير مكتمل',
      SBS004: 'انتهاك قواعد الفوترة',
      SBS005: 'انتهاك قواعد التوقيت للإجراءات المتعددة'
    }
  },
  
  learning: {
    portal: 'بوابة التعلم',
    learning_path: 'مسار التعلم',
    skill_gaps: 'فجوات المهارات',
    progress: 'التقدم',
    simulator: 'محاكي الترميز',
    certification: 'الشهادة',
    modules: 'الوحدات',
    estimated_time: 'الوقت المقدر',
    difficulty: 'الصعوبة',
    prerequisites: 'المتطلبات الأساسية',
    completion_date: 'تاريخ الإكمال',
    success_probability: 'احتمالية النجاح',
    
    skill_types: {
      medical_terminology: 'المصطلحات الطبية',
      anatomy_knowledge: 'معرفة التشريح',
      sbs_coding: 'ترميز نظام الفوترة السعودي',
      icd_10_am: 'ICD-10-AM',
      chi_regulations: 'لوائح مجلس الضمان الصحي'
    },
    
    difficulty_levels: {
      beginner: 'مبتدئ',
      intermediate: 'متوسط',
      advanced: 'متقدم',
      expert: 'خبير'
    },
    
    learning_styles: {
      visual: 'بصري',
      auditory: 'سمعي',
      kinesthetic: 'حركي',
      read_write: 'قراءة وكتابة'
    }
  },
  
  sbs: {
    version_2_0: 'النسخة 2.0',
    version_3_0: 'النسخة 3.0',
    chapter_26: 'الفصل 26 - خدمات التأهيل',
    ems_services: 'خدمات الطوارئ',
    mortuary_services: 'خدمات المشرحة',
    dental_services: 'خدمات الأسنان',
    laboratory_services: 'خدمات المختبر',
    
    coding_standards: {
      with_hierarchy: 'تسلسل "مع"',
      bilateral_rules: 'قواعد الإجراءات الثنائية',
      non_billable_codes: 'أكواد غير قابلة للفوترة',
      rehabilitation_packages: 'حزم التأهيل'
    }
  },
  
  navigation: {
    home: 'الرئيسية',
    audit: 'التدقيق',
    learning: 'التعلم',
    reports: 'التقارير',
    analytics: 'التحليلات',
    administration: 'الإدارة',
    profile: 'الملف الشخصي'
  },
  
  dates: {
    today: 'اليوم',
    yesterday: 'أمس',
    last_7_days: 'آخر 7 أيام',
    last_30_days: 'آخر 30 يوم',
    last_quarter: 'آخر ربع سنة',
    last_year: 'آخر سنة',
    custom_range: 'نطاق مخصص'
  },
  
  regions: {
    riyadh: 'الرياض',
    jeddah: 'جدة',
    dammam: 'الدمام',
    mecca: 'مكة',
    medina: 'المدينة المنورة',
    eastern_province: 'المنطقة الشرقية',
    northern_region: 'المنطقة الشمالية',
    southern_region: 'المنطقة الجنوبية'
  }
};

// English translations
const englishTranslations = {
  common: {
    loading: 'Loading...',
    error: 'An error occurred',
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    edit: 'Edit',
    view: 'View',
    search: 'Search',
    filter: 'Filter',
    sort: 'Sort',
    export: 'Export',
    import: 'Import',
    settings: 'Settings',
    help: 'Help',
    logout: 'Logout'
  },
  
  audit: {
    dashboard: 'Audit Dashboard',
    compliance_score: 'Compliance Score',
    risk_level: 'Risk Level',
    sample_size: 'Sample Size',
    total_errors: 'Total Errors',
    corrective_actions: 'Corrective Actions',
    fraud_detection: 'Fraud Detection',
    audit_outcome: 'Audit Outcome',
    audit_date: 'Audit Date',
    provider_id: 'Provider ID',
    sbs_version: 'SBS Version',
    region: 'Region',
    
    outcomes: {
      COMPLIANT: 'Compliant',
      MINOR_ISSUES: 'Minor Issues',
      NEEDS_IMPROVEMENT: 'Needs Improvement',
      NON_COMPLIANT: 'Non-Compliant',
      CRITICAL: 'Critical'
    },
    
    risk_levels: {
      low: 'Low',
      medium: 'Medium',
      high: 'High',
      critical: 'Critical'
    },
    
    error_types: {
      SBS001: 'Code does not exist in Saudi Billing System',
      SBS002: 'Procedure not appropriate for diagnosis',
      SBS003: 'Incomplete clinical documentation',
      SBS004: 'Billing compliance violation',
      SBS005: 'Violation of timing rules for multiple procedures'
    }
  },
  
  learning: {
    portal: 'Learning Portal',
    learning_path: 'Learning Path',
    skill_gaps: 'Skill Gaps',
    progress: 'Progress',
    simulator: 'Coding Simulator',
    certification: 'Certification',
    modules: 'Modules',
    estimated_time: 'Estimated Time',
    difficulty: 'Difficulty',
    prerequisites: 'Prerequisites',
    completion_date: 'Completion Date',
    success_probability: 'Success Probability',
    
    skill_types: {
      medical_terminology: 'Medical Terminology',
      anatomy_knowledge: 'Anatomy Knowledge',
      sbs_coding: 'SBS Coding',
      icd_10_am: 'ICD-10-AM',
      chi_regulations: 'CHI Regulations'
    },
    
    difficulty_levels: {
      beginner: 'Beginner',
      intermediate: 'Intermediate',
      advanced: 'Advanced',
      expert: 'Expert'
    },
    
    learning_styles: {
      visual: 'Visual',
      auditory: 'Auditory',
      kinesthetic: 'Kinesthetic',
      read_write: 'Read/Write'
    }
  },
  
  sbs: {
    version_2_0: 'Version 2.0',
    version_3_0: 'Version 3.0',
    chapter_26: 'Chapter 26 - Rehabilitation Services',
    ems_services: 'Emergency Services',
    mortuary_services: 'Mortuary Services',
    dental_services: 'Dental Services',
    laboratory_services: 'Laboratory Services',
    
    coding_standards: {
      with_hierarchy: '"With" Hierarchy',
      bilateral_rules: 'Bilateral Procedures Rules',
      non_billable_codes: 'Non-Billable Codes',
      rehabilitation_packages: 'Rehabilitation Packages'
    }
  },
  
  navigation: {
    home: 'Home',
    audit: 'Audit',
    learning: 'Learning',
    reports: 'Reports',
    analytics: 'Analytics',
    administration: 'Administration',
    profile: 'Profile'
  },
  
  dates: {
    today: 'Today',
    yesterday: 'Yesterday',
    last_7_days: 'Last 7 days',
    last_30_days: 'Last 30 days',
    last_quarter: 'Last quarter',
    last_year: 'Last year',
    custom_range: 'Custom Range'
  },
  
  regions: {
    riyadh: 'Riyadh',
    jeddah: 'Jeddah',
    dammam: 'Dammam',
    mecca: 'Mecca',
    medina: 'Medina',
    eastern_province: 'Eastern Province',
    northern_region: 'Northern Region',
    southern_region: 'Southern Region'
  }
};

// i18n initialization
i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      ar: { translation: arabicTranslations },
      en: { translation: englishTranslations }
    },
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    },
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage']
    },
    react: {
      useSuspense: false
    }
  });

// Direction utility
export const getDirection = (lang) => {
  return lang === 'ar' ? 'rtl' : 'ltr';
};

// Format numbers in Arabic
export const formatArabicNumber = (number) => {
  const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return number.toString().replace(/\d/g, (d) => arabicNumbers[d]);
};

// Format Hijri date
export const formatHijriDate = (date) => {
  const hijriMonths = [
    'محرم', 'صفر', 'ربيع الأول', 'ربيع الآخر', 'جمادى الأولى', 'جمادى الآخرة',
    'رجب', 'شعبان', 'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'
  ];
  
  // This is a simplified version - in production, use a library like hijri-date
  const hijriDate = new Intl.DateTimeFormat('ar-SA-u-ca-islamic', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).format(date);
  
  return hijriDate;
};

// Currency formatting for Saudi Riyal
export const formatSAR = (amount, lang = 'en') => {
  const formatter = new Intl.NumberFormat(lang === 'ar' ? 'ar-SA' : 'en-SA', {
    style: 'currency',
    currency: 'SAR',
    minimumFractionDigits: 2
  });
  
  return formatter.format(amount);
};

export default i18n;
