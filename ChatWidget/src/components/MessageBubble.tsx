/**
 * MessageBubble - Individual chat message with citations
 */

import React, { useState } from 'react';
import { ChatMessage } from '../types/ChatMessage';
import { CitationList } from './CitationList';
import '../styles/MessageBubble.css';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const [showSources, setShowSources] = useState(false);

  const bubbleClass = [
    'message-bubble',
    `message-bubble--${message.type}`,
  ].join(' ');

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
    }).format(date);
  };

  return (
    <div className={bubbleClass}>
      <div className="message-bubble__content">
        <p className="message-bubble__text">{message.content}</p>

        {message.sources && message.sources.length > 0 && (
          <div className="message-bubble__sources">
            <button
              className="message-bubble__sources-toggle"
              onClick={() => setShowSources(!showSources)}
              title={`${message.sources.length} source(s)`}
            >
              📚 {message.sources.length} source{message.sources.length !== 1 ? 's' : ''}
              {message.confidence !== undefined && (
                <span className="message-bubble__confidence">
                  {Math.round(message.confidence * 100)}% confidence
                </span>
              )}
            </button>

            {showSources && (
              <CitationList citations={message.sources} />
            )}
          </div>
        )}
      </div>

      <span className="message-bubble__time">
        {formatTime(message.timestamp)}
      </span>
    </div>
  );
};

export default MessageBubble;
