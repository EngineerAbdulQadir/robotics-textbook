/**
 * Chat session type definitions
 */

export interface ChatSession {
  id: string;
  anonymous_browser_id: string;
  created_at: Date;
  expires_at: Date;
  page_context?: string;
}
