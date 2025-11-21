/**
 * PlayerManagement.js - Modal para gerenciar jogadores do evento
 * Permite adicionar e remover jogadores (apenas para organizadores)
 * Inclui busca dinâmica de jogadores cadastrados
 */

import React, { useState, useEffect } from 'react';
import playersAPI from '../services/players';
import PlayerSearchForm from './PlayerSearchForm';
import '../styles/PlayerManagement.css';

function PlayerManagement({ eventId, isOpen, onClose, onPlayersUpdated, isOrganizer }) {
  const [newPlayerName, setNewPlayerName] = useState('');
  const [newPlayerClub, setNewPlayerClub] = useState('');
  const [newPlayerElo, setNewPlayerElo] = useState('1600');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showSearchMode, setShowSearchMode] = useState(true);
  const [eventPlayers, setEventPlayers] = useState([]);
  const [playerIds, setPlayerIds] = useState([]);

  // Carregar jogadores do evento ao abrir o modal
  useEffect(() => {
    if (isOpen) {
      loadEventPlayers();
    }
  }, [isOpen, eventId]);

  const loadEventPlayers = async () => {
    try {
      const players = await playersAPI.listEventPlayers(eventId);
      setEventPlayers(players);
      // Usar usuario_id para excluir da busca (identificador único do usuário)
      setPlayerIds(players.map(p => p.usuario_id).filter(id => id !== null));
    } catch (err) {
      console.error('[PlayerManagement] Erro ao carregar jogadores:', err);
    }
  };

  const handleSelectFromSearch = async (user) => {
    // Auto-preencher o formulário com o jogador selecionado
    setNewPlayerName(user.name);
    setNewPlayerClub(''); // Limpar clube (pode ser preenchido depois)
    setNewPlayerElo('1600'); // Usar Elo padrão
    setShowSearchMode(false); // Mostrar o resto do formulário
    setError(null);
  };

  const handleAddNewManually = () => {
    // Mudar para modo de entrada manual
    setShowSearchMode(false);
    setNewPlayerName('');
    setNewPlayerClub('');
    setNewPlayerElo('1600');
    setError(null);
  };

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
      
      // Fechar modal e atualizar lista (sem delay, atualização parcial)
      onPlayersUpdated();
      
      // Limpar modal após atualização ser processada
      setTimeout(() => {
        setSuccess(null);
        setShowSearchMode(true);
        onClose(); // Fechar modal após sucesso
      }, 1500);
    } catch (err) {
      console.error('[PlayerManagement] Erro ao adicionar jogador:', err);
      
      // Extrair mensagem de erro de forma segura
      let errorMessage = 'Erro ao adicionar jogador';
      if (err.response?.data?.detail) {
        // Se é string, usar diretamente
        if (typeof err.response.data.detail === 'string') {
          errorMessage = err.response.data.detail;
        } 
        // Se é array de objetos (validation errors), extrair primeira mensagem
        else if (Array.isArray(err.response.data.detail)) {
          errorMessage = err.response.data.detail[0]?.msg || 'Erro ao adicionar jogador';
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
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
          {loading && <div className="modal-loading-indicator"></div>}
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

        {/* Modo Busca */}
        {showSearchMode && (
          <div className="search-mode">
            <p className="search-mode-title">🔍 Procure um jogador registrado:</p>
            <PlayerSearchForm 
              onSelectPlayer={handleSelectFromSearch}
              onAddNew={handleAddNewManually}
              excludePlayerIds={playerIds}
              isOrganizer={isOrganizer}
            />
          </div>
        )}

        {/* Modo Formulário */}
        {!showSearchMode && (
          <form onSubmit={handleAddPlayer} className="player-form">
            <button 
              type="button"
              className="btn-back-to-search"
              onClick={() => {
                setShowSearchMode(true);
                setNewPlayerName('');
                setNewPlayerClub('');
                setNewPlayerElo('1600');
                setError(null);
              }}
              disabled={loading}
            >
              ← Voltar para busca
            </button>

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
        )}
      </div>
    </div>
  );
}

export default PlayerManagement;
