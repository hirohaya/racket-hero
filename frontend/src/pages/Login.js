import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import './Auth.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!email || !senha) {
      setError('Preencha todos os campos');
      setLoading(false);
      return;
    }

    try {
      await login(email, senha);
      navigate('/');
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || 'Erro ao fazer login. Tente novamente.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>🏓 Login</h1>
        <p className="auth-subtitle">Bem-vindo ao Racket Hero</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="senha">Senha</label>
            <input
              id="senha"
              type="password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              placeholder="Sua senha"
              disabled={loading}
            />
          </div>

          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <div className="auth-links">
          <Link to="/forgot-password">Esqueceu sua senha?</Link>
          <span>Não tem conta? </span>
          <Link to="/register">Registre-se aqui</Link>
        </div>

        {/* Test Accounts */}
        <div className="test-accounts">
          <p className="test-accounts-title">🧪 Contas de Teste</p>
          <div className="test-accounts-list">
            <div className="test-account">
              <button
                type="button"
                className="test-account-btn"
                onClick={() => {
                  setEmail('jogador@test.com');
                  setSenha('Senha123!');
                  setError('');
                }}
              >
                <span className="account-role">🎯 Jogador</span>
                <span className="account-email">jogador@test.com</span>
                <span className="account-password">Senha123!</span>
              </button>
            </div>

            <div className="test-account">
              <button
                type="button"
                className="test-account-btn"
                onClick={() => {
                  setEmail('organizador@test.com');
                  setSenha('Senha123!');
                  setError('');
                }}
              >
                <span className="account-role">📋 Organizador</span>
                <span className="account-email">organizador@test.com</span>
                <span className="account-password">Senha123!</span>
              </button>
            </div>
          </div>
          <p className="test-accounts-info">Clique em uma conta para preenchê-la automaticamente</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
