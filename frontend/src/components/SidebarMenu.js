/**
 * SidebarMenu.js - Barra de menu lateral para navegação dentro do evento
 * 
 * Mostra opções de:
 * - Jogadores
 * - Partidas
 * - Evento (apenas para organizadores)
 * 
 * Respeita permissões de cada tipo de usuário
 */

import React from 'react';
import './SidebarMenu.css';

function SidebarMenu({ eventId, currentPage, onNavigate, isOrganizer, user }) {
  const menuItems = [
    {
      id: 'players',
      label: '👥 Jogadores',
      page: 'players',
      requiredRole: null // Todos podem ver jogadores
    },
    {
      id: 'matches',
      label: '🏓 Partidas',
      page: 'matches',
      requiredRole: null // Todos podem ver partidas
    },
    {
      id: 'event',
      label: '⚙️ Evento',
      page: 'event',
      requiredRole: 'organizador' // Apenas organizadores
    }
  ];

  // Filtrar itens baseado em permissões
  const visibleItems = menuItems.filter(item => {
    if (!item.requiredRole) return true;
    if (item.requiredRole === 'organizador') return isOrganizer;
    return false;
  });

  return (
    <aside className="sidebar-menu">
      <div className="sidebar-header">
        <h3>Menu</h3>
      </div>

      <nav className="sidebar-nav">
        <ul className="nav-list">
          {visibleItems.map(item => (
            <li key={item.id} className="nav-item">
              <button
                className={`nav-link ${currentPage === item.page ? 'active' : ''}`}
                onClick={() => onNavigate(item.page)}
                title={item.label}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {isOrganizer && (
        <div className="sidebar-footer">
          <p className="role-badge">👨‍💼 Organizador</p>
        </div>
      )}
    </aside>
  );
}

export default SidebarMenu;
