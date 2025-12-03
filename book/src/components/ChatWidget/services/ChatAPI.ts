/**
 * ChatAPI - Handles communication with the FastAPI backend
 */

import { Citation } from '../types/ChatMessage';

export interface QueryResponse {
  answer: string;
  sources: Citation[];
  session_id: string;
  message_id: string;
  confidence: number;
}

export class ChatAPI {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async query(question: string, sessionId: string, pageContext?: string): Promise<QueryResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/chat/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        session_id: sessionId,
        page_context: pageContext,
      }),
    });

    if (!response.ok) {
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After') || '60';
        throw new Error(`Rate limited. Please try again in ${retryAfter} seconds.`);
      }
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API error: ${response.status}`);
    }
    return response.json();
  }

  async querySelection(
    selectedText: string,
    question: string,
    sessionId: string,
    chapter: string,
    section?: string
  ): Promise<QueryResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/chat/selection`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        selected_text: selectedText,
        question,
        session_id: sessionId,
        chapter,
        section: section || '',
      }),
    });

    if (!response.ok) {
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After') || '60';
        throw new Error(`Rate limited. Please try again in ${retryAfter} seconds.`);
      }
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API error: ${response.status}`);
    }
    return response.json();
  }

  async health(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/api/v1/health`);
    if (!response.ok) throw new Error(`Health check failed: ${response.status}`);
    return response.json();
  }
}
