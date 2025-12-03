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

  /**
   * Send a general question about textbook content
   */
  async query(
    question: string,
    sessionId: string,
    pageContext?: string
  ): Promise<QueryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/chat/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          session_id: sessionId,
          page_context: pageContext,
        }),
      });

      if (!response.ok) {
        const error = await response.json();

        // Handle rate limiting (429)
        if (response.status === 429) {
          const retryAfter = response.headers.get('Retry-After') || '60';
          throw new Error(`Rate limited. Please try again in ${retryAfter} seconds.`);
        }

        throw new Error(error.detail || `API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Query API error:', error);
      throw error;
    }
  }

  /**
   * Send a question about selected text
   */
  async querySelection(
    selectedText: string,
    question: string,
    sessionId: string,
    chapter: string,
    section?: string
  ): Promise<QueryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/chat/selection`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          selected_text: selectedText,
          question,
          session_id: sessionId,
          chapter,
          section: section || '',
        }),
      });

      if (!response.ok) {
        const error = await response.json();

        // Handle rate limiting (429)
        if (response.status === 429) {
          const retryAfter = response.headers.get('Retry-After') || '60';
          throw new Error(`Rate limited. Please try again in ${retryAfter} seconds.`);
        }

        throw new Error(error.detail || `API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Selection query API error:', error);
      throw error;
    }
  }

  /**
   * Get conversation history (for future implementation)
   */
  async getHistory(sessionId: string): Promise<any> {
    try {
      const response = await fetch(
        `${this.baseUrl}/api/v1/chat/history?session_id=${sessionId}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to fetch history: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('History API error:', error);
      throw error;
    }
  }

  /**
   * Check API health
   */
  async health(): Promise<{
    status: string;
    version: string;
    qdrant_status: string;
    gemini_status: string;
  }> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }
}
