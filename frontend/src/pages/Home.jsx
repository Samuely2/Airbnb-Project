import { useNavigate } from 'react-router-dom';
import Header from '../components/header/Header';
import Footer from '../components/footer/Footers';
import styles from '../components/auth/home.module.css';
import { getCurrentUser } from '../services/userService';
import { useEffect, useState } from 'react';
import OwnerDashboard from '../components/usertypes/OwnerDashboard/OwnerDashboard';
import ContractorDashboard from '../components/usertypes/ContractorDashboard/ContractorDashboard';
import { UserTypes } from '../interfaces/userTypes';

export default function Home() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const currentUser = getCurrentUser();
    
    if (!currentUser) {
      navigate('/login');
      return;
    }
    
    setUser(currentUser);
    setLoading(false);
  }, [navigate]);

  const handleLogout = () => {
    // Limpar localStorage e redirecionar
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  if (loading) {
    return <div>Carregando...</div>;
  }

  const renderUserSpecificContent = () => {
    if (user.typeUser === UserTypes.OWNER) {
      return <OwnerDashboard/>;
    }
    if (user.typeUser === UserTypes.CONTRACTOR) {
      return <ContractorDashboard/>;
    }
    
    return (
      <div>
        <h1>Bem-vindo!</h1>
        <p>Seu tipo de usuário não foi reconhecido.</p>
      </div>
    );
  };
  return (
    <div className={styles.homeContainer}>
      <Header userName={user.name} />
      
      <main className={styles.mainContent}>
        {renderUserSpecificContent()}
        
        <button 
          onClick={handleLogout}
          className={styles.logoutButton}
        >
          Sair
        </button>
      </main>

      <Footer />
    </div>
  );
}