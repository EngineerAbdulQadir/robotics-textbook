/**
 * Tests for ChatAPI service
 */

import { ChatAPI } from '../../services/ChatAPI';

describe('ChatAPI Service', () => {
  let chatAPI: ChatAPI;
  const baseUrl = 'http://localhost:8000';

  beforeEach(() => {
    chatAPI = new ChatAPI(baseUrl);
    (global.fetch as jest.Mock).mockClear();
  });

  describe('query method', () => {
    test('sends query request successfully', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({
          answer: 'Test answer',
          sources: [],
          session_id: 'test-session',
          message_id: 'msg-1',
          confidence: 0.85,
        }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      const result = await chatAPI.query('What is AI?', 'test-session', 'Chapter 1');

      expect(global.fetch).toHaveBeenCalledWith(
        `${baseUrl}/api/v1/chat/query`,
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question: 'What is AI?',
            session_id: 'test-session',
            page_context: 'Chapter 1',
          }),
        })
      );

      expect(result.answer).toBe('Test answer');
      expect(result.confidence).toBe(0.85);
    });

    test('handles query API errors', async () => {
      const mockResponse = {
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Server error' }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      await expect(
        chatAPI.query('What is AI?', 'test-session')
      ).rejects.toThrow('API error: 500');
    });

    test('handles rate limiting (429)', async () => {
      const mockResponse = {
        ok: false,
        status: 429,
        headers: new Map([['Retry-After', '60']]),
        json: async () => ({ detail: 'Rate limited' }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      await expect(
        chatAPI.query('What is AI?', 'test-session')
      ).rejects.toThrow('Rate limited. Please try again in 60 seconds.');
    });

    test('handles rate limiting with default retry', async () => {
      const mockResponse = {
        ok: false,
        status: 429,
        headers: new Map(),
        json: async () => ({ detail: 'Rate limited' }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      await expect(
        chatAPI.query('What is AI?', 'test-session')
      ).rejects.toThrow('Rate limited. Please try again in 60 seconds.');
    });

    test('handles network errors', async () => {
      (global.fetch as jest.Mock).mockRejectedValue(
        new Error('Network error')
      );

      await expect(
        chatAPI.query('What is AI?', 'test-session')
      ).rejects.toThrow('Network error');
    });
  });

  describe('querySelection method', () => {
    test('sends selection query request successfully', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({
          answer: 'Selected text explanation',
          sources: [],
          session_id: 'test-session',
          message_id: 'msg-2',
          confidence: 0.90,
        }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      const result = await chatAPI.querySelection(
        'Neural networks',
        'How do they work?',
        'test-session',
        'Chapter 5',
        'Neural Networks'
      );

      expect(global.fetch).toHaveBeenCalledWith(
        `${baseUrl}/api/v1/chat/selection`,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            selected_text: 'Neural networks',
            question: 'How do they work?',
            session_id: 'test-session',
            chapter: 'Chapter 5',
            section: 'Neural Networks',
          }),
        })
      );

      expect(result.answer).toBe('Selected text explanation');
    });

    test('handles selection API errors', async () => {
      const mockResponse = {
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Invalid request' }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      await expect(
        chatAPI.querySelection(
          'text',
          'question',
          'session-id',
          'chapter'
        )
      ).rejects.toThrow();
    });

    test('handles selection rate limiting (429)', async () => {
      const mockResponse = {
        ok: false,
        status: 429,
        headers: new Map([['Retry-After', '45']]),
        json: async () => ({ detail: 'Rate limited' }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      await expect(
        chatAPI.querySelection(
          'text',
          'question',
          'session-id',
          'chapter'
        )
      ).rejects.toThrow('Rate limited. Please try again in 45 seconds.');
    });
  });

  describe('getHistory method', () => {
    test('fetches conversation history', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({
          messages: [
            { id: 'msg-1', role: 'user', content: 'Hello' },
            { id: 'msg-2', role: 'assistant', content: 'Hi there' },
          ],
        }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      const result = await chatAPI.getHistory('test-session');

      expect(global.fetch).toHaveBeenCalledWith(
        `${baseUrl}/api/v1/chat/history?session_id=test-session`,
        expect.any(Object)
      );

      expect(result.messages).toHaveLength(2);
    });

    test('handles history fetch errors', async () => {
      const mockResponse = {
        ok: false,
        status: 404,
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      await expect(
        chatAPI.getHistory('invalid-session')
      ).rejects.toThrow();
    });
  });

  describe('health method', () => {
    test('checks API health status', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({
          status: 'ok',
          version: '0.1.0',
          qdrant_status: 'healthy',
          gemini_status: 'healthy',
        }),
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      const result = await chatAPI.health();

      expect(global.fetch).toHaveBeenCalledWith(
        `${baseUrl}/api/v1/health`,
        expect.any(Object)
      );

      expect(result.status).toBe('ok');
    });

    test('handles health check errors', async () => {
      const mockResponse = {
        ok: false,
        status: 503,
      };

      (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

      await expect(chatAPI.health()).rejects.toThrow();
    });
  });
});

describe('ChatAPI Error Messages', () => {
  let chatAPI: ChatAPI;

  beforeEach(() => {
    chatAPI = new ChatAPI('http://localhost:8000');
    (global.fetch as jest.Mock).mockClear();
  });

  test('provides user-friendly rate limit message with retry time', async () => {
    const mockResponse = {
      ok: false,
      status: 429,
      headers: new Map([['Retry-After', '30']]),
      json: async () => ({ detail: 'Rate limited' }),
    };

    (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

    try {
      await chatAPI.query('test', 'session');
    } catch (error: any) {
      expect(error.message).toContain('30 seconds');
      expect(error.message).toContain('Rate limited');
    }
  });

  test('provides descriptive error for other failures', async () => {
    const mockResponse = {
      ok: false,
      status: 500,
      json: async () => ({ detail: 'Internal server error' }),
    };

    (global.fetch as jest.Mock).mockResolvedValue(mockResponse);

    try {
      await chatAPI.query('test', 'session');
    } catch (error: any) {
      expect(error.message).toContain('API error');
    }
  });
});
