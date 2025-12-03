/**
 * ChatWidget - Embedded RAG chatbot for textbook content
 *
 * Features:
 * - Real-time chat with RAG-based answers
 * - Selected text highlighting and context
 * - Message history with citations
 * - Session persistence via localStorage
 * - Responsive design for all screen sizes
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { ChatMessage } from './types/ChatMessage';
import { ChatSession } from './types/ChatSession';
import { ChatAPI } from './services/ChatAPI';
import { SessionManager } from './services/SessionManager';
import { MessageList } from './components/MessageList';
import { InputBox } from './components/InputBox';
import { Header } from './components/Header';
import { LoadingIndicator } from './components/LoadingIndicator';
import './styles/ChatWidget.css';

export interface ChatWidgetProps {
  apiUrl?: string;
  theme?: 'light' | 'dark';
  position?: 'bottom-right' | 'bottom-left';
  width?: string;
  height?: string;
  onSessionChange?: (session: ChatSession) => void;
}

// Production backend URL - Update this after deploying to Render
const PRODUCTION_API_URL = 'https://rag-chatbot-backend-0nqt.onrender.com';

export const ChatWidget: React.FC<ChatWidgetProps> = ({
  apiUrl = PRODUCTION_API_URL,
  theme = 'light',
  position = 'bottom-right',
  width = '400px',
  height = '600px',
  onSessionChange,
}) => {
  // State management
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedText, setSelectedText] = useState<string>('');
  const [session, setSession] = useState<ChatSession | null>(null);
  const [inputValue, setInputValue] = useState('');

  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatApiRef = useRef<ChatAPI | null>(null);
  const sessionManagerRef = useRef<SessionManager | null>(null);

  // Initialize services
  useEffect(() => {
    chatApiRef.current = new ChatAPI(apiUrl);
    sessionManagerRef.current = new SessionManager();

    // Load or create session
    const existingSession = sessionManagerRef.current.getSession();
    if (existingSession) {
      setSession(existingSession);
    } else {
      const newSession = sessionManagerRef.current.createSession();
      setSession(newSession);
    }

    // Load conversation history
    const savedMessages = sessionManagerRef.current.getConversationHistory();
    if (savedMessages) {
      setMessages(savedMessages);
    }

    // Listen for text selection
    document.addEventListener('mouseup', handleTextSelection);

    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, []);

  // Notify parent of session changes
  useEffect(() => {
    if (session && onSessionChange) {
      onSessionChange(session);
    }
  }, [session, onSessionChange]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle text selection from the textbook
  const handleTextSelection = useCallback(() => {
    const selected = window.getSelection()?.toString().trim();
    if (selected && selected.length > 5) {
      setSelectedText(selected);
      // Auto-open widget if text is selected
      if (!isOpen) {
        setIsOpen(true);
      }
    }
  }, [isOpen]);

  // Send message to API
  const handleSendMessage = useCallback(
    async (question: string, useSelection: boolean = false) => {
      if (!question.trim() || !session || !chatApiRef.current) {
        return;
      }

      // Clear input
      setInputValue('');
      setError(null);

      // Add user message to display
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        type: 'user',
        content: question,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMessage]);

      try {
        setIsLoading(true);

        let response;
        if (useSelection && selectedText) {
          // Use selection endpoint
          const chapter = window.location.pathname.split('/')[2] || 'Unknown';
          response = await chatApiRef.current.querySelection(
            selectedText,
            question,
            session.id,
            chapter
          );
        } else {
          // Use general query endpoint
          response = await chatApiRef.current.query(
            question,
            session.id,
            window.location.pathname
          );
        }

        // Add assistant message
        const assistantMessage: ChatMessage = {
          id: response.message_id,
          type: 'assistant',
          content: response.answer,
          sources: response.sources,
          confidence: response.confidence,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);

        // Save to local storage
        if (sessionManagerRef.current) {
          sessionManagerRef.current.saveConversation([...messages, userMessage, assistantMessage]);
        }

        setSelectedText(''); // Clear selection after use
      } catch (err) {
        const errorMsg = err instanceof Error ? err.message : 'Failed to get response';
        setError(errorMsg);

        // Add error message
        const errorMessage: ChatMessage = {
          id: `error-${Date.now()}`,
          type: 'error',
          content: errorMsg,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [session, selectedText, messages]
  );

  const handleClearHistory = useCallback(() => {
    setMessages([]);
    if (sessionManagerRef.current) {
      sessionManagerRef.current.clearConversation();
    }
  }, []);

  const handleNewSession = useCallback(() => {
    if (sessionManagerRef.current) {
      const newSession = sessionManagerRef.current.createSession();
      setSession(newSession);
      setMessages([]);
      setSelectedText('');
    }
  }, []);

  // Widget CSS classes
  const widgetClasses = [
    'chat-widget',
    `chat-widget--${theme}`,
    `chat-widget--${position}`,
    isOpen ? 'chat-widget--open' : 'chat-widget--closed',
  ].join(' ');

  return (
    <div
      className={widgetClasses}
      style={{
        width: isOpen ? width : 'auto',
        height: isOpen ? height : 'auto',
      }}
    >
      <Header
        isOpen={isOpen}
        onToggle={() => setIsOpen(!isOpen)}
        onClearHistory={handleClearHistory}
        onNewSession={handleNewSession}
        sessionId={session?.id}
      />

      {isOpen && (
        <div className="chat-widget__body">
          <MessageList
            messages={messages}
            isLoading={isLoading}
            error={error}
            selectedText={selectedText}
          />

          {isLoading && <LoadingIndicator />}

          <InputBox
            value={inputValue}
            onChange={(value) => setInputValue(value)}
            onSend={(question) => handleSendMessage(question)}
            onSendWithSelection={(question) =>
              handleSendMessage(question, true)
            }
            selectedText={selectedText}
            disabled={isLoading}
          />

          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
