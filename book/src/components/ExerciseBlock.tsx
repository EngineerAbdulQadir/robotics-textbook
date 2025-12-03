import React, { useState } from 'react';
import styles from './ExerciseBlock.module.css';

interface ExerciseBlockProps {
  number: number;
  title: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  taskDescription: string;
  instructions: string[];
  hints?: string[];
  solutionCode?: string;
  solutionExplanation?: string;
  validationChecklist?: string[];
  estimatedTime?: number;
  bloomLevel?: string;
}

/**
 * ExerciseBlock Component
 *
 * Displays interactive exercise cards with progressive difficulty,
 * hints, solutions, and validation checklists for hands-on learning.
 *
 * @param props - ExerciseBlock properties
 * @returns React component
 */
export default function ExerciseBlock({
  number,
  title,
  difficulty,
  taskDescription,
  instructions,
  hints,
  solutionCode,
  solutionExplanation,
  validationChecklist,
  estimatedTime,
  bloomLevel,
}: ExerciseBlockProps): JSX.Element {
  const [showHints, setShowHints] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [expandedHint, setExpandedHint] = useState<number | null>(null);

  const difficultyColors = {
    beginner: '#28a745',
    intermediate: '#ffc107',
    advanced: '#dc3545',
  };

  return (
    <div className={styles.exerciseBlock}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <h3 className={styles.title}>
            ✍️ Exercise {number}: {title}
          </h3>
          <span
            className={styles.difficulty}
            style={{ backgroundColor: difficultyColors[difficulty] }}
          >
            {difficulty}
          </span>
        </div>

        <div className={styles.metadata}>
          {estimatedTime && (
            <span className={styles.time}>⏱️ {estimatedTime} min</span>
          )}
          {bloomLevel && (
            <span className={styles.bloom}>📚 {bloomLevel}</span>
          )}
        </div>
      </div>

      <div className={styles.taskDescription}>
        <h4>📋 Task</h4>
        <p>{taskDescription}</p>
      </div>

      <div className={styles.instructions}>
        <h4>📝 Instructions</h4>
        <ol>
          {instructions.map((instruction, index) => (
            <li key={index}>{instruction}</li>
          ))}
        </ol>
      </div>

      {hints && hints.length > 0 && (
        <div className={styles.hintsSection}>
          <button
            className={styles.hintsToggle}
            onClick={() => setShowHints(!showHints)}
          >
            {showHints ? '▼' : '▶'} Hints (Need Help?)
          </button>

          {showHints && (
            <div className={styles.hints}>
              {hints.map((hint, index) => (
                <div key={index} className={styles.hint}>
                  <button
                    className={styles.hintToggle}
                    onClick={() =>
                      setExpandedHint(
                        expandedHint === index ? null : index
                      )
                    }
                  >
                    💡 Hint {index + 1}: {hint.substring(0, 50)}...
                  </button>
                  {expandedHint === index && (
                    <div className={styles.hintContent}>
                      {hint}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {validationChecklist && (
        <div className={styles.validation}>
          <h4>✅ Validation Checklist</h4>
          <ul>
            {validationChecklist.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}

      {solutionCode && (
        <div className={styles.solutionSection}>
          <button
            className={styles.solutionToggle}
            onClick={() => setShowSolution(!showSolution)}
          >
            {showSolution ? '▼' : '▶'} View Solution
          </button>

          {showSolution && (
            <div className={styles.solution}>
              {solutionCode && (
                <div className={styles.solutionCode}>
                  <p className={styles.solutionLabel}>💻 Solution Code:</p>
                  <pre>
                    <code>{solutionCode}</code>
                  </pre>
                </div>
              )}

              {solutionExplanation && (
                <div className={styles.solutionExplanation}>
                  <p className={styles.solutionLabel}>🧠 Explanation:</p>
                  <p>{solutionExplanation}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
