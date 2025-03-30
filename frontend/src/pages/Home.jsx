import { useLocation, useNavigate } from 'react-router-dom';
import Header from '../components/header/Header';
import Footer from '../components/footer/Footers';
import styles from '../components/auth/home.module.css'; 

export default function Home() {
  const location = useLocation();
  const navigate = useNavigate();
  const userName = location.state?.name || 'Usuário'; 

  const handleLogout = () => {
    navigate('/login');
  };

  return (
    <div className={styles.homeContainer}>
      <Header userName={userName} />
      
      <main className={styles.mainContent}>
        <h1>Seja bem vindo!</h1>
        <p>Aqui você pode gerenciar suas reservas.</p>
        
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