/**
 * Página de Detalhes do Evento
 * Mostra informações do evento e permite inscrição
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import eventsAPI from '../services/events';
import playersAPI from '../services/players';
import rankingAPI from '../services/ranking';
import './EventDetails.css';

function EventDetails() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { eventId } = useParams();
  
  const [event, setEvent] = useState(null);
  const [players, setPlayers] = useState([]);
  const [ranking, setRanking] = useState([]);
  const [isRegistered, setIsRegistered] = useState(false);
  const [loading, setLoading] = useState(true);
  const [registering, setRegistering] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [expandedPlayersSection, setExpandedPlayersSection] = useState(true);
  const [expandedRankingSection, setExpandedRankingSection] = useState(true);

  // Carregar detalhes do evento e lista de jogadores
  useEffect(() => {
    loadEventDetails();
  }, [eventId]);

  const loadEventDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Buscar detalhes do evento
      const eventData = await eventsAPI.get(eventId);
      setEvent(eventData);
      
      // Buscar jogadores inscritos
      const playersData = await playersAPI.listEventPlayers(eventId);
      setPlayers(playersData);
      
      // Buscar ranking
      const rankingData = await rankingAPI.get(eventId);
      setRanking(rankingData);
      
      // Verificar se usuário já está registrado
      if (user && playersData.some(p => p.usuario_id === user.id)) {
        setIsRegistered(true);
      }
      
      console.log('[EventDetails] Evento carregado:', eventData);
      console.log('[EventDetails] Jogadores:', playersData);
      console.log('[EventDetails] Ranking:', rankingData);
    } catch (err) {
      console.error('[EventDetails] Erro ao carregar evento:', err);
      setError('Erro ao carregar detalhes do evento');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    try {
      setRegistering(true);
      setError(null);
      
      console.log('[EventDetails] Registrando usuário no evento...');
      const result = await playersAPI.registerToEvent(eventId);
      
      console.log('[EventDetails] Inscrição bem-sucedida:', result);
      setSuccess(result.message || 'Inscrição realizada com sucesso!');
      setIsRegistered(true);
      
      // Recarregar lista de jogadores
      await loadEventDetails();
      
      // Limpar mensagem após 3 segundos
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error('[EventDetails] Erro ao registrar:', err);
      setError(err.message || 'Erro ao realizar inscrição');
    } finally {
      setRegistering(false);
    }
  };

  const handleUnregister = async () => {
    if (!window.confirm('Tem certeza que deseja cancelar sua inscrição?')) {
      return;
    }

    try {
      setRegistering(true);
      setError(null);
      
      console.log('[EventDetails] Removendo inscrição...');
      const result = await playersAPI.unregisterFromEvent(eventId);
      
      console.log('[EventDetails] Desinscrição bem-sucedida:', result);
      setSuccess(result.message || 'Inscrição cancelada com sucesso!');
      setIsRegistered(false);
      
      // Recarregar lista de jogadores
      await loadEventDetails();
      
      // Limpar mensagem após 3 segundos
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      console.error('[EventDetails] Erro ao desinscrever:', err);
      setError(err.message || 'Erro ao cancelar inscrição');
    } finally {
      setRegistering(false);
    }
  };

  // Formatar data
  const formatDate = (dateStr) => {
    try {
      const date = new Date(dateStr + 'T00:00:00');
      return date.toLocaleDateString('pt-BR');
    } catch {
      return dateStr;
    }
  };

  // Obter ranking ordenado por pontuação (decrescente)
  const getRanking = () => {
    return ranking.length > 0 ? ranking : [...players].sort((a, b) => b.initial_elo - a.initial_elo);
  };

  if (loading) {
    return (
      <div className="event-details-container">
        <div className="loading">Carregando detalhes do evento...</div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="event-details-container">
        <div className="error-state">
          <h2>Evento não encontrado</h2>
          <button onClick={() => navigate('/eventos')} className="back-btn">
            Voltar para Eventos
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="event-details-container">
      {/* Alertas */}
      {error && (
        <div className="alert alert-error">
          <span>{error}</span>
          <button className="alert-close" onClick={() => setError(null)}>×</button>
        </div>
      )}
      {success && (
        <div className="alert alert-success">
          <span>{success}</span>
          <button className="alert-close" onClick={() => setSuccess(null)}>×</button>
        </div>
      )}

      {/* Voltar */}
      <button onClick={() => navigate('/eventos')} className="back-btn">
        ← Voltar para Eventos
      </button>

      {/* Detalhes do Evento */}
      <div className="event-card">
        <div className="event-header">
          <h1>{event.name}</h1>
          <span className={`status-badge ${event.active ? 'active' : 'inactive'}`}>
            {event.active ? '✓ Ativo' : '✗ Inativo'}
          </span>
        </div>

        <div className="event-info">
          <div className="info-item">
            <label>📅 Data</label>
            <p>{formatDate(event.date)}</p>
          </div>
          <div className="info-item">
            <label>⏰ Hora</label>
            <p>{event.time}</p>
          </div>
          <div className="info-item">
            <label>👥 Inscritos</label>
            <p>{players.length} jogador{players.length !== 1 ? 'es' : ''}</p>
          </div>
        </div>

        {/* Botão de Inscrição */}
        {user && (
          <div className="registration-section">
            {isRegistered ? (
              <div className="registered-status">
                <p className="registered-text">✓ Você está inscrito neste evento</p>
                <button
                  onClick={handleUnregister}
                  disabled={registering}
                  className="btn-unregister"
                >
                  {registering ? 'Cancelando...' : 'Cancelar Inscrição'}
                </button>
              </div>
            ) : (
              <button
                onClick={handleRegister}
                disabled={registering || !event.active}
                className="btn-register"
              >
                {registering ? 'Inscrevendo...' : '+ Inscrever-se'}
              </button>
            )}
          </div>
        )}

        {!user && (
          <div className="login-required">
            <p>Faça login para se inscrever no evento</p>
          </div>
        )}
      </div>

      {/* Lista de Jogadores Inscritos */}
      <div className="players-section">
        <div className="section-header" onClick={() => setExpandedPlayersSection(!expandedPlayersSection)}>
          <h2>👥 Jogadores Inscritos ({players.length})</h2>
          <span className={`expand-icon ${expandedPlayersSection ? 'expanded' : ''}`}>
            ▼
          </span>
        </div>

        {expandedPlayersSection && (
          <>
            {players.length === 0 ? (
              <div className="empty-players">
                <p>Nenhum jogador inscrito ainda</p>
              </div>
            ) : (
              <table className="players-table">
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Clube</th>
                    <th>Pontuação</th>
                  </tr>
                </thead>
                <tbody>
                  {players.map((player) => (
                    <tr key={player.id} className={player.usuario_id === user?.id ? 'current-user' : ''}>
                      <td>
                        <strong>{player.name}</strong>
                        {player.usuario_id === user?.id && (
                          <span className="you-badge">você</span>
                        )}
                      </td>
                      <td>{player.club || '-'}</td>
                      <td>{player.initial_elo.toFixed(1)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </>
        )}
      </div>

      {/* Ranking */}
      <div className="ranking-section">
        <div className="section-header" onClick={() => setExpandedRankingSection(!expandedRankingSection)}>
          <h2>📊 Ranking ({players.length})</h2>
          <span className={`expand-icon ${expandedRankingSection ? 'expanded' : ''}`}>
            ▼
          </span>
        </div>

        {expandedRankingSection && (
          <>
            {players.length === 0 ? (
              <div className="empty-ranking">
                <p>Nenhum jogador para ranking</p>
              </div>
            ) : (
              <table className="ranking-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Jogador</th>
                    <th>Clube</th>
                    <th>Pontuação</th>
                    <th>% Vitórias</th>
                  </tr>
                </thead>
                <tbody>
                  {getRanking().map((player, index) => (
                    <tr key={player.player_id || player.id} className={player.usuario_id === user?.id ? 'current-user' : ''}>
                      <td className="rank-position">
                        {index === 0 && '🥇'}
                        {index === 1 && '🥈'}
                        {index === 2 && '🥉'}
                        {index > 2 && `${index + 1}º`}
                      </td>
                      <td>
                        <strong>{player.name}</strong>
                        {player.usuario_id === user?.id && (
                          <span className="you-badge">você</span>
                        )}
                      </td>
                      <td>{player.club || '-'}</td>
                      <td>{(player.elo || player.initial_elo).toFixed(1)}</td>
                      <td className="win-percentage">
                        {player.win_percentage !== undefined ? `${player.win_percentage}%` : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </>
        )}
      </div>

      {/* Link para Partidas */}
      <div className="matches-link-section">
        <button
          onClick={() => navigate(`/evento/${eventId}/partidas`)}
          className="btn-matches"
        >
          🏓 Ver Partidas
        </button>
      </div>
    </div>
  );
}

export default EventDetails;
