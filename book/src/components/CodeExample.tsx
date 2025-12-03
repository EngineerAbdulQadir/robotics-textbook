import React, { useState } from 'react';
import styles from './CodeExample.module.css';

interface CodeExampleProps {
  title: string;
  concept: string;
  language: 'python' | 'cpp';
  code: string;
  explanation?: string;
  runCommand?: string;
  expectedOutput?: string;
  difficulty?: 'beginner' | 'intermediate' | 'advanced';
}

/**
 * CodeExample Component
 *
 * Displays ROS 2 code examples with syntax highlighting, explanation,
 * and execution instructions for educational purposes.
 *
 * @param props - CodeExample properties
 * @returns React component
 */
export default function CodeExample({
  title,
  concept,
  language,
  code,
  explanation,
  runCommand,
  expectedOutput,
  difficulty = 'beginner',
}: CodeExampleProps): JSX.Element {
  const [showOutput, setShowOutput] = useState(false);

  const difficultyColors = {
    beginner: '#28a745',
    intermediate: '#ffc107',
    advanced: '#dc3545',
  };

  return (
    <div className={styles.codeExample}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h3 className={styles.title}>{title}</h3>
          <span
            className={styles.difficulty}
            style={{ backgroundColor: difficultyColors[difficulty] }}
          >
            {difficulty}
          </span>
        </div>
        <p className={styles.concept}>
          <strong>Concept:</strong> {concept}
        </p>
      </div>

      <div className={styles.codeBlock}>
        <pre>
          <code className={`language-${language}`}>
            {code}
          </code>
        </pre>
      </div>

      {explanation && (
        <div className={styles.explanation}>
          <h4>💡 Explanation</h4>
          <p>{explanation}</p>
        </div>
      )}

      {runCommand && (
        <div className={styles.runSection}>
          <h4>🚀 Run This Example</h4>
          <div className={styles.command}>
            <code>{runCommand}</code>
            <button
              className={styles.copyBtn}
              onClick={() => navigator.clipboard.writeText(runCommand)}
              title="Copy to clipboard"
            >
              📋
            </button>
          </div>
        </div>
      )}

      {expectedOutput && (
        <div className={styles.outputSection}>
          <button
            className={styles.outputToggle}
            onClick={() => setShowOutput(!showOutput)}
          >
            {showOutput ? '▼' : '▶'} Expected Output
          </button>
          {showOutput && (
            <pre className={styles.output}>
              <code>{expectedOutput}</code>
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
