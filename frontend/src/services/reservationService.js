import api from './api';

export const reservationService = {
  async create(reservationData) {
    try {
      const response = await api.post('/reservations', {
        fk_hall: reservationData.hallId,
        fk_user: reservationData.userId,
        start_date: reservationData.startDate.toISOString(),
        end_date: reservationData.endDate.toISOString(),
        notes: reservationData.notes
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao criar reserva');
    }
  },

  async getForOwner(ownerId) {
    try {
      // Primeiro busca os salões do dono
      const hallsResponse = await api.get('/halls', { params: { owner_id: ownerId } });
      const hallIds = hallsResponse.data.map(hall => hall.id);
      
      // Depois busca as reservas para esses salões
      const reservationsResponse = await api.get('/reservations', {
        params: { hall_id: hallIds.join(',') }
      });
      return reservationsResponse.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar reservas');
    }
  },

  async getForContractor(contractorId) {
    try {
      const response = await api.get('/reservations', {
        params: { user_id: contractorId }
      });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao buscar suas reservas');
    }
  },

  async updateStatus(reservationId, status) {
    try {
      const response = await api.put(`/reservations/${reservationId}/status`, { status });
      return response.data;
    } catch (error) {
      throw this._handleError(error, 'Erro ao atualizar status');
    }
  }
};