import styles from './AuthLayout.module.css';

const AuthLayout = ({ children, hasSidebar = false, collapsed = false }) => {
  return (
    <div className={styles.layoutWrapper}>
      {hasSidebar && (
        <div 
          className={styles.sidebarPlaceholder} 
          style={{ width: collapsed ? '80px' : '250px' }}
        ></div>
      )}
      <div 
        className={styles.authContainer}
        style={{ 
          marginLeft: hasSidebar ? (collapsed ? '80px' : '250px') : '0',
          width: hasSidebar ? (collapsed ? 'calc(100% - 80px)' : 'calc(100% - 250px)') : '100%'
        }}
      >
        {children}
      </div>
    </div>
  );
};

export default AuthLayout;