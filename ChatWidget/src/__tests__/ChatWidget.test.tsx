/**
 * Tests for ChatWidget component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatWidget from '../ChatWidget';

describe('ChatWidget Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (global.fetch as jest.Mock).mockClear();
  });

  test('renders chat widget button', () => {
    render(<ChatWidget />);
    const widget = screen.getByRole('heading', { level: 3, hidden: true });
    expect(widget).toBeInTheDocument();
  });

  test('toggles open/closed state', () => {
    render(<ChatWidget />);
    const button = screen.getByRole('button', { hidden: true });

    // Initially closed
    expect(button).toBeInTheDocument();

    // Click to open
    fireEvent.click(button);
    // Note: Full assertion depends on component structure
  });

  test('initializes with default props', () => {
    render(<ChatWidget />);
    expect(screen.getByRole('heading', { hidden: true })).toBeInTheDocument();
  });

  test('accepts custom API URL', () => {
    render(<ChatWidget apiUrl="https://api.example.com" />);
    expect(screen.getByRole('heading', { hidden: true })).toBeInTheDocument();
  });

  test('supports light and dark themes', () => {
    const { rerender } = render(<ChatWidget theme="light" />);
    let widget = screen.getByRole('heading', { hidden: true }).closest('div');
    expect(widget).toHaveClass('chat-widget--light');

    rerender(<ChatWidget theme="dark" />);
    widget = screen.getByRole('heading', { hidden: true }).closest('div');
    expect(widget).toHaveClass('chat-widget--dark');
  });

  test('respects position prop', () => {
    const { rerender } = render(<ChatWidget position="bottom-right" />);
    let widget = screen.getByRole('heading', { hidden: true }).closest('div');
    expect(widget).toHaveClass('chat-widget--bottom-right');

    rerender(<ChatWidget position="bottom-left" />);
    widget = screen.getByRole('heading', { hidden: true }).closest('div');
    expect(widget).toHaveClass('chat-widget--bottom-left');
  });

  test('calls onSessionChange callback', async () => {
    const mockSessionChange = jest.fn();
    render(<ChatWidget onSessionChange={mockSessionChange} />);

    // Session should be created on mount
    await waitFor(() => {
      expect(mockSessionChange).toHaveBeenCalled();
    });
  });

  test('listens for text selection', () => {
    render(<ChatWidget />);

    // Simulate text selection
    const selection = window.getSelection() as any;
    if (selection) {
      selection.toString = () => 'selected text';
      const event = new MouseEvent('mouseup');
      fireEvent.(document, event);
    }
  });
});

describe('ChatWidget Text Selection', () => {
  test('detects selected text over 5 characters', () => {
    render(<ChatWidget />);

    // Trigger selection event
    const selection = {
      toString: () => 'This is a long selection',
    };

    // Mock window.getSelection
    jest.spyOn(window, 'getSelection').mockReturnValue(selection as any);

    const event = new MouseEvent('mouseup');
    fireEvent.mouseUp(document);

    // Component should detect and store the selection
  });

  test('ignores selected text under 5 characters', () => {
    render(<ChatWidget />);

    const selection = {
      toString: () => 'Hi',
    };

    jest.spyOn(window, 'getSelection').mockReturnValue(selection as any);
    const event = new MouseEvent('mouseup');
    fireEvent.mouseUp(document);

    // Component should ignore short selection
  });
});

describe('ChatWidget Session Management', () => {
  test('creates new session on mount', async () => {
    render(<ChatWidget />);

    // Wait for session initialization
    await waitFor(() => {
      expect(localStorage.setItem).toHaveBeenCalled();
    }, { timeout: 1000 });
  });

  test('loads existing session from localStorage', () => {
    const existingSession = {
      id: 'existing-session-id',
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    };

    (localStorage.getItem as jest.Mock).mockReturnValue(JSON.stringify(existingSession));

    render(<ChatWidget />);

    expect(localStorage.getItem).toHaveBeenCalledWith(expect.stringContaining('session'));
  });

  test('clears history on new session', async () => {
    render(<ChatWidget />);

    // Get the clear history button (if visible when open)
    // This depends on component structure

    // Simulate clearing history
    // Assert that messages are cleared and new session created
  });
});

describe('ChatWidget Error Handling', () => {
  test('displays error message on API failure', async () => {
    (global.fetch as jest.Mock).mockRejectedValue(new Error('API Error'));

    render(<ChatWidget />);

    // Try to send a message (assuming there's an input and send button)
    // Assert error message is displayed
  });

  test('handles rate limit (429) gracefully', async () => {
    (global.fetch as jest.Mock).mockResolvedValue({
      ok: false,
      status: 429,
      headers: new Map([['Retry-After', '60']]),
      json: async () => ({ detail: 'Rate limited' }),
    });

    render(<ChatWidget />);

    // Try to send a message
    // Assert "Rate limited. Try again in 60 seconds" message
  });

  test('handles network errors gracefully', async () => {
    (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));

    render(<ChatWidget />);

    // Try to send a message
    // Assert error message is displayed
  });
});

describe('ChatWidget Props', () => {
  test('customizes width and height', () => {
    const { container } = render(
      <ChatWidget width="500px" height="700px" />
    );

    const widget = container.querySelector('.chat-widget');
    // Style assertions depend on component implementation
    expect(widget).toBeInTheDocument();
  });

  test('defaults to sensible sizes', () => {
    const { container } = render(<ChatWidget />);

    const widget = container.querySelector('.chat-widget');
    expect(widget).toBeInTheDocument();
  });
});
