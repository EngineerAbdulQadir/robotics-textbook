/**
 * ChatWidget - Main export file
 */

export { ChatWidget, type ChatWidgetProps } from './ChatWidget';
export { ChatAPI } from './services/ChatAPI';
export { SessionManager } from './services/SessionManager';
export { type ChatMessage, type MessageType, type Citation } from './types/ChatMessage';
export { type ChatSession } from './types/ChatSession';

// Default export
export { default } from './ChatWidget';
