/**
 * SessionManager - Handles session management and local storage
 */

import { ChatSession } from '../types/ChatSession';
import { ChatMessage } from '../types/ChatMessage';
import { v4 as uuidv4 } from 'uuid';

const SESSION_KEY = 'rag_chatbot_session';
const HISTORY_KEY = 'rag_chatbot_history';
const SESSION_EXPIRY_DAYS = 30;

export class SessionManager {
  /**
   * Get or create a session
   */
  getSession(): ChatSession | null {
    try {
      const stored = localStorage.getItem(SESSION_KEY);
      if (!stored) {
        return null;
      }

      const session = JSON.parse(stored) as ChatSession;

      // Check if session is expired
      if (new Date(session.expires_at) < new Date()) {
        localStorage.removeItem(SESSION_KEY);
        localStorage.removeItem(HISTORY_KEY);
        return null;
      }

      return session;
    } catch (error) {
      console.error('Error retrieving session:', error);
      return null;
    }
  }

  /**
   * Create a new session
   */
  createSession(pageContext?: string): ChatSession {
    const now = new Date();
    const expiresAt = new Date(
      now.getTime() + SESSION_EXPIRY_DAYS * 24 * 60 * 60 * 1000
    );

    const session: ChatSession = {
      id: uuidv4(),
      anonymous_browser_id: this.getOrCreateBrowserId(),
      created_at: now,
      expires_at: expiresAt,
      page_context: pageContext,
    };

    try {
      localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    } catch (error) {
      console.error('Error saving session:', error);
    }

    return session;
  }

  /**
   * Get or create a unique browser ID
   */
  private getOrCreateBrowserId(): string {
    const key = 'rag_chatbot_browser_id';

    try {
      let browserId = localStorage.getItem(key);

      if (!browserId) {
        browserId = uuidv4();
        localStorage.setItem(key, browserId);
      }

      return browserId;
    } catch (error) {
      console.error('Error managing browser ID:', error);
      return uuidv4();
    }
  }

  /**
   * Save conversation history
   */
  saveConversation(messages: ChatMessage[]): void {
    try {
      const serialized = messages.map((msg) => ({
        ...msg,
        timestamp: msg.timestamp.toISOString(),
      }));
      localStorage.setItem(HISTORY_KEY, JSON.stringify(serialized));
    } catch (error) {
      console.error('Error saving conversation:', error);
    }
  }

  /**
   * Get conversation history
   */
  getConversationHistory(): ChatMessage[] | null {
    try {
      const stored = localStorage.getItem(HISTORY_KEY);
      if (!stored) {
        return null;
      }

      const messages = JSON.parse(stored) as Array<any>;
      return messages.map((msg) => ({
        ...msg,
        timestamp: new Date(msg.timestamp),
      }));
    } catch (error) {
      console.error('Error retrieving conversation:', error);
      return null;
    }
  }

  /**
   * Clear conversation history
   */
  clearConversation(): void {
    try {
      localStorage.removeItem(HISTORY_KEY);
    } catch (error) {
      console.error('Error clearing conversation:', error);
    }
  }

  /**
   * Delete session (logout)
   */
  deleteSession(): void {
    try {
      localStorage.removeItem(SESSION_KEY);
      localStorage.removeItem(HISTORY_KEY);
    } catch (error) {
      console.error('Error deleting session:', error);
    }
  }

  /**
   * Get session expiry time remaining in seconds
   */
  getSessionTimeRemaining(): number {
    const session = this.getSession();
    if (!session) {
      return 0;
    }

    const expiresAt = new Date(session.expires_at);
    const now = new Date();
    const remaining = expiresAt.getTime() - now.getTime();

    return Math.max(0, Math.floor(remaining / 1000));
  }

  /**
   * Check if session is about to expire (within 1 hour)
   */
  isSessionExpiringSoon(): boolean {
    return this.getSessionTimeRemaining() < 3600;
  }
}
