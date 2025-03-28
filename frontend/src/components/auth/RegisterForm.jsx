import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { registerUser } from '../../services/api';
import styles from './RegisterForm.module.css';

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    password: '',
    address: '',
    typeUser: 'Dono'
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
      if (!formData.name || !formData.phone || !formData.email || !formData.password || !formData.address) {
        throw new Error('Preencha todos os campos obrigatórios');
      }

      await registerUser(formData);
      setMessage('Cadastro realizado com sucesso!');
      
      setTimeout(() => {
        navigate('/login');
      }, 1500);
      
    } catch (err) {
      setError(err.message || 'Erro ao realizar cadastro');
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <div className={styles.header}>
          <h2>Criar Conta</h2>
          <p>Preencha seus dados para se registrar</p>
        </div>

        {error && <div className={styles.alertError}>{error}</div>}
        {message && <div className={styles.alertSuccess}>{message}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="Nome completo"
            />
          </div>

          <div className={styles.formGroup}>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="Telefone"
            />
          </div>

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
              placeholder="Senha (mínimo 6 caracteres)"
              minLength="6"
            />
          </div>

          <div className={styles.formGroup}>
            <input
              type="text"
              name="address"
              value={formData.address}
              onChange={handleChange}
              required
              className={styles.input}
              placeholder="Endereço completo"
            />
          </div>

          <div className={styles.formGroup}>
            <select
              name="typeUser"
              value={formData.typeUser}
              onChange={handleChange}
              className={styles.select}
            >
              <option value="Dono">Dono</option>
              <option value="Contratante">Contratante</option>
              <option value="Ambos">Ambos</option>
            </select>
          </div>

          <button type="submit" className={styles.submitButton}>
            Cadastrar
          </button>
        </form>

        <div className={styles.footer}>
          Já possui uma conta? <Link to="/login" className={styles.link}>Faça login</Link>
        </div>
      </div>
    </div>
  );
};

export default RegisterForm;