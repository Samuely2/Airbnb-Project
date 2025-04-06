import axios from 'axios';

// Configuração global do Axios
const api = axios.create({
  baseURL: "http://localhost:5000",
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
});

export default api;
