/**
 * Logger service para frontend
 * Gerencia logs no console, localStorage e com diferentes níveis
 */

const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARNING: 2,
  ERROR: 3,
  CRITICAL: 4,
};

const LOG_COLORS = {
  DEBUG: "color: #7f8c8d; font-weight: bold;",
  INFO: "color: #3498db; font-weight: bold;",
  WARNING: "color: #f39c12; font-weight: bold;",
  ERROR: "color: #e74c3c; font-weight: bold;",
  CRITICAL: "color: #c0392b; font-weight: bold; background: #ffe6e6;",
};

class Logger {
  constructor(name = "RacketHero", level = LOG_LEVELS.DEBUG) {
    this.name = name;
    this.level = level;
    this.maxLogs = 500; // Máximo de logs no localStorage
    this.initStorage();
  }

  /**
   * Inicializar localStorage se necessário
   */
  initStorage() {
    const key = "RACKET_HERO_LOGS";
    if (!localStorage.getItem(key)) {
      localStorage.setItem(key, JSON.stringify([]));
    }
  }

  /**
   * Formatar timestamp
   * @returns {string} HH:MM:SS
   */
  getTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString("pt-BR", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  }

  /**
   * Salvar log no localStorage
   * @param {string} level - Nível do log
   * @param {string} message - Mensagem
   * @param {object} data - Dados adicionais
   */
  saveToStorage(level, message, data = null) {
    try {
      const key = "RACKET_HERO_LOGS";
      const logs = JSON.parse(localStorage.getItem(key) || "[]");

      logs.push({
        timestamp: new Date().toISOString(),
        level,
        module: this.name,
        message,
        data,
      });

      // Manter apenas os últimos N logs
      if (logs.length > this.maxLogs) {
        logs.shift();
      }

      localStorage.setItem(key, JSON.stringify(logs));
    } catch (error) {
      console.error("Erro ao salvar log no localStorage:", error);
    }
  }

  /**
   * Log interno com formatação
   * @private
   */
  _log(level, message, data = null) {
    if (LOG_LEVELS[level] >= this.level) {
      const timestamp = this.getTimestamp();
      const logMessage = `[${timestamp}] [${this.name}] ${message}`;

      // Salvar no localStorage
      this.saveToStorage(level, message, data);

      // Exibir no console com cores
      const style = LOG_COLORS[level];
      if (data) {
        console.log(
          `%c${logMessage}`,
          style,
          data
        );
      } else {
        console.log(`%c${logMessage}`, style);
      }
    }
  }

  /**
   * Log de debug
   * @param {string} message
   * @param {object} data
   */
  debug(message, data = null) {
    this._log("DEBUG", message, data);
  }

  /**
   * Log de informação
   * @param {string} message
   * @param {object} data
   */
  info(message, data = null) {
    this._log("INFO", message, data);
  }

  /**
   * Log de warning
   * @param {string} message
   * @param {object} data
   */
  warning(message, data = null) {
    this._log("WARNING", message, data);
  }

  /**
   * Log de erro
   * @param {string} message
   * @param {object} data
   */
  error(message, data = null) {
    this._log("ERROR", message, data);
  }

  /**
   * Log crítico
   * @param {string} message
   * @param {object} data
   */
  critical(message, data = null) {
    this._log("CRITICAL", message, data);
  }

  /**
   * Obter todos os logs do localStorage
   * @returns {array} Array de logs
   */
  static getLogs() {
    try {
      return JSON.parse(localStorage.getItem("RACKET_HERO_LOGS") || "[]");
    } catch (error) {
      console.error("Erro ao ler logs:", error);
      return [];
    }
  }

  /**
   * Limpar todos os logs do localStorage
   */
  static clearLogs() {
    localStorage.setItem("RACKET_HERO_LOGS", JSON.stringify([]));
    console.log("%cLogs limpos!", LOG_COLORS.INFO);
  }

  /**
   * Exportar logs como JSON
   * @returns {string} JSON stringificado
   */
  static exportLogs() {
    const logs = Logger.getLogs();
    const json = JSON.stringify(logs, null, 2);
    return json;
  }

  /**
   * Baixar logs como arquivo
   */
  static downloadLogs() {
    const logs = Logger.exportLogs();
    const element = document.createElement("a");
    element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(logs));
    element.setAttribute("download", `racket-hero-logs-${new Date().toISOString()}.json`);
    element.style.display = "none";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  }
}

// Criar instância global
const logger = new Logger("RacketHero");

export default logger;
export { Logger };
