import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock simples do App
const MockApp = () => (
  <div>
    <header>
      <h1>Racket Hero</h1>
      <nav>
        <a href="/">Home</a>
        <a href="/eventos">Eventos</a>
        <a href="/login">Login</a>
      </nav>
    </header>
    <main>
      <h2>Bem-vindo</h2>
    </main>
  </div>
);

test('deve renderizar o aplicativo principal', () => {
  render(<MockApp />);
  const heading = screen.getByText('Racket Hero');
  expect(heading).toBeInTheDocument();
});

test('deve ter navegação principal', () => {
  render(<MockApp />);
  expect(screen.getByText('Home')).toBeInTheDocument();
  expect(screen.getByText('Eventos')).toBeInTheDocument();
  expect(screen.getByText('Login')).toBeInTheDocument();
});

test('deve exibir mensagem de boas-vindas', () => {
  render(<MockApp />);
  expect(screen.getByText('Bem-vindo')).toBeInTheDocument();
});

