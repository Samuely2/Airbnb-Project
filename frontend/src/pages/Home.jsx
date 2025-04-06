import { useNavigate, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Header from '../components/header/Header';
import Footer from '../components/footer/Footers';
import styles from '../components/auth/home.module.css';
import { getCurrentUser } from '../services/userService';
import OwnerDashboard from '../components/usertypes/OwnerDashboard/OwnerDashboard';
import ContractorDashboard from '../components/usertypes/ContractorDashboard/ContractorDashboard';
import { UserTypes } from '../interfaces/userTypes';
import AuthLayout from '../components/layout/AuthLayout';

export default function Home() {
  const navigate = useNavigate();
  const location = useLocation();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [menuCollapsed, setMenuCollapsed] = useState(false);

  useEffect(() => {
    const currentUser = getCurrentUser();
    
    if (!currentUser) {
      navigate('/login', { state: { from: location }, replace: true });
      return;
    }
    
    setUser(currentUser);
    setLoading(false);
  }, [navigate, location]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const toggleMenu = () => {
    setMenuCollapsed(!menuCollapsed);
  };

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <div className={styles.loadingSpinner}></div>
        <p>Carregando...</p>
      </div>
    );
  }

  const renderUserSpecificContent = () => {
    if (!user) return null;
    
    switch(user.typeUser) {
      case UserTypes.OWNER:
        return <OwnerDashboard />;
      case UserTypes.CONTRACTOR:
        return <ContractorDashboard />;
      default:
        return (
          <div className={styles.defaultContent}>
            <h1>Bem-vindo, {user.name}!</h1>
            <p>Seu tipo de usuário não foi reconhecido.</p>
          </div>
        );
    }
  };

  return (
    <>
       <Header 
      userName={user?.name} 
      onToggleMenu={toggleMenu}
      collapsed={menuCollapsed}
    />
    
    <AuthLayout hasSidebar={true} collapsed={menuCollapsed}>
      <div className={styles.mainContentWrapper}>
        <main className={styles.mainContent}>
          {renderUserSpecificContent()}
        </main>
      </div>
      
      <button 
        onClick={handleLogout}
        className={styles.logoutButton}
      >
        Sair
      </button>
    </AuthLayout>

    <Footer />
    </>
  );
}