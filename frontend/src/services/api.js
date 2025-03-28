import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' 
    ? 'http://localhost:5000' 
    : 'http://backend:5000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// Configuração para adicionar o token JWT em requisições subsequentes
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const registerUser = async (userData) => {
  try {
    const response = await api.post('/users', {
      name: userData.name,
      phone: userData.phone,
      email: userData.email,
      password: userData.password,
      address: userData.address,
      typeUser: userData.typeUser || 'Dono'
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Erro ao cadastrar usuário' };
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await api.post('/users/login', {
      email: credentials.email,
      password: credentials.password
    });
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  } catch (error) {
    throw error.response?.data;
  }
};

export const logoutUser = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

export const getCurrentUser = () => {
  const user = localStorage.getItem('user');
  return user ? JSON.parse(user) : null;
};