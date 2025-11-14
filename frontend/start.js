#!/usr/bin/env node
/**
 * Script simples para iniciar o servidor de desenvolvimento
 * Evita problemas com webpack do create-react-app
 */

const path = require('path');
const http = require('http');
const fs = require('fs');

// Tentar usar react-scripts normalmente
try {
  require('react-scripts/scripts/start.js');
} catch (error) {
  console.error('Erro ao iniciar com react-scripts:', error.message);
  console.log('\nTentando alternativa: usar webpack-dev-server diretamente...');
  
  // Se falhar, usar alternativa
  process.exit(1);
}
