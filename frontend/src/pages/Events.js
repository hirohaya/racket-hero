/**
 * Pagina de Eventos
 * Lista todos os eventos e permite criar novos
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import eventsAPI from '../services/events';
import './Events.css';

function Events() {
  const navigate = useNavigate();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [deleteConfirmation, setDeleteConfirmation] = useState(null);

  // Carregar eventos ao montar componente
  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await eventsAPI.list();
      setEvents(data);
      console.log('[Events] Eventos carregados:', data);
    } catch (err) {
      console.error('[Events] Erro ao carregar eventos:', err);
      setError('Erro ao carregar eventos. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleNewEvent = () => {
    navigate('/novo-evento');
  };

  const handleEdit = (eventId) => {
    navigate(`/editar-evento/${eventId}`);
  };

  const handleDeleteClick = (event) => {
    setDeleteConfirmation(event);
  };

  const handleConfirmDelete = async () => {
    if (!deleteConfirmation) return;

    try {
      await eventsAPI.delete(deleteConfirmation.id);
      setSuccess(`Evento "${deleteConfirmation.name}" deletado com sucesso!`);
      setDeleteConfirmation(null);
      loadEvents(); // Recarregar lista
      
      // Limpar mensagem de sucesso apos 3 segundos
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error('[Events] Erro ao deletar evento:', err);
      setError('Erro ao deletar evento. Tente novamente.');
      setDeleteConfirmation(null);
    }
  };

  const handleCancelDelete = () => {
    setDeleteConfirmation(null);
  };

  const closeAlert = () => {
    setError(null);
    setSuccess(null);
  };

  // Formatar data para exibicao
  const formatDate = (dateStr) => {
    try {
      const date = new Date(dateStr + 'T00:00:00');
      return date.toLocaleDateString('pt-BR');
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="events-container">
      {/* Alertas */}
      {error && (
        <div className="alert alert-error">
          <span>{error}</span>
          <button className="alert-close" onClick={closeAlert}>×</button>
        </div>
      )}
      {success && (
        <div className="alert alert-success">
          <span>{success}</span>
          <button className="alert-close" onClick={closeAlert}>×</button>
        </div>
      )}

      {/* Header */}
      <div className="events-header">
        <h1>📋 Eventos</h1>
        <button className="new-event-btn" onClick={handleNewEvent}>
          + Novo Evento
        </button>
      </div>

      {/* Loading state */}
      {loading && <div className="loading">Carregando eventos...</div>}

      {/* Empty state */}
      {!loading && events.length === 0 && (
        <div className="empty-state">
          <h2>Nenhum evento criado ainda</h2>
          <p>Clique em "Novo Evento" para comectar!</p>
          <button className="new-event-btn" onClick={handleNewEvent}>
            + Criar Primeiro Evento
          </button>
        </div>
      )}

      {/* Tabela de eventos */}
      {!loading && events.length > 0 && (
        <table className="events-table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Data</th>
              <th>Hora</th>
              <th>Status</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id}>
                <td><strong>{event.name}</strong></td>
                <td className="event-date">{formatDate(event.date)}</td>
                <td className="event-date">{event.time}</td>
                <td>
                  <span className={`event-status ${event.active ? 'status-active' : 'status-inactive'}`}>
                    {event.active ? 'Ativo' : 'Inativo'}
                  </span>
                </td>
                <td>
                  <div className="event-actions">
                    <button 
                      className="edit-btn"
                      onClick={() => handleEdit(event.id)}
                      title="Editar evento"
                    >
                      Editar
                    </button>
                    <button 
                      className="delete-btn"
                      onClick={() => handleDeleteClick(event)}
                      title="Deletar evento"
                    >
                      Deletar
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Modal de confirmacao de delecao */}
      {deleteConfirmation && (
        <div className="confirmation-modal">
          <div className="confirmation-content">
            <h2>Deletar Evento?</h2>
            <p>
              Tem certeza que deseja deletar o evento "{deleteConfirmation.name}"?
              Esta acão nao pode ser desfeita.
            </p>
            <div className="confirmation-actions">
              <button className="cancel-btn" onClick={handleCancelDelete}>
                Cancelar
              </button>
              <button className="confirm-btn" onClick={handleConfirmDelete}>
                Deletar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Events;
