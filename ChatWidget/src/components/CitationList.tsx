/**
 * CitationList - Displays sources/citations for an answer
 */

import React from 'react';
import { Citation } from '../types/ChatMessage';
import '../styles/CitationList.css';

interface CitationListProps {
  citations: Citation[];
}

export const CitationList: React.FC<CitationListProps> = ({ citations }) => {
  return (
    <div className="citation-list">
      <h4 className="citation-list__title">Sources</h4>
      <ul className="citation-list__items">
        {citations.map((citation) => (
          <li key={citation.id} className="citation-item">
            <div className="citation-item__header">
              <span className="citation-item__chapter">{citation.chapter}</span>
              {citation.section && (
                <span className="citation-item__section">{citation.section}</span>
              )}
              <span className="citation-item__confidence">
                {Math.round(citation.confidence_score * 100)}%
              </span>
            </div>
            <p className="citation-item__excerpt">
              {citation.content_excerpt}
            </p>
            {citation.link && (
              <a
                href={citation.link}
                className="citation-item__link"
                target="_blank"
                rel="noopener noreferrer"
              >
                Read more →
              </a>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CitationList;
