import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

const resources = {
  en: {
    translation: {
      welcome: 'Welcome to GIVC Core Academy',
      login: 'Login',
      register: 'Register',
      courses: 'Courses',
      enrollments: 'My Enrollments',
      assessments: 'Assessments',
      profile: 'Profile',
    },
  },
  ar: {
    translation: {
      welcome: 'مرحباً بك في أكاديمية GIVC الأساسية',
      login: 'تسجيل الدخول',
      register: 'التسجيل',
      courses: 'الدورات',
      enrollments: 'تسجيلاتي',
      assessments: 'الاختبارات',
      profile: 'الملف الشخصي',
    },
  },
}

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'ar',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  })

export default i18n
