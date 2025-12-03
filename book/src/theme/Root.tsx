import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import AuthModal from '../components/AuthModal';
import ChatWidget from '../components/ChatWidget/ChatWidget';

export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
      <AuthModal />
      <ChatWidget />
    </AuthProvider>
  );
}
