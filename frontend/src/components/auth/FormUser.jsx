import React, { useState } from 'react';

const FormUser = ({ onUserSubmit }) => {
  const [username, setUsername] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim()) {
      onUserSubmit(username); // Envia o nome para o componente Home
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
      <input
        type="text"
        placeholder="Digite seu nome"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={{ padding: '8px', marginRight: '10px' }}
      />
      <button type="submit" style={{ padding: '8px 16px' }}>
        Enviar
      </button>
    </form>
  );
};

export default FormUser;