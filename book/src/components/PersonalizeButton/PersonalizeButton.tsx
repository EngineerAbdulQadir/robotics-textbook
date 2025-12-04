import React, { useState } from 'react';
import { useAuth } from '@site/src/contexts/AuthContext';
import { Sparkles, Loader2, CheckCircle, AlertCircle, Languages } from 'lucide-react';
import styles from './PersonalizeButton.module.css';

interface PersonalizeButtonProps {
  chapterTitle: string;
  chapterContent: string;
  onPersonalizedContent?: (content: string) => void;
}

// Backend API URL
const getApiUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:3001';
  return window.location.hostname === 'localhost'
    ? 'http://localhost:3001'
    : 'https://rag-chatbot-backend-production-5f64.up.railway.app';
};

export default function PersonalizeButton({ 
  chapterTitle, 
  chapterContent,
  onPersonalizedContent 
}: PersonalizeButtonProps) {
  const { user, openAuthModal } = useAuth();
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');
  const [personalizedContent, setPersonalizedContent] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [translatedContent, setTranslatedContent] = useState<string | null>(null);
  const [translating, setTranslating] = useState(false);

  const handlePersonalize = async () => {
    if (!user) {
      openAuthModal();
      return;
    }

    setLoading(true);
    setStatus('idle');
    setMessage('');

    try {
      const API_URL = getApiUrl();
      console.log('🚀 Sending personalization request to:', `${API_URL}/api/personalize-content`);
      console.log('👤 User object:', user);
      console.log('📦 Request data:', { userId: user.id, chapterTitle, contentLength: chapterContent.length });
      
      const response = await fetch(`${API_URL}/api/personalize-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          userId: user.id,
          chapterTitle,
          chapterContent: chapterContent.substring(0, 2000), // Limit content size
        }),
      });
      
      console.log('📨 Response status:', response.status);

      const data = await response.json();

      if (!response.ok) {
        // Show the actual error message from the API
        const errorMessage = data.error || 'Failed to personalize content';
        
        // Special handling for profile not found
        if (errorMessage.includes('profile not found') || response.status === 404) {
          throw new Error('Profile not found. Please sign out and create a new account to use personalization features.');
        }
        
        throw new Error(errorMessage);
      }
      
      setStatus('success');
      setMessage('Content personalized! Click "View Personalized Content" to see it.');
      setPersonalizedContent(data.personalizedContent);
      
      if (onPersonalizedContent && data.personalizedContent) {
        onPersonalizedContent(data.personalizedContent);
      }

      // Reset status after 5 seconds
      setTimeout(() => {
        setStatus('idle');
        setMessage('');
      }, 5000);

    } catch (error) {
      console.error('Personalization error:', error);
      setStatus('error');
      const errorMessage = error instanceof Error ? error.message : 'Failed to personalize content. Please try again.';
      setMessage(errorMessage);
      
      setTimeout(() => {
        setStatus('idle');
        setMessage('');
      }, 5000); // Show error for 5 seconds
    } finally {
      setLoading(false);
    }
  };

  const handleTranslate = async () => {
    if (!user) {
      openAuthModal();
      return;
    }

    setTranslating(true);
    setMessage('');

    try {
      const API_URL = getApiUrl();
      console.log('🌐 Sending translation request to Urdu...');
      
      const response = await fetch(`${API_URL}/api/translate-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          userId: user.id,
          chapterTitle,
          chapterContent: chapterContent.substring(0, 3000),
          targetLanguage: 'urdu',
        }),
      });

      console.log('📨 Translation response status:', response.status);

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to translate content');
      }
      
      setTranslatedContent(data.translatedContent);
      setMessage('Content translated to Urdu! Click "View Urdu Translation" to see it.');
      
      setTimeout(() => {
        setMessage('');
      }, 5000);

    } catch (error) {
      console.error('Translation error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Failed to translate content. Please try again.';
      setMessage(errorMessage);
      
      setTimeout(() => {
        setMessage('');
      }, 5000);
    } finally {
      setTranslating(false);
    }
  };

  return (
    <div className={styles.container}>
      <button
        className={`${styles.personalizeBtn} ${status !== 'idle' ? styles[status] : ''}`}
        onClick={handlePersonalize}
        disabled={loading}
      >
        {loading ? (
          <>
            <Loader2 size={18} className={styles.spinner} />
            Personalizing...
          </>
        ) : status === 'success' ? (
          <>
            <CheckCircle size={18} />
            Personalized!
          </>
        ) : status === 'error' ? (
          <>
            <AlertCircle size={18} />
            Try Again
          </>
        ) : (
          <>
            <Sparkles size={18} />
            {user ? 'Personalize for Me' : 'Sign In to Personalize'}
          </>
        )}
      </button>

      <button
        className={styles.translateBtn}
        onClick={handleTranslate}
        disabled={translating}
      >
        {translating ? (
          <>
            <Loader2 size={18} className={styles.spinner} />
            Translating...
          </>
        ) : (
          <>
            <Languages size={18} />
            {user ? 'Translate to Urdu' : 'Sign In to Translate'}
          </>
        )}
      </button>
      
      {message && (
        <div className={`${styles.message} ${styles[status]}`}>
          {message}
        </div>
      )}

      {user && (
        <p className={styles.hint}>
          Content will be adapted to your experience level and learning goals
        </p>
      )}

      {personalizedContent && (
        <button
          className={styles.viewBtn}
          onClick={() => setShowModal(true)}
        >
          <Sparkles size={18} />
          View Personalized Content
        </button>
      )}

      {translatedContent && (
        <button
          className={styles.viewUrduBtn}
          onClick={() => setShowModal(true)}
        >
          <Languages size={18} />
          View Urdu Translation
        </button>
      )}

      {showModal && (personalizedContent || translatedContent) && (
        <div className={styles.modal} onClick={() => setShowModal(false)}>
          <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
            <button className={styles.closeBtn} onClick={() => setShowModal(false)}>
              ×
            </button>
            <div 
              className={translatedContent ? styles.urduContent : styles.personalizedHtml}
              dangerouslySetInnerHTML={{ __html: translatedContent || personalizedContent || '' }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
