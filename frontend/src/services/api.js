import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' 
    ? 'http://localhost:5000'
    : 'http://backend:5000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
});

export const registerUser = async (userData) => {
  try {
    const response = await api.post('/users/', { 
      name: userData.name,
      phone: userData.phone,
      email: userData.email,
      password: userData.password,
      address: userData.address,
      typeUser: userData.typeUser || 'Dono'
    });
    return response.data;
  } catch (error) {
    const errorData = error.response?.data || {
      error: error.message || 'Erro desconhecido no cadastro'
    };
    throw errorData;
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