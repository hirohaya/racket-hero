import React, { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/authService';
import logger from '../services/logger';

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
        logger.info('Carregando usuário autenticado...');
        const token = authService.getAccessToken();
        if (token) {
          // Tentar obter dados do servidor
          try {
            const currentUser = await authService.getCurrentUser();
            setUser(currentUser);
            setIsAuthenticated(true);
            logger.info('Usuário carregado com sucesso', { email: currentUser.email });
          } catch (error) {
            // Se falhar, usar dados do localStorage
            const storedUser = authService.getUserFromStorage();
            if (storedUser) {
              setUser(storedUser);
              setIsAuthenticated(true);
              logger.warning('Usando dados do localStorage para o usuário');
            } else {
              // Sem dados válidos, logout
              authService.logout();
              setIsAuthenticated(false);
              logger.warning('Nenhum dado de usuário disponível');
            }
          }
        } else {
          setIsAuthenticated(false);
          logger.debug('Nenhum token de acesso encontrado');
        }
      } catch (err) {
        logger.error('Erro ao carregar usuário', err.message);
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
      logger.info('Tentando fazer login', { email });
      const response = await authService.login(email, senha);
      setUser(response.usuario);
      setIsAuthenticated(true);
      logger.info('Login realizado com sucesso', { email: response.usuario.email });
      return response;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Erro ao fazer login';
      setError(errorMessage);
      logger.error('Erro ao fazer login', { email, error: errorMessage });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, nome, senha) => {
    setLoading(true);
    setError(null);
    try {
      logger.info('Tentando registrar novo usuário', { email, nome });
      const response = await authService.register(email, nome, senha);
      setUser(response.usuario);
      setIsAuthenticated(true);
      logger.info('Registro realizado com sucesso', { email: response.usuario.email });
      return response;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Erro ao registrar';
      setError(errorMessage);
      logger.error('Erro ao registrar', { email, error: errorMessage });
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    logger.info('Fazendo logout');
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
