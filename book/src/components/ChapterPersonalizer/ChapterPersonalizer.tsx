import React, { useState, useEffect } from 'react';
import PersonalizeButton from '../PersonalizeButton/PersonalizeButton';
import styles from './ChapterPersonalizer.module.css';

interface ChapterPersonalizerProps {
  children: React.ReactNode;
}

export default function ChapterPersonalizer({ children }: ChapterPersonalizerProps) {
  const [chapterTitle, setChapterTitle] = useState('');
  const [chapterContent, setChapterContent] = useState('');
  const [personalizedContent, setPersonalizedContent] = useState<string | null>(null);
  const [showPersonalized, setShowPersonalized] = useState(false);

  useEffect(() => {
    // Extract chapter title from the first h1 element
    const h1Element = document.querySelector('article h1');
    if (h1Element) {
      setChapterTitle(h1Element.textContent || '');
    }

    // Extract chapter content (simplified - gets text content)
    const articleElement = document.querySelector('article');
    if (articleElement) {
      setChapterContent(articleElement.textContent || '');
    }
  }, []);

  const handlePersonalizedContent = (content: string) => {
    setPersonalizedContent(content);
    setShowPersonalized(true);
  };

  const toggleView = () => {
    setShowPersonalized(!showPersonalized);
  };

  return (
    <div className={styles.wrapper}>
      <PersonalizeButton
        chapterTitle={chapterTitle}
        chapterContent={chapterContent}
        onPersonalizedContent={handlePersonalizedContent}
      />

      {personalizedContent && (
        <div className={styles.viewToggle}>
          <button
            className={`${styles.toggleBtn} ${!showPersonalized ? styles.active : ''}`}
            onClick={() => setShowPersonalized(false)}
          >
            Original Content
          </button>
          <button
            className={`${styles.toggleBtn} ${showPersonalized ? styles.active : ''}`}
            onClick={() => setShowPersonalized(true)}
          >
            Personalized Content
          </button>
        </div>
      )}

      {showPersonalized && personalizedContent ? (
        <div className={styles.personalizedContent}>
          <div className={styles.badge}>
            ✨ Personalized for You
          </div>
          <div 
            className={styles.content}
            dangerouslySetInnerHTML={{ __html: personalizedContent }}
          />
        </div>
      ) : (
        <div className={styles.originalContent}>
          {children}
        </div>
      )}
    </div>
  );
}
