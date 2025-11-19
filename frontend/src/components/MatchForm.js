/**
 * MatchForm.js - Formulário para Criar/Editar Partidas
 * 
 * Componente modal/formulário para:
 * - Criar nova partida entre dois jogadores
 * - Selecionar vencedor
 * - Editar resultado de partida existente
 * - Validação de dados
 */

import React, { useState, useEffect } from 'react';
import '../styles/MatchForm.css';

function MatchForm({
  isOpen,
  eventId,
  players = [],
  match = null,
  onSubmit,
  onCancel,
  isLoading = false
}) {
  const [formData, setFormData] = useState({
    player1Id: '',
    player2Id: '',
    winnerId: ''
  });

  const [errors, setErrors] = useState({});

  // Preencher formulário se estiver editando uma partida
  useEffect(() => {
    if (match) {
      setFormData({
        player1Id: match.player_1_id ? String(match.player_1_id) : '',
        player2Id: match.player_2_id ? String(match.player_2_id) : '',
        winnerId: match.winner_id ? String(match.winner_id) : ''
      });
    } else {
      setFormData({
        player1Id: '',
        player2Id: '',
        winnerId: ''
      });
    }
    setErrors({});
  }, [match, isOpen]);

  const validateForm = () => {
    const newErrors = {};

    if (!formData.player1Id) {
      newErrors.player1Id = 'Selecione o Jogador 1';
    }

    if (!formData.player2Id) {
      newErrors.player2Id = 'Selecione o Jogador 2';
    }

    if (formData.player1Id && formData.player2Id && formData.player1Id === formData.player2Id) {
      newErrors.player2Id = 'Jogadores devem ser diferentes';
    }

    // Winner_id é OPCIONAL - não validar se é obrigatório
    if (
      formData.winnerId &&
      formData.winnerId !== formData.player1Id &&
      formData.winnerId !== formData.player2Id
    ) {
      newErrors.winnerId = 'O vencedor deve ser um dos jogadores';
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
    // Limpar erro ao mudar o campo
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const matchData = {
      event_id: eventId,
      player_1_id: parseInt(formData.player1Id),
      player_2_id: parseInt(formData.player2Id),
      winner_id: formData.winnerId ? parseInt(formData.winnerId) : null
    };

    onSubmit(matchData);
  };

  if (!isOpen) {
    return null;
  }

  const getPlayerName = (id) => {
    const player = players.find((p) => p.id === parseInt(id));
    return player ? player.name : '';
  };

  // Filtrar Player 2 para não poder ser igual a Player 1
  const availablePlayers2 = players.filter((p) => p.id !== parseInt(formData.player1Id));

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{match ? '✏️ Editar Partida' : '🎯 Nova Partida'}</h2>
          <button className="close-btn" onClick={onCancel}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="match-form">
          {/* Jogador 1 */}
          <div className="form-group">
            <label htmlFor="player1Id">Jogador 1 (Branco)</label>
            <select
              id="player1Id"
              name="player1Id"
              value={formData.player1Id}
              onChange={handleChange}
              disabled={match !== null} // Desabilitar ao editar
              className={errors.player1Id ? 'input-error' : ''}
            >
              <option value="">Selecione um jogador</option>
              {players.map((player) => (
                <option key={player.id} value={String(player.id)}>
                  {player.name} (Elo: {player.initial_elo?.toFixed(2) || '1600'})
                </option>
              ))}
            </select>
            {errors.player1Id && <span className="error-message">{errors.player1Id}</span>}
          </div>

          {/* Jogador 2 */}
          <div className="form-group">
            <label htmlFor="player2Id">Jogador 2 (Preto)</label>
            <select
              id="player2Id"
              name="player2Id"
              value={formData.player2Id}
              onChange={handleChange}
              disabled={match !== null} // Desabilitar ao editar
              className={errors.player2Id ? 'input-error' : ''}
            >
              <option value="">Selecione um jogador</option>
              {availablePlayers2.map((player) => (
                <option key={player.id} value={String(player.id)}>
                  {player.name} (Elo: {player.initial_elo?.toFixed(2) || '1600'})
                </option>
              ))}
            </select>
            {errors.player2Id && <span className="error-message">{errors.player2Id}</span>}
          </div>

          {/* Vencedor */}
          <div className="form-group">
            <label htmlFor="winnerId">Vencedor (Opcional)</label>
            <select
              id="winnerId"
              name="winnerId"
              value={formData.winnerId}
              onChange={handleChange}
              className={errors.winnerId ? 'input-error' : ''}
            >
              <option value="">Selecione o vencedor</option>
              {formData.player1Id && (
                <option value={formData.player1Id}>
                  {getPlayerName(formData.player1Id)} (Jogador 1)
                </option>
              )}
              {formData.player2Id && (
                <option value={formData.player2Id}>
                  {getPlayerName(formData.player2Id)} (Jogador 2)
                </option>
              )}
            </select>
            {errors.winnerId && <span className="error-message">{errors.winnerId}</span>}
          </div>

          {/* Resumo da partida */}
          {formData.player1Id && formData.player2Id && (
            <div className="match-summary">
              <h4>📊 Resumo da Partida</h4>
              <p>
                <strong>{getPlayerName(formData.player1Id)}</strong> vs <strong>{getPlayerName(formData.player2Id)}</strong>
              </p>
              {formData.winnerId && (
                <p className="winner-info">
                  🏆 Vencedor: <strong>{getPlayerName(formData.winnerId)}</strong>
                </p>
              )}
            </div>
          )}

          {/* Botões */}
          <div className="modal-footer">
            <button
              type="button"
              onClick={onCancel}
              className="btn-secondary"
              disabled={isLoading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn-primary"
              disabled={isLoading}
            >
              {isLoading ? '⏳ Salvando...' : match ? '💾 Atualizar' : '➕ Criar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default MatchForm;
