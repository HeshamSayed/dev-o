import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import UsageIndicator from '../components/UsageIndicator';
import UpgradeModal from '../components/UpgradeModal';
import MessageRenderer from '../components/Chat/MessageRenderer';
import ConversationSidebar from '../components/Chat/ConversationSidebar';
import ThinkingDisplay from '../components/Chat/ThinkingDisplay';
import { chatApi, Conversation } from '../api/chat';
import userApi from '../api/user';
import { ChatMessage, WSMessage } from '../types';
import './ChatPage.css';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

export default function ChatPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingConversations, setLoadingConversations] = useState(true);
  const [wsConnected, setWsConnected] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [limitInfo, setLimitInfo] = useState<{ used: number; limit: number; minutesUntilReset: number } | null>(null);
  const [thinkingMode, setThinkingMode] = useState(false);
  const [currentThinking, setCurrentThinking] = useState<string>('');
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    connectWebSocket();
    loadConversations();
    loadUserPreferences();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const loadUserPreferences = async () => {
    try {
      const response = await userApi.getMe();
      if (response.data.profile?.show_thinking !== undefined) {
        setThinkingMode(response.data.profile.show_thinking);
      }
    } catch (error) {
      console.error('Error loading user preferences:', error);
    }
  };

  const handleThinkingModeToggle = async (enabled: boolean) => {
    setThinkingMode(enabled);
    // Save preference to backend
    try {
      await userApi.updateProfile({ show_thinking: enabled });
    } catch (error) {
      console.error('Error saving thinking mode preference:', error);
      // Revert on error
      setThinkingMode(!enabled);
    }
  };

  const loadConversations = async () => {
    try {
      setLoadingConversations(true);
      const response = await chatApi.getConversations();
      // Handle paginated response from DRF
      const responseData: any = response.data;
      const data = responseData.results || responseData;
      setConversations(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading conversations:', error);
      setConversations([]);
    } finally {
      setLoadingConversations(false);
    }
  };

  const loadConversation = async (id: string) => {
    try {
      setLoading(true);
      const response = await chatApi.getConversation(id);
      setActiveConversationId(id);
      setMessages(response.data.messages.map(msg => ({
        role: msg.role,
        content: msg.content,
      })));
    } catch (error) {
      console.error('Error loading conversation:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = async () => {
    try {
      const response = await chatApi.createConversation();
      const newConversation = response.data;

      // Add to conversations list and set as active
      setConversations(prev => [newConversation, ...prev]);
      setActiveConversationId(newConversation.id);

      // Clear messages and input for fresh start
      setMessages([]);
      setInput('');

      // Focus on the input field
      setTimeout(() => {
        textareaRef.current?.focus();
      }, 100);
    } catch (error) {
      console.error('Error creating conversation:', error);
    }
  };

  const handleDeleteConversation = async (id: string) => {
    try {
      await chatApi.deleteConversation(id);
      setConversations(prev => prev.filter(c => c.id !== id));
      if (activeConversationId === id) {
        setActiveConversationId(null);
        setMessages([]);
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const connectWebSocket = () => {
    const token = localStorage.getItem('access_token');
    const ws = new WebSocket(`${WS_URL}/ws/chat/?token=${token}`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setWsConnected(true);
    };

    ws.onmessage = (event) => {
      const data: WSMessage = JSON.parse(event.data);
      handleWebSocketMessage(data);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setWsConnected(false);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setWsConnected(false);
      // Reconnect after 3 seconds
      setTimeout(connectWebSocket, 3000);
    };

    wsRef.current = ws;
  };

  const handleWebSocketMessage = (data: WSMessage) => {
    switch (data.type) {
      case 'connected':
        break;
      case 'thinking_start':
        setCurrentThinking('');
        break;
      case 'thinking':
        setCurrentThinking(prev => prev + (data.content || ''));
        break;
      case 'thinking_end':
        // Store the complete thinking in the last assistant message
        if (currentThinking) {
          setMessages(prev => {
            const lastIdx = prev.length - 1;
            const lastMsg = prev[lastIdx];
            if (lastMsg && lastMsg.role === 'assistant') {
              return [...prev.slice(0, lastIdx), { ...lastMsg, thinking: currentThinking }];
            }
            return prev;
          });
        }
        setCurrentThinking('');
        break;
      case 'token':
        setLoading(false);
        setMessages(prev => {
          const lastIdx = prev.length - 1;
          const lastMsg = prev[lastIdx];
          if (lastMsg && lastMsg.role === 'assistant') {
            return [...prev.slice(0, lastIdx), { ...lastMsg, content: lastMsg.content + data.content }];
          }
          return [...prev, { role: 'assistant', content: data.content || '', thinking: currentThinking || undefined }];
        });
        break;
      case 'done':
        setLoading(false);
        setCurrentThinking('');
        break;
      case 'limit_exceeded':
        setLoading(false);
        setLimitInfo({
          used: data.used || 0,
          limit: data.limit || 0,
          minutesUntilReset: data.window_info?.minutes_until_reset || 0,
        });
        setShowUpgradeModal(true);
        break;
      case 'error':
        setLoading(false);
        setCurrentThinking('');
        setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${data.error}` }]);
        break;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading || !wsConnected) return;

    // Create new conversation if none is active
    let conversationId = activeConversationId;
    if (!conversationId) {
      try {
        const response = await chatApi.createConversation();
        conversationId = response.data.id;
        setActiveConversationId(conversationId);
        setConversations(prev => [response.data, ...prev]);
      } catch (error) {
        console.error('Error creating conversation:', error);
        return;
      }
    }

    const userMessage: ChatMessage = {
      role: 'user',
      content: input.trim(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    wsRef.current?.send(JSON.stringify({
      type: 'chat_message',
      message: input.trim(),
      conversation_id: conversationId,
      thinking_mode: thinkingMode,
    }));
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-page">
      <ConversationSidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={loadConversation}
        onNewChat={handleNewChat}
        onDeleteConversation={handleDeleteConversation}
        loading={loadingConversations}
      />
      <div className="chat-main">
        <header className="chat-header">
        <div className="chat-header-left">
          {wsConnected ? (
            <span className="connection-status connected">🟢 Connected</span>
          ) : (
            <span className="connection-status disconnected">🔴 Disconnected</span>
          )}
        </div>

        <div className="chat-header-center">
          <UsageIndicator compact />
        </div>

        <div className="chat-header-right">
          <button className="nav-btn" onClick={() => navigate('/pricing')}>
            Pricing
          </button>
          <button className="nav-btn" onClick={() => navigate('/referrals')}>
            Referrals
          </button>
          <button className="nav-btn" onClick={() => navigate('/projects')}>
            Projects
          </button>
          <div className="user-menu">
            <button className="user-menu-button" onClick={() => setShowMenu(!showMenu)}>
              <div className="user-avatar">
                {user?.email?.[0].toUpperCase() || 'U'}
              </div>
              <span className="user-email">{user?.email}</span>
            </button>

            {showMenu && (
              <div className="user-menu-dropdown">
                <button className="menu-item" onClick={logout}>
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <h2 className="empty-title">How can I help you build today?</h2>
            <p className="empty-subtitle">Start a conversation or create a new project</p>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div key={index} className={`message message-${message.role}`}>
                <div className="message-avatar">
                  {message.role === 'user' ? (
                    <div className="avatar-user">
                      {user?.email?.[0].toUpperCase() || 'U'}
                    </div>
                  ) : (
                    <div className="avatar-assistant">AI</div>
                  )}
                </div>
                <div className="message-content">
                  <div className="message-role">
                    {message.role === 'user' ? 'You' : 'DEV-O'}
                  </div>
                  {message.role === 'assistant' && thinkingMode && message.thinking && (
                    <ThinkingDisplay thinking={message.thinking} />
                  )}
                  <div className="message-text">
                    {message.role === 'assistant' ? (
                      <MessageRenderer content={message.content} />
                    ) : (
                      message.content
                    )}
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="message message-assistant">
                <div className="message-avatar">
                  <div className="avatar-assistant">D-O</div>
                </div>
                <div className="message-content">
                  <div className="message-role">DEV-O</div>
                  {thinkingMode && currentThinking && (
                    <ThinkingDisplay thinking={currentThinking} isLoading={true} />
                  )}
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <div className="chat-input-container">
        <form onSubmit={handleSubmit} className="chat-input-form">
          <div className="input-thinking-toggle">
            <button
              type="button"
              className={`thinking-toggle-button ${thinkingMode ? 'active' : ''}`}
              onClick={() => handleThinkingModeToggle(!thinkingMode)}
              title={thinkingMode ? 'Disable thinking mode' : 'Enable thinking mode'}
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" strokeWidth="2"/>
                <path d="M12 6v6l4 2" strokeWidth="2" strokeLinecap="round"/>
                <circle cx="12" cy="7" r="1" fill="currentColor"/>
                <circle cx="17" cy="12" r="1" fill="currentColor"/>
                <circle cx="7" cy="12" r="1" fill="currentColor"/>
                <circle cx="12" cy="17" r="1" fill="currentColor"/>
              </svg>
              <span className="toggle-indicator"></span>
            </button>
          </div>
          <textarea
            ref={textareaRef}
            className="chat-input"
            placeholder={thinkingMode ? "Message AI (Thinking mode ON)..." : "Message AI..."}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            rows={1}
            disabled={loading || !wsConnected}
          />
          <button
            type="submit"
            className="chat-send-button"
            disabled={!input.trim() || loading || !wsConnected}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M22 2L11 13" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M22 2L15 22L11 13L2 9L22 2Z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </form>
      </div>

        {limitInfo && (
          <UpgradeModal
            isOpen={showUpgradeModal}
            onClose={() => setShowUpgradeModal(false)}
            limitType="chat"
            used={limitInfo.used}
            limit={limitInfo.limit}
            minutesUntilReset={limitInfo.minutesUntilReset}
          />
        )}
      </div>
    </div>
  );
}
