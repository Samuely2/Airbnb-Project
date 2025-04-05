import React, { useState } from 'react';
import styles from './ContractorDashboard.module.css';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

const ContractorDashboard = () => {
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [dateRange, setDateRange] = useState([new Date(), new Date()]);
  const [activeTab, setActiveTab] = useState('available');
  const [showCalendar, setShowCalendar] = useState(false);

  // Dados de exemplo
  const availableProperties = [
    { id: 1, name: 'Salão de Festas A', location: 'Centro', capacity: 100, price: 500 },
    { id: 2, name: 'Salão de Festas B', location: 'Zona Sul', capacity: 150, price: 700 },
    // ... mais propriedades
  ];

  const pendingBookings = [
    { id: 1, property: 'Salão A', date: '10/10/2023', status: 'pending' },
  ];

  const confirmedBookings = [
    { id: 2, property: 'Salão B', date: '25/10/2023', status: 'confirmed' },
  ];

  const handleReserve = (property) => {
    setSelectedProperty(property);
    setShowCalendar(true);
  };

  const confirmReservation = () => {
    // Lógica para confirmar reserva
    alert(`Reserva confirmada para ${selectedProperty.name} nas datas selecionadas`);
    setShowCalendar(false);
    setSelectedProperty(null);
  };

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
          className={`${styles.tabButton} ${activeTab === 'pending' ? styles.active : ''}`}
          onClick={() => setActiveTab('pending')}
        >
          Minhas Reservas Pendentes
        </button>
        <button 
          className={`${styles.tabButton} ${activeTab === 'confirmed' ? styles.active : ''}`}
          onClick={() => setActiveTab('confirmed')}
        >
          Minhas Reservas Confirmadas
        </button>
      </div>

      {activeTab === 'available' && (
        <div className={styles.propertySection}>
          {showCalendar && selectedProperty ? (
            <div className={styles.reservationFlow}>
              <h3>Reservar: {selectedProperty.name}</h3>
              
              <div className={styles.calendarContainer}>
                <Calendar
                  selectRange
                  onChange={setDateRange}
                  value={dateRange}
                  tileClassName={({ date }) => {
                    // Lógica para marcar dias ocupados
                    return date.getDay() === 0 ? styles.unavailableDay : '';
                  }}
                />
              </div>
              
              <div className={styles.reservationActions}>
                <button 
                  className={styles.cancelButton}
                  onClick={() => setShowCalendar(false)}
                >
                  Cancelar
                </button>
                <button 
                  className={styles.confirmButton}
                  onClick={confirmReservation}
                >
                  Confirmar Reserva
                </button>
              </div>
            </div>
          ) : (
            <div className={styles.propertyGrid}>
              {availableProperties.map(property => (
                <div key={property.id} className={styles.propertyCard}>
                  <div className={styles.propertyImage}></div>
                  <div className={styles.propertyInfo}>
                    <h3>{property.name}</h3>
                    <p>Local: {property.location}</p>
                    <p>Capacidade: {property.capacity} pessoas</p>
                    <p>Preço: R$ {property.price}/noite</p>
                    <button 
                      className={styles.reserveButton}
                      onClick={() => handleReserve(property)}
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

      {activeTab === 'pending' && (
        <div className={styles.bookingsSection}>
          {pendingBookings.length > 0 ? (
            <div className={styles.bookingList}>
              {pendingBookings.map(booking => (
                <div key={booking.id} className={styles.bookingItem}>
                  <p><strong>{booking.property}</strong></p>
                  <p>Data: {booking.date}</p>
                  <p>Status: <span className={styles.pending}>Pendente</span></p>
                </div>
              ))}
            </div>
          ) : (
            <p className={styles.noBookings}>Nenhuma reserva pendente.</p>
          )}
        </div>
      )}

      {activeTab === 'confirmed' && (
        <div className={styles.bookingsSection}>
          {confirmedBookings.length > 0 ? (
            <div className={styles.bookingList}>
              {confirmedBookings.map(booking => (
                <div key={booking.id} className={styles.bookingItem}>
                  <p><strong>{booking.property}</strong></p>
                  <p>Data: {booking.date}</p>
                  <p>Status: <span className={styles.confirmed}>Confirmado</span></p>
                  <button className={styles.detailsButton}>Ver Detalhes</button>
                </div>
              ))}
            </div>
          ) : (
            <p className={styles.noBookings}>Nenhuma reserva confirmada.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default ContractorDashboard;