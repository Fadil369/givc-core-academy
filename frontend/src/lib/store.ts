import { create } from 'zustand'

interface User {
  id: number
  email: string
  full_name: string
  full_name_ar?: string
  user_type: string
  preferred_language: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  setUser: (user: User | null) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({ user: null, isAuthenticated: false })
  },
}))

interface UIState {
  language: 'ar' | 'en'
  direction: 'rtl' | 'ltr'
  toggleLanguage: () => void
  setLanguage: (lang: 'ar' | 'en') => void
}

export const useUIStore = create<UIState>((set) => ({
  language: 'ar',
  direction: 'rtl',
  toggleLanguage: () =>
    set((state) => ({
      language: state.language === 'ar' ? 'en' : 'ar',
      direction: state.direction === 'rtl' ? 'ltr' : 'rtl',
    })),
  setLanguage: (lang) =>
    set({
      language: lang,
      direction: lang === 'ar' ? 'rtl' : 'ltr',
    }),
}))
