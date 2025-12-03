import React from 'react';
import { useAuth } from '@site/src/contexts/AuthContext';
import { User, LogIn } from 'lucide-react';
import styles from './NavbarAuth.module.css';

export default function NavbarAuth() {
  const { user, openAuthModal, isLoading } = useAuth();

  if (isLoading) {
    return (
      <button className={styles.authButton} disabled>
        Loading...
      </button>
    );
  }

  return (
    <button
      className={styles.authButton}
      onClick={openAuthModal}
      title={user ? 'View profile' : 'Sign in or create account'}
    >
      {user ? (
        <>
          <User size={16} />
          <span>{user.name || user.email.split('@')[0]}</span>
        </>
      ) : (
        <>
          <LogIn size={16} />
          <span>Sign In</span>
        </>
      )}
    </button>
  );
}

