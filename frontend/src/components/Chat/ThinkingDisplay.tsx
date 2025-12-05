import { useState } from 'react';
import { BrainIcon } from '../Icons/PageIcons';
import './ThinkingDisplay.css';

interface ThinkingDisplayProps {
  thinking: string;
  isLoading?: boolean;
}

export default function ThinkingDisplay({ thinking, isLoading }: ThinkingDisplayProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  if (!thinking && !isLoading) return null;

  return (
    <div className={`thinking-display ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="thinking-header" onClick={() => setIsCollapsed(!isCollapsed)}>
        <div className="thinking-icon"><BrainIcon size={20} /></div>
        <span className="thinking-label">AI Thinking Process</span>
        <button className="thinking-toggle">
          {isCollapsed ? '▶' : '▼'}
        </button>
      </div>
      {!isCollapsed && (
        <div className="thinking-content">
          {isLoading && !thinking && (
            <div className="thinking-loading">
              <span className="thinking-dot"></span>
              <span className="thinking-dot"></span>
              <span className="thinking-dot"></span>
            </div>
          )}
          {thinking && (
            <pre className="thinking-text">{thinking}</pre>
          )}
        </div>
      )}
    </div>
  );
}