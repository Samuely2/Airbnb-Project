import axios from 'axios';

// Configuração global do Axios
const api = axios.create({
  baseURL: "/users",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
});

// Interceptor para adicionar o token JWT automaticamente
api.interceptors.request.use(config => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Interceptor para tratar erros de autenticação
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Serviços de Usuário
export const userService = {
  async register(userData) {
    try {
      const response = await api.post('/users', {
        name: userData.name,
        phone: userData.phone,
        email: userData.email,
        password: userData.password,
        address: userData.address,
        typeUser: userData.typeUser || 1
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error, 'Erro no cadastro');
    }
  },

  async login(credentials) {
    try {
      const response = await api.post('/users/login', credentials);
      
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    } catch (error) {
      throw this.handleError(error, 'Erro no login');
    }
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete api.defaults.headers.common['Authorization'];
  },

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  handleError(error, defaultMessage) {
    console.error('Erro:', error);
    
    const errorData = error.response?.data || {
      error: error.message || defaultMessage
    };
    
    if (error.response?.status === 401) {
      errorData.error = 'Sessão expirada. Faça login novamente.';
    }
    
    return errorData;
  }
};

// Métodos nomeados para compatibilidade
export const registerUser = userData => userService.register(userData);
export const loginUser = credentials => userService.login(credentials);
export const logoutUser = () => userService.logout();
export const getCurrentUser = () => userService.getCurrentUser();