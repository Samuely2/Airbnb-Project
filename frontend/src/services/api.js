import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NODE_ENV === 'development' 
    ? 'http://localhost:5000/users' 
    : 'http://backend:5000/users',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const registerUser = async (userData) => {
  try {
    const response = await api.post('/', {
      name: userData.name,
      phone: userData.phone,
      email: userData.email,
      password: userData.password,
      address: userData.address,
      typeUser: userData.typeUser || 'Dono' // Valor padrão
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Erro ao cadastrar usuário' };
  }
};
export const loginUser = async (credentials) => {
    try {
      const response = await api.post('/login', credentials);
      return response.data;
    } catch (error) {
      throw error.response?.data || new Error('Falha no login');
    }
  };