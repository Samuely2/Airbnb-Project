import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { loginUser } from '../../services/userService';
import styles from './LoginForm.module.css';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    
    try {
      if (!formData.email || !formData.password) {
        throw new Error('Preencha todos os campos');
      }

      await loginUser(formData);
      setMessage('Login realizado com sucesso!');
      // Após o sucesso da API:
navigate('/home', { 
  state: { 
    name: formData.name, // Substitua pelos dados reais da API
    email: formData.email 
  } 
});
      setTimeout(() => {
        navigate('/home');
      }, 1500);
      
    } catch (err) {
      setError(err.message || 'Erro ao fazer login');
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h2>Bem-vindo de volta</h2>
          <p>Faça login para acessar sua conta</p>
        </div>

        {error && <div className={styles.alertError}>{error}</div>}
        {message && <div className={styles.alertSuccess}>{message}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="Email"
            />
          </div>

          <div className={styles.formGroup}>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="Senha"
              minLength="6"
            />
          </div>

          <button type="submit" className={styles.submitButton}>
            Entrar
          </button>
        </form>

        <div className={styles.footer}>
          Não tem uma conta? <Link to="/register" className={styles.link}>Cadastre-se</Link>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;