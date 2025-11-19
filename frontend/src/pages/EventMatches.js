/**
 * EventMatches.js - Página de Partidas de um Evento
 * 
 * Exibe:
 * - Lista de todas as partidas do evento
 * - Nomes dos jogadores, Elo atual
 * - Vencedor de cada partida
 * - Opções para editar e deletar partidas
 * - Botão para criar nova partida
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import MatchForm from '../components/MatchForm';
import EventsAPI from '../services/events';
import PlayersAPI from '../services/players';
import MatchesAPI from '../services/matches';
import '../styles/EventMatches.css';

function EventMatches() {
  const { eventId } = useParams();
  const navigate = useNavigate();

  // Estado
  const [event, setEvent] = useState(null);
  const [players, setPlayers] = useState([]);
  const [matches, setMatches] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Carregar dados iniciais
  useEffect(() => {
    loadEventData();
  }, [eventId]);

  const loadEventData = async () => {
    try {
      setError(null);
      setIsLoading(true);

      // Carregar evento
      const eventData = await EventsAPI.get(eventId);
      setEvent(eventData);

      // Carregar jogadores
      const playersData = await PlayersAPI.listEventPlayers(eventId);
      setPlayers(playersData);

      // Carregar partidas
      const matchesData = await MatchesAPI.getMatches(eventId);
      setMatches(matchesData);
    } catch (err) {
      console.error('[EventMatches] Erro ao carregar dados:', err);
      setError('Erro ao carregar dados do evento. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateMatch = () => {
    if (players.length < 2) {
      setError('É necessário pelo menos 2 jogadores inscritos para criar uma partida.');
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
    try {
      setIsLoading(true);
      setError(null);

      if (selectedMatch) {
        // Atualizar partida existente
        await MatchesAPI.updateMatch(selectedMatch.id, matchData.winner_id);
      } else {
        // Criar nova partida
        await MatchesAPI.createMatch(
          matchData.event_id,
          matchData.player_1_id,
          matchData.player_2_id,
          matchData.winner_id
        );
      }

      setIsFormOpen(false);
      setSelectedMatch(null);
      await loadEventData(); // Recarregar dados
    } catch (err) {
      console.error('[EventMatches] Erro ao salvar partida:', err);
      setError(err.response?.data?.detail || 'Erro ao salvar partida. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteMatch = async (matchId) => {
    if (!window.confirm('Tem certeza que deseja deletar esta partida?')) {
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      await MatchesAPI.deleteMatch(matchId);
      await loadEventData(); // Recarregar dados
    } catch (err) {
      console.error('[EventMatches] Erro ao deletar partida:', err);
      setError('Erro ao deletar partida. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && !event) {
    return <div className="loading">⏳ Carregando...</div>;
  }

  return (
    <div className="event-matches-container">
      {/* Header */}
      <div className="event-matches-header">
        <button className="back-btn" onClick={() => navigate(`/evento/${eventId}`)}>
          ← Voltar
        </button>

        <div className="event-info">
          <h1>🎯 {event?.name || 'Partidas'}</h1>
          <p className="event-meta">
            📅 {event?.date} - ⏰ {event?.time}
          </p>
        </div>

        <button
          className="btn-primary btn-lg"
          onClick={handleCreateMatch}
          disabled={isLoading || players.length < 2}
        >
          ➕ Nova Partida
        </button>
      </div>

      {/* Erro */}
      {error && (
        <div className="error-alert">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {/* Seção de Partidas */}
      <div className="matches-section">
        <h2>🏓 Partidas ({matches.length})</h2>

        {matches.length === 0 ? (
          <div className="empty-state">
            <p>Nenhuma partida criada ainda.</p>
            <button className="btn-primary" onClick={handleCreateMatch}>
              Criar primeira partida
            </button>
          </div>
        ) : (
          <div className="matches-table-container">
            <table className="matches-table">
              <thead>
                <tr>
                  <th>Jogador 1</th>
                  <th>Elo 1</th>
                  <th>vs</th>
                  <th>Jogador 2</th>
                  <th>Elo 2</th>
                  <th>Vencedor</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {matches.map((match) => (
                  <tr key={match.id} className={`match-row ${match.winner_id ? 'played' : 'pending'}`}>
                    <td className="player-name">
                      <strong>{match.player_1_name}</strong>
                    </td>
                    <td className="player-elo">
                      {match.player_1_elo?.toFixed(2)}
                    </td>
                    <td className="vs">vs</td>
                    <td className="player-name">
                      <strong>{match.player_2_name}</strong>
                    </td>
                    <td className="player-elo">
                      {match.player_2_elo?.toFixed(2)}
                    </td>
                    <td className="winner">
                      {match.winner_id ? (
                        <>
                          <span className="trophy">🏆</span>
                          {match.winner_name}
                        </>
                      ) : (
                        <span className="pending-badge">⏳ Não jogada</span>
                      )}
                    </td>
                    <td className="actions">
                      <button
                        className="btn-small btn-edit"
                        onClick={() => handleEditMatch(match)}
                        disabled={isLoading}
                        title="Editar resultado"
                      >
                        ✏️
                      </button>
                      <button
                        className="btn-small btn-delete"
                        onClick={() => handleDeleteMatch(match.id)}
                        disabled={isLoading}
                        title="Deletar partida"
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
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

export default EventMatches;
