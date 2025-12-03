/**
 * SessionManager - Handles session management and local storage
 */

import { ChatSession } from '../types/ChatSession';
import { ChatMessage } from '../types/ChatMessage';

const SESSION_KEY = 'rag_chatbot_session';
const HISTORY_KEY = 'rag_chatbot_history';
const SESSION_EXPIRY_DAYS = 30;

// Simple UUID generator (no external dependency)
function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export class SessionManager {
  getSession(): ChatSession | null {
    if (typeof window === 'undefined') return null;
    try {
      const stored = localStorage.getItem(SESSION_KEY);
      if (!stored) return null;

      const session = JSON.parse(stored) as ChatSession;
      if (new Date(session.expires_at) < new Date()) {
        localStorage.removeItem(SESSION_KEY);
        localStorage.removeItem(HISTORY_KEY);
        return null;
      }
      return session;
    } catch {
      return null;
    }
  }

  createSession(pageContext?: string): ChatSession {
    const now = new Date();
    const expiresAt = new Date(now.getTime() + SESSION_EXPIRY_DAYS * 24 * 60 * 60 * 1000);

    const session: ChatSession = {
      id: generateUUID(),
      anonymous_browser_id: this.getOrCreateBrowserId(),
      created_at: now,
      expires_at: expiresAt,
      page_context: pageContext,
    };

    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(SESSION_KEY, JSON.stringify(session));
      } catch {}
    }
    return session;
  }

  private getOrCreateBrowserId(): string {
    if (typeof window === 'undefined') return generateUUID();
    const key = 'rag_chatbot_browser_id';
    try {
      let browserId = localStorage.getItem(key);
      if (!browserId) {
        browserId = generateUUID();
        localStorage.setItem(key, browserId);
      }
      return browserId;
    } catch {
      return generateUUID();
    }
  }

  saveConversation(messages: ChatMessage[]): void {
    if (typeof window === 'undefined') return;
    try {
      const serialized = messages.map((msg) => ({
        ...msg,
        timestamp: msg.timestamp.toISOString(),
      }));
      localStorage.setItem(HISTORY_KEY, JSON.stringify(serialized));
    } catch {}
  }

  getConversationHistory(): ChatMessage[] | null {
    if (typeof window === 'undefined') return null;
    try {
      const stored = localStorage.getItem(HISTORY_KEY);
      if (!stored) return null;
      const messages = JSON.parse(stored);
      return messages.map((msg: any) => ({
        ...msg,
        timestamp: new Date(msg.timestamp),
      }));
    } catch {
      return null;
    }
  }

  clearConversation(): void {
    if (typeof window === 'undefined') return;
    try {
      localStorage.removeItem(HISTORY_KEY);
    } catch {}
  }

  deleteSession(): void {
    if (typeof window === 'undefined') return;
    try {
      localStorage.removeItem(SESSION_KEY);
      localStorage.removeItem(HISTORY_KEY);
    } catch {}
  }
}
