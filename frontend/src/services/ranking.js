/**
 * Serviço de API para Ranking
 * Faz requisições para os endpoints /ranking do backend
 */

import api from './api';

const rankingAPI = {
  /**
   * Obter ranking de um evento
   * @param {number} eventId - ID do evento
   */
  async get(eventId) {
    try {
      const response = await api.get(`/ranking/${eventId}`);
      console.log('[RankingAPI] Ranking carregado:', response.data);
      return response.data;
    } catch (error) {
      console.error('[RankingAPI] Erro ao obter ranking:', error);
      throw error;
    }
  }
};

export default rankingAPI;
