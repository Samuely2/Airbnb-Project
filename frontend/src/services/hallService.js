// src/services/hallService.js
import api from './api';

export const hallService = {
  async createHall(hallData) {
    try {
      const response = await api.post('/halls', hallData);
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao criar salão');
    }
  },

  async getAllHalls(filters = {}) {
    try {
      const params = {};
      if (filters.ownerId) params.owner_id = filters.ownerId;
      if (filters.minCapacity) params.min_capacity = filters.minCapacity;
      
      const response = await api.get('/halls', { params });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar salões');
    }
  },

  async getHallDetails(hallId) {
    try {
      const response = await api.get(`/halls/${hallId}`);
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar detalhes do salão');
    }
  },

  async updateHall(hallId, updateData) {
    try {
      const response = await api.put(`/halls/${hallId}`, updateData);
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao atualizar salão');
    }
  },

  async deleteHall(hallId) {
    try {
      const response = await api.delete(`/halls/${hallId}`);
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao remover salão');
    }
  },
  async getAvailableHalls(filters) {
    try {
      const params = {
        min_capacity: filters.capacity,
        start_date: filters.startDate?.toISOString(),
        end_date: filters.endDate?.toISOString()
      };
      const response = await api.get('/halls', { params });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar salões disponíveis');
    }
  },
  async checkAvailability(hallId, startDate, endDate) {
    try {
      const response = await api.get(`/halls/${hallId}/availability`, {
        params: {
          start_date: startDate.toISOString(),
          end_date: endDate.toISOString()
        }
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao verificar disponibilidade');
    }
  },

  _handleError(error, defaultMessage) {
    console.error('HallService Error:', error);
    return {
      message: error.response?.data?.error || defaultMessage,
      status: error.response?.status,
      data: error.response?.data
    };
  }
};