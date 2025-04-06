import { createContext, useContext, useState } from 'react';
import { jwtDecode } from 'jwt-decode'; // 👈 Correto

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  const login = (token) => {
    const decoded = jwtDecode(token); // 👈 Correto
    setUser(decoded); // exemplo: setUser({ id: decoded.sub })
    setToken(token);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
