/**
 * LoadingIndicator - Shows loading state while waiting for response
 */

import React from 'react';
import '../styles/LoadingIndicator.css';

export const LoadingIndicator: React.FC = () => {
  return (
    <div className="loading-indicator">
      <div className="loading-indicator__spinner">
        <div className="loading-indicator__dot"></div>
        <div className="loading-indicator__dot"></div>
        <div className="loading-indicator__dot"></div>
      </div>
      <p className="loading-indicator__text">Thinking...</p>
    </div>
  );
};

export default LoadingIndicator;
