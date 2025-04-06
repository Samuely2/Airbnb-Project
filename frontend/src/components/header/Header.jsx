import { useState } from 'react';
import styles from './Header.module.css';
import logo from '../../img/airbnb.webp';
import { FaHome, FaSearch, FaHeart, FaEnvelope, FaBars, FaSignOutAlt } from 'react-icons/fa';

export default function Header({ userName }) {
  const [collapsed, setCollapsed] = useState(false);
  const userInitial = userName ? userName.charAt(0).toUpperCase() : 'U';

  const toggleMenu = () => {
    setCollapsed(!collapsed);
  };

  return (
    <div className={`${styles.sidebar} ${collapsed ? styles.collapsed : ''}`}>
      <div className={styles.sidebarHeader}>
        {!collapsed && <img src={logo} alt="Logo" className={styles.logo} />}
        <button className={styles.toggleButton} onClick={toggleMenu}>
          <FaBars />
        </button>
      </div>

      <nav className={styles.navMenu}>
        <ul>
          <li className={styles.navItem}>
            <FaHome className={styles.navIcon} />
            {!collapsed && <span>Início</span>}
          </li>
          <li className={styles.navItem}>
            <FaSearch className={styles.navIcon} />
            {!collapsed && <span>Explorar</span>}
          </li>
          <li className={styles.navItem}>
            <FaHeart className={styles.navIcon} />
            {!collapsed && <span>Favoritos</span>}
          </li>
          <li className={styles.navItem}>
            <FaEnvelope className={styles.navIcon} />
            {!collapsed && <span>Mensagens</span>}
          </li>
        </ul>
      </nav>

      <div className={styles.userArea}>
        <div className={styles.userAvatar}>{userInitial}</div>
        {!collapsed && (
          <div className={styles.userInfo}>
            <span className={styles.userName}>{userName}</span>
            <span className={styles.userStatus}>Online</span>
          </div>
        )}
        {!collapsed && (
          <button className={styles.logoutButton}>
            <FaSignOutAlt />
          </button>
        )}
      </div>
    </div>
  );
}