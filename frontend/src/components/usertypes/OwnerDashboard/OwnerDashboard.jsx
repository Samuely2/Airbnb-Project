import React, { useState } from 'react';
import styles from './OwnerDashboard.module.css';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

const OwnerDashboard = () => {
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [showInterested, setShowInterested] = useState(false);
  const [dateRange, setDateRange] = useState([new Date(), new Date()]);
  const [activeTab, setActiveTab] = useState('properties');

  // Dados de exemplo
  const properties = [
    { id: 1, name: 'Salão de Festas A', location: 'Centro', capacity: 100, price: 500 },
    { id: 2, name: 'Salão de Festas B', location: 'Zona Sul', capacity: 150, price: 700 },
    // ... mais propriedades
  ];

  const interestedClients = [
    { id: 1, name: 'Cliente X', eventDate: '15/10/2023', guests: 80 },
    { id: 2, name: 'Cliente Y', eventDate: '20/10/2023', guests: 120 },
  ];

  const bookings = [
    { id: 1, property: 'Salão A', date: '10/10/2023', status: 'confirmed' },
    { id: 2, property: 'Salão B', date: '25/10/2023', status: 'pending' },
  ];

  return (
    <div className={styles.dashboardContainer}>
      <h2 className={styles.title}>Painel do Proprietário</h2>
      
      <div className={styles.tabs}>
        <button 
          className={`${styles.tabButton} ${activeTab === 'properties' ? styles.active : ''}`}
          onClick={() => setActiveTab('properties')}
        >
          Minhas Propriedades
        </button>
        <button 
          className={`${styles.tabButton} ${activeTab === 'bookings' ? styles.active : ''}`}
          onClick={() => setActiveTab('bookings')}
        >
          Minhas Reservas
        </button>
      </div>

      {activeTab === 'properties' && (
        <div className={styles.propertySection}>
          <div className={styles.propertyGrid}>
            {properties.map(property => (
              <div key={property.id} className={styles.propertyCard}>
                <div className={styles.propertyImage}></div>
                <div className={styles.propertyInfo}>
                  <h3>{property.name}</h3>
                  <p>Local: {property.location}</p>
                  <p>Capacidade: {property.capacity} pessoas</p>
                  <p>Preço: R$ {property.price}/noite</p>
                  <div className={styles.propertyActions}>
                    <button 
                      className={styles.viewButton}
                      onClick={() => setSelectedProperty(property)}
                    >
                      Visualizar
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {selectedProperty && (
            <div className={styles.propertyDetail}>
              <h3>Detalhes: {selectedProperty.name}</h3>
              
              <div className={styles.detailContent}>
                <div className={styles.calendarSection}>
                  <h4>Disponibilidade</h4>
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

                <div className={styles.interestedSection}>
                  <button 
                    className={styles.toggleInterested}
                    onClick={() => setShowInterested(!showInterested)}
                  >
                    {showInterested ? 'Ocultar' : 'Mostrar'} Interessados
                  </button>

                  {showInterested && (
                    <div className={styles.interestedList}>
                      <h4>Clientes Interessados</h4>
                      {interestedClients.length > 0 ? (
                        <ul>
                          {interestedClients.map(client => (
                            <li key={client.id} className={styles.interestedItem}>
                              <p>{client.name}</p>
                              <p>Data do Evento: {client.eventDate}</p>
                              <p>Convidados: {client.guests}</p>
                              <button className={styles.contactButton}>Contatar</button>
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p>Nenhum cliente interessado ainda.</p>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'bookings' && (
        <div className={styles.bookingsSection}>
          <div className={styles.bookingTabs}>
            <button className={styles.bookingTab}>Pendentes</button>
            <button className={styles.bookingTab}>Confirmadas</button>
            <button className={styles.bookingTab}>Histórico</button>
          </div>

          <div className={styles.bookingList}>
            {bookings.map(booking => (
              <div key={booking.id} className={styles.bookingItem}>
                <p><strong>{booking.property}</strong></p>
                <p>Data: {booking.date}</p>
                <p>Status: 
                  <span className={booking.status === 'confirmed' ? styles.confirmed : styles.pending}>
                    {booking.status === 'confirmed' ? 'Confirmado' : 'Pendente'}
                  </span>
                </p>
                <div className={styles.bookingActions}>
                  {booking.status === 'pending' && (
                    <>
                      <button className={styles.acceptButton}>Aceitar</button>
                      <button className={styles.rejectButton}>Recusar</button>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default OwnerDashboard;