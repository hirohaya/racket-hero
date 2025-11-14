import React, { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Verificar se há um usuário autenticado ao montar
  useEffect(() => {
    const loadUser = async () => {
      try {
        const token = authService.getAccessToken();
        if (token) {
          // Tentar obter dados do servidor
          try {
            const currentUser = await authService.getCurrentUser();
            setUser(currentUser);
            setIsAuthenticated(true);
          } catch (error) {
            // Se falhar, usar dados do localStorage
            const storedUser = authService.getUserFromStorage();
            if (storedUser) {
              setUser(storedUser);
              setIsAuthenticated(true);
            } else {
              // Sem dados válidos, logout
              authService.logout();
              setIsAuthenticated(false);
            }
          }
        } else {
          setIsAuthenticated(false);
        }
      } catch (err) {
        console.error('Erro ao carregar usuário:', err);
        setError(err.message);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = async (email, senha) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authService.login(email, senha);
      setUser(response.usuario);
      setIsAuthenticated(true);
      return response;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Erro ao fazer login';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, nome, senha) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authService.register(email, nome, senha);
      setUser(response.usuario);
      setIsAuthenticated(true);
      return response;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Erro ao registrar';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
    setError(null);
  };

  const resetPassword = async (token, novaSenha) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authService.resetPassword(token, novaSenha);
      setUser(response.usuario);
      setIsAuthenticated(true);
      return response;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Erro ao redefinir senha';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    resetPassword,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider');
  }
  return context;
};
