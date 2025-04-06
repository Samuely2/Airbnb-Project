import React, { useState, useEffect } from 'react';
import { ReservationStatus, EnumUtils } from '../../../enums/enumsEnv.ts'; 
import { hallService, reservationService } from '../../../services';
import styles from './ContractorDashboard.module.css';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { userService } from '../../../services/userService.js';

const ContractorDashboard = () => {
  const [halls, setHalls] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('available');
  const [selectedHall, setSelectedHall] = useState(null);
  const [showCalendar, setShowCalendar] = useState(false);
  const [dateRange, setDateRange] = useState([new Date(), new Date()]);
  const user = userService.getCurrentUser();

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [availableHalls, myReservations] = await Promise.all([
          hallService.getAvailableHalls({}),
          reservationService.getForContractor(user.id)
        ]);
        setHalls(availableHalls);
        setReservations(myReservations);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [user.id]);

  const handleReserve = async () => {
    if (!selectedHall) return;
    
    try {
      await reservationService.create({
        hallId: selectedHall.id,
        userId: user.id,
        startDate: dateRange[0],
        endDate: dateRange[1],
        status: ReservationStatus.PENDING
      });
      
      const updated = await reservationService.getForContractor(user.id);
      setReservations(updated);
      alert('Reserva solicitada com sucesso!');
      setShowCalendar(false);
      setSelectedHall(null);
    } catch (error) {
      alert(`Erro ao reservar: ${error.message}`);
    }
  };

  const handleCancel = async (reservationId) => {
    if (window.confirm('Tem certeza que deseja cancelar esta reserva?')) {
      try {
        await reservationService.updateStatus(
          reservationId, 
          ReservationStatus.CANCELED
        );
        const updated = await reservationService.getForContractor(user.id);
        setReservations(updated);
        alert('Reserva cancelada com sucesso!');
      } catch (error) {
        alert(`Erro ao cancelar reserva: ${error.message}`);
      }
    }
  };

  if (loading) return <div className={styles.loading}>Carregando...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.dashboardContainer}>
      <h2 className={styles.title}>Painel do Contratante</h2>
      
      <div className={styles.tabs}>
        <button 
          className={`${styles.tabButton} ${activeTab === 'available' ? styles.active : ''}`}
          onClick={() => setActiveTab('available')}
        >
          Salões Disponíveis
        </button>
        <button 
          className={`${styles.tabButton} ${activeTab === 'my-reservations' ? styles.active : ''}`}
          onClick={() => setActiveTab('my-reservations')}
        >
          Minhas Reservas
        </button>
      </div>

      {activeTab === 'available' && (
        <div className={styles.propertySection}>
          {showCalendar && selectedHall ? (
            <div className={styles.reservationFlow}>
              <h3>Reservar: {selectedHall.name}</h3>
              
              <div className={styles.calendarContainer}>
                <Calendar
                  selectRange
                  onChange={setDateRange}
                  value={dateRange}
                  minDate={new Date()}
                  tileClassName={({ date }) => {
                    const isUnavailable = reservations.some(
                      r => r.hall_id === selectedHall.id && 
                           new Date(r.start_date) <= date && 
                           date <= new Date(r.end_date) &&
                           r.status !== ReservationStatus.CANCELED
                    );
                    return isUnavailable ? styles.unavailableDay : '';
                  }}
                />
              </div>
              
              <div className={styles.reservationActions}>
                <button 
                  className={styles.rejectButton}
                  onClick={() => setShowCalendar(false)}
                >
                  Cancelar
                </button>
                <button 
                  className={styles.acceptButton}
                  onClick={handleReserve}
                  disabled={!dateRange[0] || !dateRange[1]}
                >
                  Confirmar Reserva
                </button>
              </div>
            </div>
          ) : (
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
                    <button 
                      className={styles.viewButton}
                      onClick={() => {
                        setSelectedHall(hall);
                        setShowCalendar(true);
                      }}
                    >
                      Reservar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'my-reservations' && (
        <div className={styles.bookingsSection}>
          <div className={styles.bookingList}>
            {reservations.length > 0 ? (
              reservations
                .sort((a, b) => new Date(b.start_date) - new Date(a.start_date))
                .map(reservation => (
                  <div key={reservation.id} className={styles.bookingItem}>
                    <p><strong>{reservation.hall_name}</strong></p>
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
                    {reservation.status === ReservationStatus.PENDING && (
                      <button 
                        className={styles.rejectButton}
                        onClick={() => handleCancel(reservation.id)}
                      >
                        Cancelar Reserva
                      </button>
                    )}
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

export default ContractorDashboard;