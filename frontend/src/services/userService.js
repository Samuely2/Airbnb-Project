import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

// Configuração global do Axios
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
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
      const response = await api.post('/users/register', {
        name: userData.name,
        phone: userData.phone,
        email: userData.email,
        password: userData.password,
        address: userData.address,
        typeUser: userData.typeUser || 'OWNER' // Padrão para OWNER se não especificado
      });

      // Processar resposta de sucesso
      if (response.data.token) {
        const decoded = jwtDecode(response.data.token);
        const userInfo = {
          ...response.data.user,
          typeUser: decoded.typeUser // Garantimos que vem do token
        };
        
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(userInfo));
      }

      return {
        success: true,
        user: response.data.user,
        token: response.data.token
      };
    } catch (error) {
      throw this.handleError(error, 'Erro no cadastro');
    }
  },

  async login(credentials) {
    try {
      const response = await api.post('/users/login', {
        email: credentials.email,
        password: credentials.password
      });

      if (response.data.token) {
        const decoded = jwtDecode(response.data.token);
        const userInfo = {
          ...response.data.user,
          typeUser: decoded.typeUser // Garantimos que vem do token
        };
        
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(userInfo));
      }

      return {
        success: true,
        user: response.data.user,
        token: response.data.token
      };
    } catch (error) {
      throw this.handleError(error, 'Credenciais inválidas');
    }
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete api.defaults.headers.common['Authorization'];
    window.location.href = '/login';
  },

  getCurrentUser() {
    try {
      const token = localStorage.getItem('token');
      const userData = localStorage.getItem('user');

      if (!token || !userData) return null;

      // Verificar se o token está expirado
      const decoded = jwtDecode(token);
      if (decoded.exp * 1000 < Date.now()) {
        this.logout();
        return null;
      }

      return JSON.parse(userData);
    } catch (error) {
      this.logout();
      return null;
    }
  },

  getUserType() {
    const user = this.getCurrentUser();
    return user?.typeUser || null;
  },

  isOwner() {
    return this.getUserType() === 'OWNER';
  },

  isContractor() {
    return this.getUserType() === 'CONTRACTOR';
  },

  isBoth() {
    return this.getUserType() === 'BOTH';
  },

  async updateProfile(profileData) {
    try {
      const response = await api.put('/users/me', profileData);
      
      if (response.data) {
        const currentUser = this.getCurrentUser();
        const updatedUser = {
          ...currentUser,
          ...response.data
        };
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
      
      return response.data;
    } catch (error) {
      throw this.handleError(error, 'Erro ao atualizar perfil');
    }
  },

  handleError(error, defaultMessage) {
    console.error('Erro:', error);
    
    const errorData = {
      message: error.response?.data?.error || error.message || defaultMessage,
      status: error.response?.status,
      data: error.response?.data
    };
    
    // Logout automático se não autorizado
    if (error.response?.status === 401) {
      this.logout();
    }
    
    return errorData;
  }
};

// Métodos nomeados para compatibilidade
export const registerUser = userData => userService.register(userData);
export const loginUser = credentials => userService.login(credentials);
export const logoutUser = () => userService.logout();
export const getCurrentUser = () => userService.getCurrentUser();