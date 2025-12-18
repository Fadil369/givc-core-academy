import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState({
    id: 'user-123',
    full_name: 'Dr. Fadil',
    region: 'Riyadh',
    educational_background: 'Medical Coding',
    years_of_experience: 5,
    target_certification: 'CCP-KSA'
  });

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
