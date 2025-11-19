/**
 * Servico de API para Eventos
 * Faz requisicoes para os endpoints /events do backend
 */

import api from './api';

const eventsAPI = {
  /**
   * Listar todos os eventos ativos
   */
  async list() {
    try {
      const response = await api.get('/events');
      return response.data;
    } catch (error) {
      console.error('[EventsAPI] Erro ao listar eventos:', error);
      throw error;
    }
  },

  /**
   * Listar apenas os eventos nos quais o usuario esta registrado (jogadores)
   * Para organizadores e admins, retorna todos os eventos
   */
  async listMyEvents() {
    try {
      const response = await api.get('/events/meus-eventos');
      return response.data;
    } catch (error) {
      console.error('[EventsAPI] Erro ao listar meus eventos:', error);
      throw error;
    }
  },

  /**
   * Obter um evento por ID
   */
  async get(eventId) {
    try {
      const response = await api.get(`/events/${eventId}`);
      return response.data;
    } catch (error) {
      console.error(`[EventsAPI] Erro ao obter evento ${eventId}:`, error);
      throw error;
    }
  },

  /**
   * Criar novo evento
   * @param {Object} event - Dados do evento {name, date, time}
   */
  async create(event) {
    try {
      const response = await api.post('/events', event);
      console.log('[EventsAPI] Evento criado com sucesso:', response.data);
      return response.data;
    } catch (error) {
      console.error('[EventsAPI] Erro ao criar evento:', error);
      throw error;
    }
  },

  /**
   * Atualizar evento (ainda nao implementado no backend)
   */
  async update(eventId, event) {
    try {
      const response = await api.put(`/events/${eventId}`, event);
      console.log('[EventsAPI] Evento atualizado:', response.data);
      return response.data;
    } catch (error) {
      console.error(`[EventsAPI] Erro ao atualizar evento ${eventId}:`, error);
      throw error;
    }
  },

  /**
   * Deletar evento - soft delete
   */
  async delete(eventId) {
    try {
      const response = await api.delete(`/events/${eventId}`);
      console.log('[EventsAPI] Evento deletado:', eventId);
      return response.data;
    } catch (error) {
      console.error(`[EventsAPI] Erro ao deletar evento ${eventId}:`, error);
      throw error;
    }
  }
};

export default eventsAPI;
