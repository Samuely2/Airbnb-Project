import api from './api';

export const contractorService = {
  async searchHalls(filters = {}) {
    try {
      const response = await api.get('/halls', {
        params: {
          min_capacity: filters.minCapacity,
          max_price: filters.maxPrice,
          location: filters.location,
          type: filters.typeHall
        }
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar salões');
    }
  },

  async createReservation(reservationData) {
    try {
      const response = await api.post('/reservations', {
        fk_hall: reservationData.hallId,
        start_date: reservationData.startDate,
        end_date: reservationData.endDate,
        notes: reservationData.notes || ''
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao criar reserva');
    }
  },

  async getMyReservations(status = null) {
    try {
      const params = {};
      if (status) params.status = status;
      
      const response = await api.get('/reservations?user_id=me', { params });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar reservas');
    }
  },

  async cancelReservation(reservationId) {
    try {
      const response = await api.put(`/reservations/${reservationId}/status`, {
        status: 'cancelada' // Usando o enum do seu backend
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao cancelar reserva');
    }
  },

  _handleError(error, defaultMessage) {
    console.error('ContractorService Error:', error);
    return {
      message: error.response?.data?.error || defaultMessage,
      status: error.response?.status,
      data: error.response?.data
    };
  }
};