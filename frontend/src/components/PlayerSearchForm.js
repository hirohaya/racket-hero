/**
 * PlayerSearchForm.js - Componente para buscar e selecionar jogadores cadastrados
 * Permite filtro dinâmico pelo nome com lista atualizada em tempo real
 */

import React, { useState, useEffect, useRef } from 'react';
import playersAPI from '../services/players';
import '../styles/PlayerSearchForm.css';

function PlayerSearchForm({ 
  onSelectPlayer, 
  onAddNew, 
  excludePlayerIds = [],
  isOrganizer 
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [error, setError] = useState(null);
  const searchTimeoutRef = useRef(null);

  // Buscar usuários quando o termo de busca mudar
  useEffect(() => {
    // Cancelar busca anterior se existir
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    // Se não tem termo de busca, limpar resultados
    if (!searchTerm.trim()) {
      setSearchResults([]);
      setShowResults(false);
      return;
    }

    // Atrasar busca para não fazer requisição a cada keystroke
    setLoading(true);
    searchTimeoutRef.current = setTimeout(async () => {
      try {
        setError(null);
        const results = await playersAPI.searchUsuarios(searchTerm);
        console.log('[PlayerSearchForm] Resultados brutos:', results);
        console.log('[PlayerSearchForm] IDs a excluir:', excludePlayerIds);
        
        // Filtrar resultados para excluir players já adicionados
        const filtered = results.filter(
          user => !excludePlayerIds.includes(user.id)
        );
        
        console.log('[PlayerSearchForm] Resultados filtrados:', filtered);
        setSearchResults(filtered);
        setShowResults(true);
      } catch (err) {
        console.error('[PlayerSearchForm] Erro na busca:', err);
        setError('Erro ao buscar jogadores');
        setSearchResults([]);
      } finally {
        setLoading(false);
      }
    }, 300); // Aguarda 300ms após o usuário parar de digitar
  }, [searchTerm, excludePlayerIds]);

  const handleSelectUser = (user) => {
    // Chamar callback com dados do usuário selecionado
    onSelectPlayer({
      id: user.id,
      name: user.nome,
      email: user.email,
      tipo: user.tipo
    });
    
    // Limpar busca
    setSearchTerm('');
    setSearchResults([]);
    setShowResults(false);
  };

  const handleAddNew = () => {
    onAddNew();
    setSearchTerm('');
    setSearchResults([]);
    setShowResults(false);
  };

  return (
    <div className="player-search-form">
      <div className="search-container">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onFocus={() => searchTerm.trim() && setShowResults(true)}
          placeholder="🔍 Buscar jogador por nome..."
          className="search-input"
          autoComplete="off"
        />
        {loading && <div className="search-spinner">...</div>}
      </div>

      {error && (
        <div className="search-error">
          ⚠️ {error}
        </div>
      )}

      {showResults && (
        <div className="search-results">
          {searchResults.length > 0 ? (
            <>
              <div className="results-header">
                <span className="results-count">
                  {searchResults.length} resultado{searchResults.length !== 1 ? 's' : ''} encontrado{searchResults.length !== 1 ? 's' : ''}
                </span>
              </div>
              <ul className="results-list">
                {searchResults.map((user) => (
                  <li
                    key={user.id}
                    className="result-item"
                    onClick={() => handleSelectUser(user)}
                  >
                    <div className="result-user-info">
                      <span className="result-name">{user.nome}</span>
                      <span className="result-email">{user.email}</span>
                      <span className={`result-tipo ${user.tipo}`}>
                        {user.tipo === 'organizador' && '📋 Organizador'}
                        {user.tipo === 'jogador' && '🎯 Jogador'}
                        {user.tipo === 'admin' && '🔐 Admin'}
                      </span>
                    </div>
                    <span className="result-action">Selecionar →</span>
                  </li>
                ))}
              </ul>
              <div className="results-footer">
                <button
                  type="button"
                  className="btn-add-new"
                  onClick={handleAddNew}
                >
                  ➕ Adicionar Novo Jogador
                </button>
              </div>
            </>
          ) : (
            <div className="no-results">
              <p>Nenhum jogador encontrado com "{searchTerm}"</p>
              <button
                type="button"
                className="btn-add-new"
                onClick={handleAddNew}
              >
                ➕ Adicionar Novo Jogador
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default PlayerSearchForm;
