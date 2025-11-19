/**
 * matches.js - API Service para Partidas (Matches)
 * 
 * Gerencia todas as operações de CRUD para partidas:
 * - Criar nova partida
 * - Listar partidas de um evento
 * - Atualizar resultado de partida
 * - Deletar partida
 */

import api from './api';

class MatchesAPI {
  /**
   * Criar uma nova partida
   * @param {number} eventId - ID do evento
   * @param {number} player1Id - ID do jogador 1
   * @param {number} player2Id - ID do jogador 2
   * @param {number} winnerId - ID do vencedor
   * @returns {Promise} Dados da partida criada
   */
  async createMatch(eventId, player1Id, player2Id, winnerId) {
    try {
      console.log('[MatchesAPI] Criando partida:', {
        eventId,
        player1Id,
        player2Id,
        winnerId
      });

      const response = await api.post('/matches', {
        event_id: eventId,
        player_1_id: player1Id,
        player_2_id: player2Id,
        winner_id: winnerId
      });

      console.log('[MatchesAPI] Partida criada:', response.data);
      return response.data;
    } catch (error) {
      console.error('[MatchesAPI] Erro ao criar partida:', error.message);
      throw error;
    }
  }

  /**
   * Listar partidas de um evento
   * @param {number} eventId - ID do evento
   * @returns {Promise<Array>} Lista de partidas
   */
  async getMatches(eventId) {
    try {
      console.log('[MatchesAPI] Carregando partidas para evento:', eventId);

      const response = await api.get(`/matches/${eventId}`);

      console.log('[MatchesAPI] Partidas carregadas:', response.data);
      return Array.isArray(response.data) ? response.data : [];
    } catch (error) {
      console.error('[MatchesAPI] Erro ao carregar partidas:', error.message);
      throw error;
    }
  }

  /**
   * Atualizar resultado de uma partida
   * @param {number} matchId - ID da partida
   * @param {number} winnerId - Novo ID do vencedor
   * @returns {Promise} Dados da partida atualizada
   */
  async updateMatch(matchId, winnerId) {
    try {
      console.log('[MatchesAPI] Atualizando partida:', matchId, 'Novo vencedor:', winnerId);

      const response = await api.put(`/matches/${matchId}`, {
        winner_id: winnerId
      });

      console.log('[MatchesAPI] Partida atualizada:', response.data);
      return response.data;
    } catch (error) {
      console.error('[MatchesAPI] Erro ao atualizar partida:', error.message);
      throw error;
    }
  }

  /**
   * Deletar uma partida
   * @param {number} matchId - ID da partida
   * @returns {Promise} Resposta do servidor
   */
  async deleteMatch(matchId) {
    try {
      console.log('[MatchesAPI] Deletando partida:', matchId);

      const response = await api.delete(`/matches/${matchId}`);

      console.log('[MatchesAPI] Partida deletada:', response.data);
      return response.data;
    } catch (error) {
      console.error('[MatchesAPI] Erro ao deletar partida:', error.message);
      throw error;
    }
  }
}

// Exportar instância singleton
export default new MatchesAPI();
