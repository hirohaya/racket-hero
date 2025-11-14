import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import './Home.css';

const Home = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="home-container">
      <div className="home-hero">
        <h1>🏓 Bem-vindo ao Racket Hero</h1>
        <p>Gerenciamento de Torneios de Tênis de Mesa</p>

        {isAuthenticated ? (
          <div className="home-authenticated">
            <p>Olá, <strong>{user?.nome || 'Usuário'}</strong>!</p>
            <div className="home-links">
              <Link to="/eventos" className="btn-primary">
                Ver Eventos
              </Link>
              <Link to="/novo-evento" className="btn-secondary">
                Criar Novo Evento
              </Link>
            </div>
          </div>
        ) : (
          <div className="home-unauthenticated">
            <p>Faça login ou registre-se para começar!</p>
            <div className="home-links">
              <Link to="/login" className="btn-primary">
                Login
              </Link>
              <Link to="/register" className="btn-secondary">
                Registrar
              </Link>
            </div>
          </div>
        )}
      </div>

      <div className="home-features">
        <h2>Funcionalidades</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>📋 Gerenciamento de Eventos</h3>
            <p>Crie e gerencie seus torneios de tênis de mesa</p>
          </div>
          <div className="feature-card">
            <h3>🎯 Partidas</h3>
            <p>Registre resultados e acompanhe partidas</p>
          </div>
          <div className="feature-card">
            <h3>📊 Rankings</h3>
            <p>Veja rankings em tempo real com Elo rating</p>
          </div>
          <div className="feature-card">
            <h3>👥 Grupos</h3>
            <p>Organize jogadores em grupos</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
