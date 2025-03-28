import styles from './Header.module.css';
import logo from '../../img/airbnb.webp'; // Caminho corrigido para a imagem

export default function Header({ userName }) {
  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <img src={logo} alt="Airbnb Logo" className={styles.logoImage} />
      </div>
      <div className={styles.userInfo}>
        <span>Olá, <strong>{userName}</strong>!</span>
      </div>
    </header>
  );
}