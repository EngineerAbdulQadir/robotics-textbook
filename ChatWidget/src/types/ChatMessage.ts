/**
 * Chat message type definitions
 */

export interface Citation {
  id: string;
  chapter: string;
  section: string;
  content_excerpt: string;
  link?: string;
  confidence_score: number;
}

export type MessageType = 'user' | 'assistant' | 'error' | 'system';

export interface ChatMessage {
  id: string;
  type: MessageType;
  content: string;
  sources?: Citation[];
  confidence?: number;
  timestamp: Date;
  selectedText?: string;
}
