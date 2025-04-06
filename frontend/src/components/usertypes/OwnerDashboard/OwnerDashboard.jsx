import React, { useState, useEffect } from 'react';
import { ReservationStatus, UserType, EnumUtils } from '../../../enums/enumsEnv.ts';
import { hallService, reservationService } from '../../../services';
import styles from './OwnerDashboard.module.css';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { userService } from '../../../services/userService.js'; // ajuste o path conforme sua estrutura


const OwnerDashboard = () => {
  // Estados principais
  const [halls, setHalls] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Estados para navegação
  const [activeTab, setActiveTab] = useState('halls');
  const [selectedHall, setSelectedHall] = useState(null);
  const [showReservations, setShowReservations] = useState(false);
  const [dateRange, setDateRange] = useState([new Date(), new Date()]);
  const user = userService.getCurrentUser();
  // Estados para o formulário de salão
  const [showHallForm, setShowHallForm] = useState(false);
  const [currentHallId, setCurrentHallId] = useState(null);
  const [hallForm, setHallForm] = useState({
    name: '',
    capacity: '',
    price_per_hour: '',
    address: '',
    description: '',
    amenities: '',
    images: []
  });

  // Carregar dados iniciais
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [ownerHalls, ownerReservations] = await Promise.all([
          hallService.getAllHalls({ ownerId: user.id }),
          reservationService.getForOwner(user.id)
        ]);
        
        setHalls(ownerHalls);
        setReservations(ownerReservations);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [user.id]);

  // Manipular mudanças no formulário
  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setHallForm(prev => ({ ...prev, [name]: value }));
  };

  // Abrir formulário para criar novo salão
  const openCreateForm = () => {
    setCurrentHallId(null);
    setHallForm({
      name: '',
      capacity: '',
      price_per_hour: '',
      address: '',
      description: '',
      amenities: '',
      images: []
    });
    setShowHallForm(true);
    setSelectedHall(null);
  };

  // Abrir formulário para editar salão
  const openEditForm = (hall) => {
    setCurrentHallId(hall.id);
    setHallForm({
      name: hall.name,
      capacity: hall.capacity,
      price_per_hour: hall.price_per_hour,
      address: hall.address,
      description: hall.description || '',
      amenities: hall.amenities?.join(', ') || '',
      images: hall.images || []
    });
    setShowHallForm(true);
    setSelectedHall(null);
  };

  // Submeter formulário (criação/edição)
  const submitHallForm = async () => {
    try {
      const hallData = {
        ...hallForm,
        fk_owner: user.id,
        capacity: Number(hallForm.capacity),
        price_per_hour: Number(hallForm.price_per_hour),
        amenities: hallForm.amenities.split(',').map(item => item.trim()),
        images: hallForm.images
      };

      if (currentHallId) {
        // Editar salão existente
        const updatedHall = await hallService.updateHall(currentHallId, hallData);
        setHalls(halls.map(h => h.id === currentHallId ? updatedHall : h));
      } else {
        // Criar novo salão
        const newHall = await hallService.createHall(hallData);
        setHalls([...halls, newHall]);
      }

      setShowHallForm(false);
      alert(`Salão ${currentHallId ? 'atualizado' : 'criado'} com sucesso!`);
      window.location.reload();
    } catch (error) {
      alert(`Erro ao ${currentHallId ? 'atualizar' : 'criar'} salão: ${error.message}`);
    }
  };

  // Excluir salão
  const handleDeleteHall = async (hallId) => {
    if (window.confirm('Tem certeza que deseja excluir este salão?')) {
      try {
        await hallService.deleteHall(hallId);
        setHalls(halls.filter(h => h.id !== hallId));
        alert('Salão excluído com sucesso!');
      } catch (error) {
        alert(`Erro ao excluir salão: ${error.message}`);
      }
    }
  };

  // Atualizar status da reserva
  const handleStatusUpdate = async (reservationId, action) => {
    try {
      const status = action === 'accept' ? ReservationStatus.CONFIRMED : ReservationStatus.CANCELED;
      await reservationService.updateStatus(reservationId, status);
      const updated = await reservationService.getForOwner(user?.id);
      setReservations(updated);
      alert(`Reserva ${action === 'accept' ? 'aceita' : 'recusada'} com sucesso!`);
    } catch (error) {
      alert(`Erro ao atualizar reserva: ${error.message}`);
    }
  };

  // Atualizar disponibilidade
  const handleUpdateAvailability = async () => {
    if (!selectedHall) return;
    
    try {
      await hallService.addUnavailableDates(selectedHall.id, {
        startDate: dateRange[0],
        endDate: dateRange[1]
      });
      alert('Disponibilidade atualizada com sucesso!');
    } catch (error) {
      alert(`Erro ao atualizar disponibilidade: ${error.message}`);
    }
  };

  if (loading) return <div className={styles.loading}>Carregando...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  const isOwner = [UserType.OWNER, UserType.BOTH].includes(UserType.OWNER);

  return (
    <div className={styles.dashboardContainer}>
      <h2 className={styles.title}>Painel do Proprietário</h2>
      
      <div className={styles.tabs}>
        <button 
          className={`${styles.tabButton} ${activeTab === 'halls' ? styles.active : ''}`}
          onClick={() => setActiveTab('halls')}
        >
          Meus Salões
        </button>
        <button 
          className={`${styles.tabButton} ${activeTab === 'reservations' ? styles.active : ''}`}
          onClick={() => setActiveTab('reservations')}
        >
          Todas as Reservas
        </button>
      </div>

      {activeTab === 'halls' && (
        <div className={styles.propertySection}>
          <button 
            className={styles.addButton}
            onClick={openCreateForm}
          >
            + Adicionar Novo Salão
          </button>

          {/* Formulário de salão */}
          {showHallForm && (
            <div className={styles.formModal}>
              <div className={styles.formContent}>
                <h3>{currentHallId ? 'Editar Salão' : 'Adicionar Novo Salão'}</h3>
                
                <div className={styles.formGroup}>
                  <label>Nome do Salão:</label>
                  <input
                    type="text"
                    name="name"
                    value={hallForm.name}
                    onChange={handleFormChange}
                    required
                  />
                </div>

                <div className={styles.formGroup}>
                  <label>Capacidade (pessoas):</label>
                  <input
                    type="number"
                    name="capacity"
                    value={hallForm.capacity}
                    onChange={handleFormChange}
                    min="1"
                    required
                  />
                </div>

                <div className={styles.formGroup}>
                  <label>Preço por hora (R$):</label>
                  <input
                    type="number"
                    name="price_per_hour"
                    value={hallForm.price_per_hour}
                    onChange={handleFormChange}
                    min="0"
                    step="0.01"
                    required
                  />
                </div>

                <div className={styles.formGroup}>
                  <label>Endereço:</label>
                  <input
                    type="text"
                    name="address"
                    value={hallForm.address}
                    onChange={handleFormChange}
                    required
                  />
                </div>

                <div className={styles.formGroup}>
                  <label>Descrição:</label>
                  <textarea
                    name="description"
                    value={hallForm.description}
                    onChange={handleFormChange}
                  />
                </div>

                <div className={styles.formGroup}>
                  <label>Comodidades (separadas por vírgula):</label>
                  <input
                    type="text"
                    name="amenities"
                    value={hallForm.amenities}
                    onChange={handleFormChange}
                    placeholder="Ex: Wi-Fi, Estacionamento, Cozinha"
                  />
                </div>

                <div className={styles.formActions}>
                  <button 
                    className={styles.cancelButton}
                    onClick={() => setShowHallForm(false)}
                  >
                    Cancelar
                  </button>
                  <button 
                    className={styles.saveButton}
                    onClick={submitHallForm}
                  >
                    {currentHallId ? 'Atualizar' : 'Salvar'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Lista de salões */}
          <div className={styles.propertyGrid}>
            {halls.map(hall => (
              <div key={hall.id} className={styles.propertyCard}>
                <div 
                  className={styles.propertyImage}
                  style={{ backgroundImage: `url(${hall.images?.[0] || '/default-hall.jpg'})` }}
                />
                <div className={styles.propertyInfo}>
                  <h3>{hall.name}</h3>
                  <p><strong>Local:</strong> {hall.address}</p>
                  <p><strong>Capacidade:</strong> {hall.capacity} pessoas</p>
                  <p><strong>Preço:</strong> R$ {hall.price_per_hour}/hora</p>
                  <div className={styles.propertyActions}>
                    <button 
                      className={styles.editButton}
                      onClick={() => openEditForm(hall)}
                    >
                      Editar
                    </button>
                    <button 
                      className={styles.deleteButton}
                      onClick={() => handleDeleteHall(hall.id)}
                    >
                      Excluir
                    </button>
                    <button 
                      className={styles.viewButton}
                      onClick={() => setSelectedHall(hall)}
                    >
                      {selectedHall?.id === hall.id ? 'Fechar' : 'Gerenciar'}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Detalhes do salão selecionado */}
          {selectedHall && !showHallForm && (
            <div className={styles.propertyDetail}>
              <h3>Gerenciar: {selectedHall.name}</h3>
              
              <div className={styles.detailContent}>
                <div className={styles.calendarSection}>
                  <h4>Disponibilidade</h4>
                  <Calendar
                    selectRange
                    onChange={setDateRange}
                    value={dateRange}
                    tileClassName={({ date }) => {
                      const isBooked = reservations.some(
                        r => r.hall_id === selectedHall.id && 
                             new Date(r.start_date) <= date && 
                             date <= new Date(r.end_date) &&
                             r.status !== ReservationStatus.CANCELED
                      );
                      return isBooked ? styles.unavailableDay : '';
                    }}
                  />
                  {isOwner && (
                    <button 
                      className={styles.blockButton} 
                      onClick={handleUpdateAvailability}
                      style={{ marginTop: '10px' }}
                    >
                      Bloquear Datas Selecionadas
                    </button>
                  )}
                </div>

                <div className={styles.interestedSection}>
                  <button 
                    className={styles.toggleButton}
                    onClick={() => setShowReservations(!showReservations)}
                  >
                    {showReservations ? 'Ocultar Reservas' : 'Mostrar Reservas'}
                  </button>

                  {showReservations && (
                    <div className={styles.reservationList}>
                      <h4>Reservas para este salão</h4>
                      {reservations
                        .filter(r => r.hall_id === selectedHall.id)
                        .map(reservation => (
                          <div key={reservation.id} className={styles.reservationItem}>
                            <p><strong>Cliente:</strong> {reservation.user_name}</p>
                            <p><strong>Data:</strong> {new Date(reservation.start_date).toLocaleDateString()} a {new Date(reservation.end_date).toLocaleDateString()}</p>
                            <p><strong>Status:</strong> 
                              <span className={
                                reservation.status === ReservationStatus.CONFIRMED ? styles.confirmed :
                                reservation.status === ReservationStatus.PENDING ? styles.pending :
                                styles.rejected
                              }>
                                {EnumUtils.getReservationStatusLabel(reservation.status)}
                              </span>
                            </p>
                            {reservation.status === ReservationStatus.PENDING && isOwner && (
                              <div className={styles.reservationActions}>
                                <button 
                                  className={styles.acceptButton}
                                  onClick={() => handleStatusUpdate(reservation.id, 'accept')}
                                >
                                  Aceitar
                                </button>
                                <button 
                                  className={styles.rejectButton}
                                  onClick={() => handleStatusUpdate(reservation.id, 'reject')}
                                >
                                  Recusar
                                </button>
                              </div>
                            )}
                          </div>
                        ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'reservations' && (
        <div className={styles.bookingsSection}>
          <div className={styles.bookingList}>
            {reservations.length > 0 ? (
              reservations
                .sort((a, b) => new Date(b.start_date) - new Date(a.start_date))
                .map(reservation => (
                  <div key={reservation.id} className={styles.bookingItem}>
                    <p><strong>{reservation.hall_name}</strong></p>
                    <p><strong>Cliente:</strong> {reservation.user_name}</p>
                    <p><strong>Data:</strong> {new Date(reservation.start_date).toLocaleDateString()} a {new Date(reservation.end_date).toLocaleDateString()}</p>
                    <p><strong>Status:</strong> 
                      <span className={
                        reservation.status === ReservationStatus.CONFIRMED ? styles.confirmed :
                        reservation.status === ReservationStatus.PENDING ? styles.pending :
                        styles.rejected
                      }>
                        {EnumUtils.getReservationStatusLabel(reservation.status)}
                      </span>
                    </p>
                    <div className={styles.bookingActions}>
                      {reservation.status === ReservationStatus.PENDING && isOwner && (
                        <>
                          <button 
                            className={styles.acceptButton}
                            onClick={() => handleStatusUpdate(reservation.id, 'accept')}
                          >
                            Aceitar
                          </button>
                          <button 
                            className={styles.rejectButton}
                            onClick={() => handleStatusUpdate(reservation.id, 'reject')}
                          >
                            Recusar
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                ))
            ) : (
              <p className={styles.noBookings}>Nenhuma reserva encontrada.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default OwnerDashboard;