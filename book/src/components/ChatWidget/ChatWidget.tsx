/**
 * ChatWidget - Embedded RAG chatbot for Physical AI Textbook
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { MessageCircle, Bot, X, MoreVertical, Trash2, Send } from 'lucide-react';
import { ChatMessage, Citation } from './types/ChatMessage';
import { ChatSession } from './types/ChatSession';
import { ChatAPI } from './services/ChatAPI';
import { SessionManager } from './services/SessionManager';
import styles from './ChatWidget.module.css';

// Backend URL configuration
// For local development: http://localhost:8000
// For production (GitHub Pages): https://rag-chatbot-backend-production-5e31.up.railway.app
const DEV_API_URL = 'http://localhost:8000';
const PROD_API_URL = 'https://rag-chatbot-backend-production-5e31.up.railway.app';

const API_URL = typeof window !== 'undefined' 
  ? (window as any).__CHATBOT_API_URL__ || (window.location.hostname === 'localhost' ? DEV_API_URL : PROD_API_URL)
  : DEV_API_URL;

export default function ChatWidget() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [session, setSession] = useState<ChatSession | null>(null);
  const [inputValue, setInputValue] = useState('');
  const [showMenu, setShowMenu] = useState(false);
  const [showSources, setShowSources] = useState<Record<string, boolean>>({});

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatApiRef = useRef<ChatAPI | null>(null);
  const sessionManagerRef = useRef<SessionManager | null>(null);

  useEffect(() => {
    chatApiRef.current = new ChatAPI(API_URL);
    sessionManagerRef.current = new SessionManager();
    const existingSession = sessionManagerRef.current.getSession();
    if (existingSession) {
      setSession(existingSession);
    } else {
      setSession(sessionManagerRef.current.createSession());
    }
    const savedMessages = sessionManagerRef.current.getConversationHistory();
    if (savedMessages) setMessages(savedMessages);

    const handleSelection = () => {
      const selected = window.getSelection()?.toString().trim();
      if (selected && selected.length > 10) setSelectedText(selected);
    };
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = useCallback(async (question: string, useSelection = false) => {
    if (!question.trim() || !session || !chatApiRef.current) return;
    setInputValue('');

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: question,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      setIsLoading(true);
      let response;
      if (useSelection && selectedText) {
        const chapter = window.location.pathname.split('/')[2] || 'Unknown';
        response = await chatApiRef.current.querySelection(selectedText, question, session.id, chapter);
      } else {
        response = await chatApiRef.current.query(question, session.id, window.location.pathname);
      }

      const assistantMessage: ChatMessage = {
        id: response.message_id,
        type: 'assistant',
        content: response.answer,
        sources: response.sources,
        confidence: response.confidence,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
      sessionManagerRef.current?.saveConversation([...messages, userMessage, assistantMessage]);
      setSelectedText('');
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to get response';
      setMessages(prev => [...prev, { id: `error-${Date.now()}`, type: 'error', content: errorMsg, timestamp: new Date() }]);
    } finally {
      setIsLoading(false);
    }
  }, [session, selectedText, messages]);

  const handleClearHistory = () => {
    if (window.confirm('Clear conversation history?')) {
      setMessages([]);
      sessionManagerRef.current?.clearConversation();
      setShowMenu(false);
    }
  };

  const handleNewSession = () => {
    if (window.confirm('Start new conversation?')) {
      const newSession = sessionManagerRef.current?.createSession();
      if (newSession) setSession(newSession);
      setMessages([]);
      setSelectedText('');
      setShowMenu(false);
    }
  };

  const formatTime = (date: Date) => new Intl.DateTimeFormat('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }).format(date);
  const toggleSources = (id: string) => setShowSources(prev => ({ ...prev, [id]: !prev[id] }));

  if (!isOpen) {
    return (
      <div className={`${styles.chatWidget} ${styles.bottomRight} ${styles.closed}`}>
        <button className={styles.floatingBtn} onClick={() => setIsOpen(true)} title="Open Chat">
          <MessageCircle size={28} />
        </button>
      </div>
    );
  }

  return (
    <div className={`${styles.chatWidget} ${styles.bottomRight} ${styles.open}`}>
      <div className={styles.header}>
        <div className={styles.headerTitle}>
          <Bot size={20} />
          <span>Textbook Assistant</span>
        </div>
        <div className={styles.headerControls}>
          <div style={{ position: 'relative' }}>
            <button className={styles.menuBtn} onClick={() => setShowMenu(!showMenu)}>
              <MoreVertical size={16} />
            </button>
            {showMenu && (
              <div className={styles.dropdown}>
                <button className={styles.dropdownItem} onClick={handleClearHistory}>
                  <Trash2 size={14} style={{ marginRight: '8px' }} />
                  Clear History
                </button>
                <button className={styles.dropdownItem} onClick={handleNewSession}>
                  <Bot size={14} style={{ marginRight: '8px' }} />
                  New Session
                </button>
              </div>
            )}
          </div>
          <button className={styles.toggleBtn} onClick={() => setIsOpen(false)}>
            <X size={18} />
          </button>
        </div>
      </div>

      <div className={styles.body}>
        <div className={styles.messages}>
          {messages.length === 0 && !isLoading && (
            <div className={styles.emptyState}>
              <Bot size={48} style={{ color: '#2563eb', marginBottom: '1rem' }} />
              <div className={styles.emptyTitle}>Welcome!</div>
              <div className={styles.emptyHint}>{selectedText ? `Ask about: "${selectedText.substring(0, 40)}..."` : 'Ask questions about the textbook content'}</div>
            </div>
          )}

          {messages.map(msg => (
            <div key={msg.id} className={`${styles.messageBubble} ${msg.type === 'user' ? styles.userMessage : msg.type === 'error' ? styles.errorMessage : styles.assistantMessage}`}>
              <div className={styles.messageContent}>
                {msg.content}
                {msg.sources && msg.sources.length > 0 && (
                  <>
                    <button className={styles.sourcesToggle} onClick={() => toggleSources(msg.id)}>
                      📚 {msg.sources.length} source{msg.sources.length !== 1 ? 's' : ''}
                    </button>
                    {showSources[msg.id] && (
                      <div className={styles.sourcesList}>
                        {msg.sources.map((src: Citation) => (
                          <div key={src.id} className={styles.sourceItem}>
                            <span className={styles.sourceChapter}>{src.chapter}</span>
                            {src.section && <span> - {src.section}</span>}
                            <div className={styles.sourceExcerpt}>{src.content_excerpt}</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
              <div className={styles.messageTime}>{formatTime(msg.timestamp)}</div>
            </div>
          ))}

          {isLoading && (
            <div className={styles.loading}>
              <div className={styles.loadingDots}>
                <span className={styles.loadingDot}></span>
                <span className={styles.loadingDot}></span>
                <span className={styles.loadingDot}></span>
              </div>
              <span>Thinking...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className={styles.inputArea}>
          {selectedText && (
            <div className={styles.selectedTextBadge}>
              <span className={styles.selectedLabel}>Selected: </span>
              "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"
            </div>
          )}
          <div className={styles.inputWrapper}>
            <textarea
              className={styles.textarea}
              value={inputValue}
              onChange={e => setInputValue(e.target.value.slice(0, 500))}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(inputValue); } }}
              placeholder="Ask about the textbook..."
              disabled={isLoading}
              rows={1}
            />
            <div className={styles.buttons}>
              <button 
                className={styles.sendBtn} 
                onClick={() => handleSend(inputValue)} 
                disabled={isLoading || !inputValue.trim()}
                title="Send message"
              >
                <Send size={20} />
              </button>
            </div>
            <div className={styles.charCount}>{inputValue.length}/500</div>
          </div>
        </div>
      </div>
    </div>
  );
}
