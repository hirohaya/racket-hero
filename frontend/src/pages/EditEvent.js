/**
 * Pagina de Editar Evento
 * Formulario para editar evento existente
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import eventsAPI from '../services/events';
import './CreateEvent.css';

function EditEvent() {
  const navigate = useNavigate();
  const { eventId } = useParams();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    time: '19:00'
  });
  const [errors, setErrors] = useState({});

  // Carregar evento ao montar
  const loadEvent = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const event = await eventsAPI.get(eventId);
      setFormData({
        name: event.name,
        date: event.date,
        time: event.time
      });
      console.log('[EditEvent] Evento carregado:', event);
    } catch (err) {
      console.error('[EditEvent] Erro ao carregar evento:', err);
      setError('Erro ao carregar evento. Tente novamente.');
    } finally {
      setLoading(false);
    }
  }, [eventId]);

  useEffect(() => {
    loadEvent();
  }, [eventId, loadEvent]);

  // Validar formulario
  const validate = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Nome do evento é obrigatório';
    } else if (formData.name.trim().length < 3) {
      newErrors.name = 'Nome deve ter pelo menos 3 caracteres';
    }

    if (!formData.date) {
      newErrors.date = 'Data é obrigatória';
    }

    if (!formData.time) {
      newErrors.time = 'Hora é obrigatória';
    } else if (!/^\d{2}:\d{2}$/.test(formData.time)) {
      newErrors.time = 'Hora deve ser no formato HH:MM';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
    // Limpar erro do campo ao digitar
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: null
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    try {
      setSubmitting(true);
      setError(null);
      
      console.log('[EditEvent] Atualizando evento com dados:', formData);
      
      const result = await eventsAPI.update(eventId, {
        name: formData.name.trim(),
        date: formData.date,
        time: formData.time
      });

      console.log('[EditEvent] Evento atualizado com sucesso:', result);
      
      // Redirecionar para lista de eventos apos 1 segundo
      setTimeout(() => {
        navigate('/eventos', { 
          state: { success: `Evento "${formData.name}" atualizado com sucesso!` }
        });
      }, 1000);
    } catch (err) {
      console.error('[EditEvent] Erro ao atualizar evento:', err);
      setError(err.response?.data?.detail || 'Erro ao atualizar evento. Tente novamente.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = () => {
    navigate('/eventos');
  };

  if (loading) {
    return (
      <div className="create-event-container">
        <div className="create-event-card">
          <p>Carregando evento...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="create-event-container">
      <div className="create-event-card">
        <h1>📝 Editar Evento</h1>
        <p>Atualize os dados do evento abaixo</p>

        {error && (
          <div className="alert alert-error">
            <span>{error}</span>
            <button className="alert-close" onClick={() => setError(null)}>×</button>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Campo: Nome */}
          <div className="form-group">
            <label htmlFor="name">Nome do Evento *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Ex: Campeonato Regional de Ping-Pong"
              className={errors.name ? 'error' : ''}
              disabled={submitting}
            />
            {errors.name && <div className="error-message">{errors.name}</div>}
          </div>

          {/* Campo: Data */}
          <div className="form-group">
            <label htmlFor="date">Data do Evento *</label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              className={errors.date ? 'error' : ''}
              disabled={submitting}
            />
            {errors.date && <div className="error-message">{errors.date}</div>}
          </div>

          {/* Campo: Hora */}
          <div className="form-group">
            <label htmlFor="time">Hora do Evento *</label>
            <input
              type="time"
              id="time"
              name="time"
              value={formData.time}
              onChange={handleChange}
              className={errors.time ? 'error' : ''}
              disabled={submitting}
            />
            {errors.time && <div className="error-message">{errors.time}</div>}
          </div>

          {/* Botoes */}
          <div className="form-actions">
            <button
              type="button"
              className="cancel-btn"
              onClick={handleCancel}
              disabled={submitting}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="submit-btn"
              disabled={submitting}
            >
              {submitting && <span className="loading-spinner"></span>}
              {submitting ? 'Salvando...' : 'Salvar Alteracoes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default EditEvent;
