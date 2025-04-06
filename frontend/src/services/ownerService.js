import api from './api';

export const ownerService = {
  async createHall(hallData) {
    try {
      const response = await api.post('/halls', {
        name: hallData.name,
        description: hallData.description,
        capacity: hallData.capacity,
        price_per_hour: hallData.price,
        address: hallData.address,
        amenities: hallData.amenities || [],
        typeHall: hallData.typeHall || 'APARTAMENT'
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao criar salão');
    }
  },

  async getMyHalls() {
    try {
      const response = await api.get('/halls?owner_id=me');
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar salões');
    }
  },

  async getHallReservations(hallId, status = null) {
    try {
      const params = { hall_id: hallId };
      if (status) params.status = status;
      
      const response = await api.get('/reservations', { params });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar reservas');
    }
  },

  async updateReservationStatus(reservationId, status) {
    try {
      const response = await api.put(`/reservations/${reservationId}/status`, { status });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao atualizar reserva');
    }
  },

  _handleError(error, defaultMessage) {
    console.error('OwnerService Error:', error);
    return {
      message: error.response?.data?.error || defaultMessage,
      status: error.response?.status,
      data: error.response?.data
    };
  }
};