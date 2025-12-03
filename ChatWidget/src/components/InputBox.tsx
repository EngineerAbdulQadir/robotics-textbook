/**
 * InputBox - User input field for chat messages
 */

import React, { useState } from 'react';
import '../styles/InputBox.css';

interface InputBoxProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (message: string) => void;
  onSendWithSelection: (message: string) => void;
  selectedText: string;
  disabled: boolean;
}

export const InputBox: React.FC<InputBoxProps> = ({
  value,
  onChange,
  onSend,
  onSendWithSelection,
  selectedText,
  disabled,
}) => {
  const [charCount, setCharCount] = useState(0);
  const maxChars = 500;

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    if (newValue.length <= maxChars) {
      onChange(newValue);
      setCharCount(newValue.length);
    }
  };

  const handleSend = () => {
    if (value.trim()) {
      onSend(value);
    }
  };

  const handleSendWithSelection = () => {
    if (value.trim() && selectedText) {
      onSendWithSelection(value);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="input-box">
      {selectedText && (
        <div className="input-box__selection">
          <span className="input-box__selection-label">Selected:</span>
          <span className="input-box__selection-text">
            "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"
          </span>
        </div>
      )}

      <div className="input-box__textarea-container">
        <textarea
          className="input-box__textarea"
          value={value}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the textbook..."
          disabled={disabled}
          rows={3}
          maxLength={maxChars}
        />
        <div className="input-box__char-count">
          {charCount}/{maxChars}
        </div>
      </div>

      <div className="input-box__buttons">
        <button
          className="input-box__button input-box__button--primary"
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          title="Send question (Shift+Enter for new line)"
        >
          Send
        </button>

        {selectedText && (
          <button
            className="input-box__button input-box__button--secondary"
            onClick={handleSendWithSelection}
            disabled={disabled || !value.trim()}
            title="Ask about the selected text"
          >
            About Selection
          </button>
        )}
      </div>
    </div>
  );
};

export default InputBox;
