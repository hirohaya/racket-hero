/**
 * Pagina de Criar Evento
 * Formulario para criar novo evento
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import eventsAPI from '../services/events';
import './CreateEvent.css';

function CreateEvent() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    time: '19:00'
  });
  const [errors, setErrors] = useState({});

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
    } else {
      // Validar se data e valida
      const selectedDate = new Date(formData.date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      if (selectedDate < today) {
        newErrors.date = 'Data nao pode ser no passado';
      }
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
      setLoading(true);
      setError(null);
      
      console.log('[CreateEvent] Criando evento com dados:', formData);
      
      const result = await eventsAPI.create({
        name: formData.name.trim(),
        date: formData.date,
        time: formData.time
      });

      console.log('[CreateEvent] Evento criado com sucesso:', result);
      
      // Redirecionar para lista de eventos apos 1 segundo
      setTimeout(() => {
        navigate('/eventos', { 
          state: { success: `Evento "${formData.name}" criado com sucesso!` }
        });
      }, 1000);
    } catch (err) {
      console.error('[CreateEvent] Erro ao criar evento:', err);
      setError(err.response?.data?.detail || 'Erro ao criar evento. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/eventos');
  };

  // Obter data minima (hoje)
  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="create-event-container">
      <div className="create-event-card">
        <h1>📅 Novo Evento</h1>
        <p>Preencha os dados do evento abaixo</p>

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
              disabled={loading}
            />
            {errors.name && <div className="error-message">{errors.name}</div>}
            <div className="form-helper">
              Minimo de 3 caracteres
            </div>
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
              min={today}
              className={errors.date ? 'error' : ''}
              disabled={loading}
            />
            {errors.date && <div className="error-message">{errors.date}</div>}
            <div className="form-helper">
              Formato: DD/MM/YYYY (nao pode ser no passado)
            </div>
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
              disabled={loading}
            />
            {errors.time && <div className="error-message">{errors.time}</div>}
            <div className="form-helper">
              Formato: HH:MM (ex: 19:00 para 7 da noite)
            </div>
          </div>

          {/* Botoes */}
          <div className="form-actions">
            <button
              type="button"
              className="cancel-btn"
              onClick={handleCancel}
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="submit-btn"
              disabled={loading}
            >
              {loading && <span className="loading-spinner"></span>}
              {loading ? 'Criando...' : 'Criar Evento'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateEvent;
