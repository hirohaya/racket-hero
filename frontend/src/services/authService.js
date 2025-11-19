import api from './api';

const authService = {
  // Registrar novo usuário
  register: async (email, nome, senha) => {
    const response = await api.post('/auth/register', {
      email,
      nome,
      senha,
    });
    
    // Salvar tokens no localStorage
    const { access_token, refresh_token, usuario } = response.data;
    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
    localStorage.setItem('user', JSON.stringify(usuario));
    
    return response.data;
  },

  // Fazer login
  login: async (email, senha) => {
    const response = await api.post('/auth/login', {
      email,
      senha,
    });
    
    // Salvar tokens no localStorage
    const { access_token, refresh_token, usuario } = response.data;
    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
    localStorage.setItem('user', JSON.stringify(usuario));
    
    return response.data;
  },

  // Obter dados do usuário autenticado
  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      // Se não conseguir obter, tentar usar dados do localStorage
      const user = localStorage.getItem('user');
      if (user) {
        return JSON.parse(user);
      }
      throw error;
    }
  },

  // Solicitar recuperação de senha
  forgotPassword: async (email) => {
    const response = await api.post('/auth/forgot-password', {
      email,
    });
    return response.data;
  },

  // Redefinir senha
  resetPassword: async (token, novaSenha) => {
    const response = await api.post('/auth/reset-password', {
      token,
      nova_senha: novaSenha,
    });
    
    // Salvar novos tokens
    const { access_token, refresh_token, usuario } = response.data;
    localStorage.setItem('accessToken', access_token);
    localStorage.setItem('refreshToken', refresh_token);
    localStorage.setItem('user', JSON.stringify(usuario));
    
    return response.data;
  },

  // Logout
  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  },

  // Verificar se está autenticado
  isAuthenticated: () => {
    return !!localStorage.getItem('accessToken');
  },

  // Obter token de acesso
  getAccessToken: () => {
    return localStorage.getItem('accessToken');
  },

  // Obter dados do usuário do localStorage
  getUserFromStorage: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};

export default authService;
