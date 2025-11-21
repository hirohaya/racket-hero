/**
 * EventMatchesCard.js - Componente para exibir partidas dentro de um card
 * 
 * Exibe:
 * - Lista de partidas em um card
 * - Nomes dos jogadores, Elo atual
 * - Vencedor de cada partida
 * - Opções para editar e deletar partidas
 * - Botão para criar nova partida (apenas para organizadores)
 */

import React, { useState } from 'react';
import MatchForm from './MatchForm';
import './EventMatchesCard.css';

function EventMatchesCard({ 
  eventId, 
  matches = [], 
  players = [], 
  isOrganizer = false,
  onMatchCreated = null,
  onMatchUpdated = null,
  onMatchDeleted = null,
  isLoading = false,
  error = null
}) {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState(null);

  const handleCreateMatch = () => {
    if (players.length < 2) {
      alert('É necessário pelo menos 2 jogadores inscritos para criar uma partida.');
      return;
    }
    setSelectedMatch(null);
    setIsFormOpen(true);
  };

  const handleEditMatch = (match) => {
    setSelectedMatch(match);
    setIsFormOpen(true);
  };

  const handleFormSubmit = async (matchData) => {
    if (onMatchUpdated) {
      await onMatchUpdated(matchData);
    }
    setIsFormOpen(false);
    setSelectedMatch(null);
  };

  const handleDeleteMatch = (matchId) => {
    if (window.confirm('Tem certeza que deseja deletar esta partida?')) {
      if (onMatchDeleted) {
        onMatchDeleted(matchId);
      }
    }
  };

  return (
    <div className="matches-card">
      {/* Header do Card */}
      <div className="matches-card-header">
        <h2>🏓 Partidas ({matches.length})</h2>
        {isOrganizer && (
          <button
            className="btn-create-match"
            onClick={handleCreateMatch}
            disabled={isLoading || players.length < 2}
            title={players.length < 2 ? 'Mínimo 2 jogadores necessário' : 'Criar nova partida'}
          >
            ➕ Nova Partida
          </button>
        )}
      </div>

      {/* Conteúdo do Card */}
      <div className="matches-card-content">
        {error && (
          <div className="error-message">
            <span>⚠️ {error}</span>
          </div>
        )}

        {matches.length === 0 ? (
          <div className="empty-matches">
            <p>Nenhuma partida criada ainda.</p>
            {isOrganizer && (
              <button className="btn-primary" onClick={handleCreateMatch}>
                Criar primeira partida
              </button>
            )}
          </div>
        ) : (
          <div className="matches-list">
            {matches.map((match) => (
              <div 
                key={match.id} 
                className={`match-item ${match.winner_id ? 'played' : 'pending'}`}
              >
                <div className="match-players">
                  <div className="player-info">
                    <span className="player-name">{match.player_1_name}</span>
                    <span className="player-elo">{match.player_1_elo?.toFixed(2)}</span>
                  </div>

                  <div className="match-vs">
                    <span className="vs-text">vs</span>
                  </div>

                  <div className="player-info">
                    <span className="player-name">{match.player_2_name}</span>
                    <span className="player-elo">{match.player_2_elo?.toFixed(2)}</span>
                  </div>
                </div>

                <div className="match-result">
                  {match.winner_id ? (
                    <>
                      <span className="trophy">🏆</span>
                      <span className="winner-name">{match.winner_name}</span>
                    </>
                  ) : (
                    <span className="pending-badge">⏳ Não jogada</span>
                  )}
                </div>

                {isOrganizer && (
                  <div className="match-actions">
                    <button
                      className="btn-small btn-edit"
                      onClick={() => handleEditMatch(match)}
                      disabled={isLoading}
                      title="Editar resultado"
                    >
                      ✏️ Editar
                    </button>
                    <button
                      className="btn-small btn-delete"
                      onClick={() => handleDeleteMatch(match.id)}
                      disabled={isLoading}
                      title="Deletar partida"
                    >
                      🗑️ Deletar
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal de Formulário */}
      <MatchForm
        isOpen={isFormOpen}
        eventId={parseInt(eventId)}
        players={players}
        match={selectedMatch}
        onSubmit={handleFormSubmit}
        onCancel={() => {
          setIsFormOpen(false);
          setSelectedMatch(null);
        }}
        isLoading={isLoading}
      />
    </div>
  );
}

export default EventMatchesCard;
