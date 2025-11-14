import axios from 'axios';
import logger from './logger';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

logger.info('API inicializada', { baseURL: API_BASE_URL });

// Adicionar token ao header de cada requisição
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      logger.debug('Token adicionado ao header');
    }
    logger.debug('Requisição enviada', { method: config.method, url: config.url });
    return config;
  },
  (error) => {
    logger.error('Erro na requisição', error.message);
    return Promise.reject(error);
  }
);

// Interceptor para renovar token se expirado
api.interceptors.response.use(
  (response) => {
    logger.debug('Resposta recebida', { status: response.status, url: response.config.url });
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Se houver erro 401 e não for uma tentativa de refresh já feita
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      logger.warning('Token expirado, tentando renovar...');

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('Sem refresh token');
        }

        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token } = response.data;
        localStorage.setItem('accessToken', access_token);
        localStorage.setItem('refreshToken', refresh_token);
        logger.info('Token renovado com sucesso');

        // Tentar a requisição original novamente
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Se refresh falhar, limpar tokens e redirecionar para login
        logger.error('Falha ao renovar token', refreshError.message);
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    logger.error('Erro na resposta', { 
      status: error.response?.status, 
      message: error.message 
    });
    return Promise.reject(error);
  }
);

export default api;
