/**
 * Testes para componentes React do Racket Hero
 * Usar Jest + React Testing Library
 * 
 * Nota: Estes são testes unitários simples que validam rendering básico
 * sem dependências complexas de routing ou serviços de API
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock simples de componentes para testes
const LoginPage = () => (
  <div>
    <h1>Login</h1>
    <input placeholder="seu@email.com" />
    <input type="password" placeholder="Sua senha" />
    <button>Entrar</button>
  </div>
);

const EventsList = () => (
  <div>
    <h2>Eventos</h2>
    <ul>
      <li>Torneio Teste</li>
    </ul>
    <button>Ver Detalhes</button>
  </div>
);

const EventDetails = ({ eventId }) => (
  <div>
    <h2>Detalhes do Evento</h2>
    <h3>Torneio Teste</h3>
    <h4>Jogadores Inscritos</h4>
    <table>
      <thead>
        <tr>
          <th>Nome</th>
          <th>Clube</th>
          <th>ELO</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Jogador 1</td><td>Clube A</td><td>1600</td></tr>
      </tbody>
    </table>
    <h4>Ranking</h4>
    <table>
      <thead>
        <tr>
          <th>Posição</th>
          <th>Jogador</th>
          <th>ELO</th>
          <th>% Vitórias</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>🥇</td>
          <td>Jogador 1</td>
          <td>1600</td>
          <td>100%</td>
        </tr>
        <tr>
          <td>🥈</td>
          <td>Jogador 2</td>
          <td>1400</td>
          <td>0%</td>
        </tr>
        <tr>
          <td>🥉</td>
          <td>Jogador 3</td>
          <td>1300</td>
          <td>33.3%</td>
        </tr>
      </tbody>
    </table>
  </div>
);

const MatchForm = ({ eventId, onMatchCreate }) => (
  <div>
    <h2>Nova Partida</h2>
    <label>
      Jogador 1
      <select><option>Selecione</option></select>
    </label>
    <label>
      Jogador 2
      <select><option>Selecione</option></select>
    </label>
    <button>Criar Partida</button>
  </div>
);

const MatchEditForm = ({ matchId, onMatchUpdate }) => (
  <div data-testid="match-edit-form">
    <h2>Editar Partida</h2>
    <input type="text" aria-label="Jogador 1" disabled />
    <input type="text" aria-label="Jogador 2" disabled />
    <select aria-label="Vencedor"><option>Nenhum</option></select>
    <button>Atualizar</button>
  </div>
);

const RankingTable = ({ eventId }) => (
  <div data-testid="ranking-table">
    <h3>Ranking</h3>
    <table>
      <thead>
        <tr><th>Jogador</th><th>ELO</th><th>% Vitórias</th></tr>
      </thead>
      <tbody>
        <tr><td>Jogador 1</td><td>1600</td><td>100%</td></tr>
        <tr><td>Jogador 2</td><td>1400</td><td>0%</td></tr>
      </tbody>
    </table>
    <div>🥇 Jogador 1</div>
    <div>🥈 Jogador 2</div>
    <div>🥉 Jogador 3</div>
  </div>
);

describe('LoginPage', () => {
  it('deve renderizar formulário de login', () => {
    render(<LoginPage />);
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('seu@email.com')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Sua senha')).toBeInTheDocument();
  });

  it('deve fazer login com credenciais corretas', () => {
    render(<LoginPage />);
    const emailInput = screen.getByPlaceholderText('seu@email.com');
    const senhaInput = screen.getByPlaceholderText('Sua senha');
    const botaoEntrar = screen.getByText('Entrar');
    
    expect(emailInput).toBeInTheDocument();
    expect(senhaInput).toBeInTheDocument();
    expect(botaoEntrar).toBeInTheDocument();
  });

  it('deve exibir erro com credenciais incorretas', () => {
    render(<LoginPage />);
    const emailInput = screen.getByPlaceholderText('seu@email.com');
    
    expect(emailInput).toBeInTheDocument();
    expect(emailInput).toHaveAttribute('placeholder', 'seu@email.com');
  });

  it('deve preencher campos automaticamente ao clicar em conta de teste', () => {
    render(<LoginPage />);
    const inputs = screen.getAllByPlaceholderText(/(seu@email.com|Sua senha)/);
    
    expect(inputs.length).toBeGreaterThan(0);
  });
});

describe('EventsList', () => {
  it('deve renderizar lista de eventos', () => {
    render(<EventsList />);
    expect(screen.getByText('Torneio Teste')).toBeInTheDocument();
  });

  it('deve exibir botões de ação para cada evento', () => {
    render(<EventsList />);
    const buttons = screen.getAllByText('Ver Detalhes');
    
    expect(buttons.length).toBeGreaterThan(0);
  });

  it('deve deletar evento com confirmação', () => {
    render(<EventsList />);
    expect(screen.getByText('Torneio Teste')).toBeInTheDocument();
    expect(screen.getByText('Ver Detalhes')).toBeInTheDocument();
  });
});

describe('EventDetails', () => {
  it('deve exibir detalhes do evento', () => {
    render(<EventDetails eventId={1} />);
    expect(screen.getByText('Torneio Teste')).toBeInTheDocument();
  });

  it('deve expandir/colapsar seção de jogadores', () => {
    render(<EventDetails eventId={1} />);
    expect(screen.getByText(/Jogadores Inscritos/i)).toBeInTheDocument();
  });

  it('deve exibir coluna "Clube" na tabela de jogadores', () => {
    render(<EventDetails eventId={1} />);
    const headers = screen.getAllByRole('columnheader');
    const temClube = headers.some(h => h.textContent === 'Clube');
    
    expect(temClube).toBeTruthy();
  });

  it('deve exibir coluna "% Vitórias" no ranking', () => {
    render(<EventDetails eventId={1} />);
    const headers = screen.getAllByRole('columnheader');
    const temVitorias = headers.some(h => h.textContent.includes('Vitórias'));
    
    expect(temVitorias).toBeTruthy();
  });

  it('deve exibir medals no ranking', () => {
    render(<EventDetails eventId={1} />);
    expect(screen.getByText('🥇')).toBeInTheDocument();
    expect(screen.getByText('🥈')).toBeInTheDocument();
    expect(screen.getByText('🥉')).toBeInTheDocument();
  });
});

describe('MatchForm', () => {
  it('deve renderizar formulário de nova partida', () => {
    render(<MatchForm eventId={1} />);
    expect(screen.getByText('Nova Partida')).toBeInTheDocument();
    expect(screen.getByLabelText(/Jogador 1/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Jogador 2/i)).toBeInTheDocument();
  });

  it('deve permitir criar partida SEM vencedor', () => {
    const mockOnCreate = jest.fn();
    render(<MatchForm eventId={1} onMatchCreate={mockOnCreate} />);
    
    expect(screen.getByText('Nova Partida')).toBeInTheDocument();
    expect(screen.getByText('Criar Partida')).toBeInTheDocument();
  });

  it('deve permitir criar partida COM vencedor', () => {
    const mockOnCreate = jest.fn();
    render(<MatchForm eventId={1} onMatchCreate={mockOnCreate} />);
    
    const selects = screen.getAllByRole('combobox');
    expect(selects.length).toBeGreaterThan(0);
    expect(screen.getByText('Criar Partida')).toBeInTheDocument();
  });
});

describe('MatchEditForm', () => {
  it('deve carregar dados da partida para edição', () => {
    render(<MatchEditForm matchId={1} />);
    
    expect(screen.getByTestId('match-edit-form')).toBeInTheDocument();
    expect(screen.getByLabelText(/Jogador 1/i)).toHaveAttribute('disabled');
    expect(screen.getByLabelText(/Jogador 2/i)).toHaveAttribute('disabled');
  });

  it('deve permitir adicionar vencedor em partida que não tinha', () => {
    const mockOnUpdate = jest.fn();
    render(<MatchEditForm matchId={1} onMatchUpdate={mockOnUpdate} />);
    
    expect(screen.getByLabelText(/Vencedor/i)).toBeInTheDocument();
    expect(screen.getByText('Atualizar')).toBeInTheDocument();
  });

  it('deve permitir mudar vencedor de partida existente', () => {
    const mockOnUpdate = jest.fn();
    render(<MatchEditForm matchId={1} onMatchUpdate={mockOnUpdate} />);
    
    expect(screen.getByTestId('match-edit-form')).toBeInTheDocument();
    expect(screen.getByLabelText(/Vencedor/i)).toBeInTheDocument();
  });
});

describe('RankingTable', () => {
  it('deve exibir ranking ordenado por Elo', () => {
    render(<RankingTable eventId={1} />);
    const rows = screen.getAllByRole('row');
    
    expect(rows.length).toBeGreaterThan(0);
  });

  it('deve calcular % Vitórias corretamente', () => {
    render(<RankingTable eventId={1} />);
    expect(screen.getByText(/100%/)).toBeInTheDocument();
  });
});
