import React from 'react';
import LoginForm from '../components/login/LoginForm';
import AuthLayout from '../components/layout/AuthLayout';

const LoginPage = () => {
  return (
    <AuthLayout>
      <LoginForm />
    </AuthLayout>
  );
};

export default LoginPage;