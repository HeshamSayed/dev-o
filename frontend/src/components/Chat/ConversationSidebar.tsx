import { useState } from 'react';
import { Conversation } from '../../api/chat';
import Logo from '../Logo/Logo';
import './ConversationSidebar.css';

interface ConversationSidebarProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string) => void;
  loading?: boolean;
}

export default function ConversationSidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  loading = false,
}: ConversationSidebarProps) {
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      setDeletingId(id);
      try {
        await onDeleteConversation(id);
      } finally {
        setDeletingId(null);
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  // Filter conversations based on search query
  const filteredConversations = (conversations || []).filter(conversation =>
    conversation.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="conversation-sidebar">
      <div className="sidebar-logo">
        <Logo size={140} showText={false} />
      </div>

      <div className="new-chat-container">
        <button
          className="new-chat-btn"
          onClick={onNewChat}
          disabled={loading}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 5v14M5 12h14" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span>New Chat</span>
        </button>
      </div>

      <div className="sidebar-search">
        <input
          type="text"
          className="search-input"
          placeholder="Search chats..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <svg className="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="m21 21-4.35-4.35" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>

      <div className="conversations-list">
        {loading ? (
          <div className="sidebar-loading">Loading conversations...</div>
        ) : filteredConversations.length === 0 ? (
          <div className="sidebar-empty">
            <p>{searchQuery ? 'No matching chats' : 'No conversations yet'}</p>
            <p className="sidebar-empty-hint">
              {searchQuery ? 'Try a different search term' : 'Start a new chat to begin'}
            </p>
          </div>
        ) : (
          filteredConversations.map((conversation) => (
            <div
              key={conversation.id}
              className={`conversation-item ${
                conversation.id === activeConversationId ? 'active' : ''
              } ${deletingId === conversation.id ? 'deleting' : ''}`}
              onClick={() => onSelectConversation(conversation.id)}
            >
              <div className="conversation-content">
                <div className="conversation-title">
                  {conversation.title || 'New Chat'}
                </div>
                <div className="conversation-date">
                  {formatDate(conversation.updated_at)}
                </div>
              </div>
              <button
                className="delete-conversation-button"
                onClick={(e) => handleDelete(e, conversation.id)}
                disabled={deletingId === conversation.id}
                title="Delete conversation"
              >
                {deletingId === conversation.id ? (
                  <span className="delete-spinner">⋯</span>
                ) : (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
