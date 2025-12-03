/**
 * MessageList - Displays chat messages with citations
 */

import React from 'react';
import { ChatMessage } from '../types/ChatMessage';
import { MessageBubble } from './MessageBubble';
import '../styles/MessageList.css';

interface MessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  selectedText: string;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isLoading,
  error,
  selectedText,
}) => {
  return (
    <div className="message-list">
      {messages.length === 0 && !isLoading && (
        <div className="message-list__empty">
          <p className="message-list__welcome">
            Welcome to the RAG Chatbot! 👋
          </p>
          <p className="message-list__hint">
            {selectedText
              ? `Ask a question about: "${selectedText.substring(0, 50)}..."`
              : 'Select text or ask a question about the textbook content'}
          </p>
        </div>
      )}

      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {error && (
        <div className="message-list__error">
          <span className="message-list__error-icon">⚠️</span>
          <p>{error}</p>
        </div>
      )}

      {isLoading && (
        <div className="message-list__loading">
          <div className="message-list__loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <p>Thinking...</p>
        </div>
      )}
    </div>
  );
};

export default MessageList;
