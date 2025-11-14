import React, { useState } from 'react';
import logger, { Logger } from '../services/logger';
import '../styles/Debug.css';

const Debug = () => {
  const [logs, setLogs] = useState([]);
  const [selectedLevel, setSelectedLevel] = useState('');
  const [testMessage, setTestMessage] = useState('');

  // Carregar logs
  const loadLogs = () => {
    const allLogs = Logger.getLogs();
    setLogs(allLogs);
  };

  // Carregar logs ao montar o componente
  React.useEffect(() => {
    loadLogs();
    // Auto-atualizar a cada 2 segundos
    const interval = setInterval(loadLogs, 2000);
    return () => clearInterval(interval);
  }, []);

  // Filtrar logs
  const filteredLogs = selectedLevel
    ? logs.filter(log => log.level === selectedLevel)
    : logs;

  // Testar logger
  const testLogger = () => {
    if (!testMessage.trim()) return;

    const loggers = {
      debug: () => logger.debug(testMessage),
      info: () => logger.info(testMessage),
      warning: () => logger.warning(testMessage),
      error: () => logger.error(testMessage),
      critical: () => logger.critical(testMessage),
    };

    const action = selectedLevel || 'info';
    if (loggers[action]) {
      loggers[action]();
      setTestMessage('');
      loadLogs();
    }
  };

  return (
    <div className="debug-container">
      <h1>[DEBUG] Rastreamento de Logs</h1>

      <div className="debug-section">
        <h2>Teste de Logger</h2>
        <div className="test-form">
          <input
            type="text"
            value={testMessage}
            onChange={(e) => setTestMessage(e.target.value)}
            placeholder="Digite uma mensagem de teste..."
            className="test-input"
            onKeyPress={(e) => e.key === 'Enter' && testLogger()}
          />
          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="test-select"
          >
            <option value="">-- Nível --</option>
            <option value="debug">DEBUG</option>
            <option value="info">INFO</option>
            <option value="warning">WARNING</option>
            <option value="error">ERROR</option>
            <option value="critical">CRITICAL</option>
          </select>
          <button onClick={testLogger} className="btn-test">
            Enviar Log
          </button>
        </div>
      </div>

      <div className="debug-section">
        <h2>Gerenciamento de Logs ({filteredLogs.length})</h2>
        <div className="log-controls">
          <button
            onClick={loadLogs}
            className="btn-control btn-load"
            title="Recarregar logs"
          >
            Recarregar
          </button>
          <button
            onClick={() => {
              Logger.clearLogs();
              setLogs([]);
            }}
            className="btn-control btn-clear"
            title="Limpar todos os logs"
          >
            Limpar Logs
          </button>
          <button
            onClick={Logger.downloadLogs}
            className="btn-control btn-download"
            title="Baixar logs como JSON"
          >
            Baixar JSON
          </button>
          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="filter-select"
          >
            <option value="">Todos os Níveis</option>
            <option value="DEBUG">DEBUG</option>
            <option value="INFO">INFO</option>
            <option value="WARNING">WARNING</option>
            <option value="ERROR">ERROR</option>
            <option value="CRITICAL">CRITICAL</option>
          </select>
        </div>
      </div>

      <div className="debug-section">
        <h2>Logs em Tempo Real</h2>
        <div className="logs-list">
          {filteredLogs.length === 0 ? (
            <p className="no-logs">Nenhum log disponível</p>
          ) : (
            filteredLogs.map((log, index) => (
              <div key={index} className={`log-entry log-${log.level.toLowerCase()}`}>
                <div className="log-timestamp">
                  {new Date(log.timestamp).toLocaleTimeString('pt-BR')}
                </div>
                <div className="log-level">[{log.level}]</div>
                <div className="log-module">{log.module}</div>
                <div className="log-message">{log.message}</div>
                {log.data && (
                  <div className="log-data">
                    <pre>{JSON.stringify(log.data, null, 2)}</pre>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>

      <div className="debug-footer">
        <p className="hint">
          💡 Dica: Abra o console (F12) e acesse localStorage.getItem('RACKET_HERO_LOGS')
          para ver todos os logs em formato JSON
        </p>
      </div>
    </div>
  );
};

export default Debug;
