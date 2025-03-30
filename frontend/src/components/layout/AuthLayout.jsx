import styles from './AuthLayout.module.css';

const AuthLayout = ({ children }) => {
  return (
    <div className={styles.authContainer}>
      {children}
    </div>
  );
};

export default AuthLayout;