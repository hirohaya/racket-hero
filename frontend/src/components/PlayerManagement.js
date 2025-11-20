/**
 * PlayerManagement.js - Modal para gerenciar jogadores do evento
 * Permite adicionar e remover jogadores (apenas para organizadores)
 */

import React, { useState } from 'react';
import playersAPI from '../services/players';
import '../styles/PlayerManagement.css';

function PlayerManagement({ eventId, isOpen, onClose, onPlayersUpdated, isOrganizer }) {
  const [newPlayerName, setNewPlayerName] = useState('');
  const [newPlayerClub, setNewPlayerClub] = useState('');
  const [newPlayerElo, setNewPlayerElo] = useState('1600');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleAddPlayer = async (e) => {
    e.preventDefault();
    
    if (!newPlayerName.trim()) {
      setError('Nome do jogador é obrigatório');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const playerData = {
        name: newPlayerName.trim(),
        club: newPlayerClub.trim() || null,
        initial_elo: parseFloat(newPlayerElo) || 1600
      };

      console.log('[PlayerManagement] Adicionando jogador:', playerData);
      
      const response = await playersAPI.addToEvent(eventId, playerData);
      
      setSuccess(response.message || `Jogador '${newPlayerName}' adicionado com sucesso!`);
      setNewPlayerName('');
      setNewPlayerClub('');
      setNewPlayerElo('1600');
      
      // Recarregar lista de jogadores
      setTimeout(() => {
        onPlayersUpdated();
        setSuccess(null);
      }, 1500);
    } catch (err) {
      console.error('[PlayerManagement] Erro ao adicionar jogador:', err);
      setError(err.response?.data?.detail || err.message || 'Erro ao adicionar jogador');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>➕ Adicionar Jogador</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        {error && (
          <div className="modal-alert alert-error">
            {error}
            <button className="alert-close" onClick={() => setError(null)}>×</button>
          </div>
        )}
        
        {success && (
          <div className="modal-alert alert-success">
            {success}
            <button className="alert-close" onClick={() => setSuccess(null)}>×</button>
          </div>
        )}

        <form onSubmit={handleAddPlayer} className="player-form">
          <div className="form-group">
            <label htmlFor="playerName">Nome do Jogador *</label>
            <input
              id="playerName"
              type="text"
              value={newPlayerName}
              onChange={(e) => setNewPlayerName(e.target.value)}
              placeholder="Ex: João Silva"
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="playerClub">Clube</label>
            <input
              id="playerClub"
              type="text"
              value={newPlayerClub}
              onChange={(e) => setNewPlayerClub(e.target.value)}
              placeholder="Ex: Clube do Tenis"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="playerElo">Pontuação Inicial</label>
            <input
              id="playerElo"
              type="number"
              value={newPlayerElo}
              onChange={(e) => setNewPlayerElo(e.target.value)}
              placeholder="1600"
              min="0"
              max="3000"
              disabled={loading}
            />
            <small>Padrão: 1600</small>
          </div>

          <div className="modal-actions">
            <button
              type="button"
              className="btn-cancel"
              onClick={onClose}
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn-submit"
              disabled={loading}
            >
              {loading ? 'Adicionando...' : 'Adicionar Jogador'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default PlayerManagement;
