/**
 * Serviço de API para Jogadores/Players
 * Faz requisições para os endpoints /players do backend
 */

import api from './api';

const playersAPI = {
  /**
   * Registrar usuário autenticado em um evento
   * @param {number} eventId - ID do evento
   */
  async registerToEvent(eventId) {
    try {
      const response = await api.post(`/players/eventos/${eventId}/inscricao`);
      console.log('[PlayersAPI] Registrado com sucesso:', response.data);
      return response.data;
    } catch (error) {
      console.error('[PlayersAPI] Erro ao registrar:', error);
      throw error;
    }
  },

  /**
   * Remover inscrição de um evento
   * @param {number} eventId - ID do evento
   */
  async unregisterFromEvent(eventId) {
    try {
      const response = await api.delete(`/players/eventos/${eventId}/inscricao`);
      console.log('[PlayersAPI] Desinscrição realizada:', response.data);
      return response.data;
    } catch (error) {
      console.error('[PlayersAPI] Erro ao desinscrever:', error);
      throw error;
    }
  },

  /**
   * Listar jogadores inscritos em um evento
   * @param {number} eventId - ID do evento
   */
  async listEventPlayers(eventId) {
    try {
      const response = await api.get(`/players/eventos/${eventId}/inscritos`);
      console.log('[PlayersAPI] Jogadores carregados:', response.data);
      return response.data;
    } catch (error) {
      console.error('[PlayersAPI] Erro ao listar jogadores:', error);
      throw error;
    }
  },

  /**
   * Criar novo jogador (sem autenticação - uso interno)
   */
  async create(playerData) {
    try {
      const response = await api.post('/players', playerData);
      console.log('[PlayersAPI] Jogador criado:', response.data);
      return response.data;
    } catch (error) {
      console.error('[PlayersAPI] Erro ao criar jogador:', error);
      throw error;
    }
  },

  /**
   * Listar jogadores de um evento
   */
  async list(eventId) {
    try {
      const response = await api.get(`/players/${eventId}`);
      console.log('[PlayersAPI] Jogadores listados:', response.data);
      return response.data;
    } catch (error) {
      console.error('[PlayersAPI] Erro ao listar jogadores:', error);
      throw error;
    }
  },

  /**
   * Obter jogador por ID
   */
  async get(playerId) {
    try {
      const response = await api.get(`/players/player/${playerId}`);
      return response.data;
    } catch (error) {
      console.error('[PlayersAPI] Erro ao obter jogador:', error);
      throw error;
    }
  },

  /**
   * Adicionar jogador a um evento (apenas para organizadores)
   * @param {number} eventId - ID do evento
   * @param {object} playerData - Dados do jogador { name, club, initial_elo }
   */
  async addToEvent(eventId, playerData) {
    try {
      const response = await api.post(`/players/eventos/${eventId}/add`, playerData);
      console.log('[PlayersAPI] Jogador adicionado:', response.data);
      return response.data;
    } catch (error) {
      console.error('[PlayersAPI] Erro ao adicionar jogador:', error);
      throw error;
    }
  },

  /**
   * Remover jogador de um evento (apenas para organizadores)
   * @param {number} playerId - ID do jogador
   */
  async removeFromEvent(playerId) {
    try {
      const response = await api.delete(`/players/${playerId}`);
      console.log('[PlayersAPI] Jogador removido:', response.data);
      return response.data;
    } catch (error) {
      console.error('[PlayersAPI] Erro ao remover jogador:', error);
      throw error;
    }
  }
};

export default playersAPI;
