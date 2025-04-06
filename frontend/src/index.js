// src/index.js (raiz do projeto)
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext'; // Crie este contexto se necessário
import App from './App';
import reportWebVitals from './reportWebVitals';

// Importe o CSS global se existir
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// Opcional: Configuração para medir performance
reportWebVitals();