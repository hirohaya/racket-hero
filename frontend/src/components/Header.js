import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import './Header.css';

const Header = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-logo">
          <Link to="/">🏓 Racket Hero</Link>
        </div>

        <nav className="header-nav">
          {isAuthenticated ? (
            <>
              <Link to="/">Home</Link>
              <Link to="/eventos">Eventos</Link>
              <div className="user-menu">
                <span className="user-name">{user?.nome || 'Usuário'}</span>
                <button onClick={handleLogout} className="logout-btn">
                  Sair
                </button>
              </div>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register" className="btn-register">
                Registrar
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
