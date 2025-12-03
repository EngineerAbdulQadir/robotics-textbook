/**
 * Header - Chat widget header with controls
 */

import React, { useState } from 'react';
import '../styles/Header.css';

interface HeaderProps {
  isOpen: boolean;
  onToggle: () => void;
  onClearHistory: () => void;
  onNewSession: () => void;
  sessionId?: string;
}

export const Header: React.FC<HeaderProps> = ({
  isOpen,
  onToggle,
  onClearHistory,
  onNewSession,
  sessionId,
}) => {
  const [showMenu, setShowMenu] = useState(false);

  const handleClearHistory = () => {
    if (
      window.confirm(
        'Are you sure you want to clear the conversation history?'
      )
    ) {
      onClearHistory();
      setShowMenu(false);
    }
  };

  const handleNewSession = () => {
    if (window.confirm('Start a new conversation?')) {
      onNewSession();
      setShowMenu(false);
    }
  };

  return (
    <div className="chat-header">
      <div className="chat-header__title">
        <span className="chat-header__icon">🤖</span>
        <h1 className="chat-header__text">Textbook Assistant</h1>
      </div>

      <div className="chat-header__controls">
        {isOpen && (
          <div className="chat-header__menu">
            <button
              className="chat-header__menu-button"
              onClick={() => setShowMenu(!showMenu)}
              title="Menu"
            >
              ⋮
            </button>

            {showMenu && (
              <div className="chat-header__dropdown">
                <button
                  className="chat-header__dropdown-item"
                  onClick={handleClearHistory}
                >
                  🗑️ Clear History
                </button>
                <button
                  className="chat-header__dropdown-item"
                  onClick={handleNewSession}
                >
                  ↻ New Session
                </button>
                {sessionId && (
                  <div className="chat-header__session-id">
                    ID: {sessionId.substring(0, 8)}...
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        <button
          className={[
            'chat-header__toggle',
            isOpen ? 'chat-header__toggle--open' : 'chat-header__toggle--closed',
          ].join(' ')}
          onClick={onToggle}
          title={isOpen ? 'Close chat' : 'Open chat'}
        >
          {isOpen ? '−' : '+'}
        </button>
      </div>
    </div>
  );
};

export default Header;
