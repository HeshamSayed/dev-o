import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { apiService } from '../../services/api';
import type { ChatMessage } from '../../services/api';
import Logo from '../../components/Logo/Logo';
import './Chat.css';

const Chat: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user, logout, isAuthenticated } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showMenu, setShowMenu] = useState(false);
  const [projectId, setProjectId] = useState<string | null>(null);
  const [projectLoading, setProjectLoading] = useState(true);
  const [wsConnected, setWsConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    } else {
      initializeProject();
    }
  }, [isAuthenticated, navigate]);

  // Connect to WebSocket when project is loaded
  useEffect(() => {
    if (projectId && isAuthenticated) {
      connectWebSocket();
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [projectId, isAuthenticated]);

  const initializeProject = async () => {
    try {
      setProjectLoading(true);

      // Check if project ID is in URL params
      const urlProjectId = searchParams.get('project');
      if (urlProjectId) {
        setProjectId(urlProjectId);
        setProjectLoading(false);
        return;
      }

      // Check localStorage for current project
      const storedProjectId = localStorage.getItem('current_project_id');
      if (storedProjectId) {
        setProjectId(storedProjectId);
        setProjectLoading(false);
        return;
      }

      // Try to get existing projects
      const projects = await apiService.getProjects();

      if (projects && projects.length > 0) {
        // Use the first project
        setProjectId(projects[0].id);
        localStorage.setItem('current_project_id', projects[0].id);
      } else {
        // Create a default project
        const newProject = await apiService.createProject(
          'My First Project',
          'Default project for DEV-O chat'
        );
        setProjectId(newProject.id);
        localStorage.setItem('current_project_id', newProject.id);
      }
    } catch (error) {
      console.error('Failed to initialize project:', error);
      // Set a fallback - we'll handle the error in executeTask
    } finally {
      setProjectLoading(false);
    }
  };

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  const adjustTextareaHeight = useCallback(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    }
  }, []);

  useEffect(() => {
    // Throttle scrolling - only scroll every 500ms during streaming
    const timer = setTimeout(scrollToBottom, 100);
    return () => clearTimeout(timer);
  }, [messages, scrollToBottom]);

  useEffect(() => {
    adjustTextareaHeight();
  }, [input, adjustTextareaHeight]);

  const connectWebSocket = () => {
    if (!projectId) {
      console.warn('Cannot connect WebSocket: No project ID');
      return;
    }

    const token = localStorage.getItem('access_token');
    if (!token) {
      console.error('Cannot connect WebSocket: No access token');
      return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/ws/projects/${projectId}/chat/?token=${token}`;

    console.log('[WebSocket] Connecting to:', wsUrl.replace(token, 'TOKEN_HIDDEN'));

    try {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log('[WebSocket] ✅ Connected successfully');
        setWsConnected(true);
      };

      ws.onmessage = (event) => {
        console.log('[WebSocket] 📨 Message received:', event.data.substring(0, 100));
        try {
          const data = JSON.parse(event.data);
          handleWebSocketMessage(data);
        } catch (err) {
          console.error('[WebSocket] ❌ Error parsing message:', err);
        }
      };

      ws.onerror = (error) => {
        console.error('[WebSocket] ❌ Error:', error);
        setWsConnected(false);
      };

      ws.onclose = (event) => {
        console.log(`[WebSocket] 🔌 Disconnected (code: ${event.code}, reason: ${event.reason})`);
        setWsConnected(false);

        // Only reconnect if not a normal closure
        if (event.code !== 1000) {
          console.log('[WebSocket] 🔄 Reconnecting in 3 seconds...');
          setTimeout(() => {
            if (projectId && isAuthenticated) {
              connectWebSocket();
            }
          }, 3000);
        }
      };

      wsRef.current = ws;
    } catch (err) {
      console.error('[WebSocket] ❌ Failed to create connection:', err);
      setWsConnected(false);
    }
  };

  const handleWebSocketMessage = (data: any) => {
    switch (data.type) {
      case 'connected':
        // Load chat history
        if (data.messages && data.messages.length > 0) {
          setMessages(data.messages);
        }
        break;

      case 'message_start':
      case 'agent_thinking':
        // Start new assistant message
        setMessages(prev => [
          ...prev,
          {
            role: 'assistant',
            content: '',
            timestamp: new Date().toISOString(),
            agent_name: data.speaker || data.agent_name || 'DEV-O',  // Capture agent name (Alex, Sarah, Marcus, Elena)
            agent_role: data.agent_role,
          },
        ]);
        break;

      // Removed: Backend no longer echoes user messages

      case 'message_chunk':
      case 'content_chunk':
        // Real-time streaming chunk from agent (backend filters tool calls)
        // Optimized: Only update last message without copying entire array
        setMessages(prev => {
          if (prev.length === 0) return prev;
          const lastIdx = prev.length - 1;
          const lastMessage = prev[lastIdx];
          if (!lastMessage || lastMessage.role !== 'assistant') return prev;

          // Only copy and update the last message
          const updatedLast = {
            ...lastMessage,
            content: lastMessage.content + (data.chunk || '')
          };

          // Return new array with only last item replaced
          return [...prev.slice(0, lastIdx), updatedLast];
        });
        break;

      case 'thinking':
        // Append thinking to last assistant message
        // Optimized: Only update last message
        setMessages(prev => {
          if (prev.length === 0) return prev;
          const lastIdx = prev.length - 1;
          const lastMessage = prev[lastIdx];
          if (!lastMessage || lastMessage.role !== 'assistant') return prev;

          const updatedLast = {
            ...lastMessage,
            content: lastMessage.content + (data.content || '')
          };
          return [...prev.slice(0, lastIdx), updatedLast];
        });
        break;

      case 'code':
        // Append code block to last assistant message
        // Optimized: Only update last message
        setMessages(prev => {
          if (prev.length === 0) return prev;
          const lastIdx = prev.length - 1;
          const lastMessage = prev[lastIdx];
          if (!lastMessage || lastMessage.role === 'assistant') return prev;

          const updatedLast = {
            ...lastMessage,
            content: lastMessage.content + `\n\`\`\`${data.language || ''}\n${data.content || ''}\n\`\`\`\n`
          };
          return [...prev.slice(0, lastIdx), updatedLast];
        });
        break;

      case 'status':
      case 'agent_start':
      case 'task_created':
      case 'iteration_start':
      case 'context_assembled':
      case 'tool_call_start':
      case 'tool_call_result':
        // These are progress events - could show in UI if needed
        // For now, just log them
        break;

      case 'message_end':
      case 'message_complete':
      case 'waiting_for_user':
        // Message complete
        setLoading(false);
        break;

      case 'error':
        // Error occurred
        const errorMessage: ChatMessage = {
          role: 'assistant',
          content: `Error: ${data.content}`,
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, errorMessage]);
        setLoading(false);
        break;
    }
  };

  const handleCommand = async (command: string): Promise<boolean> => {
    const cmd = command.toLowerCase().trim();

    // Handle /help
    if (cmd === '/help') {
      const helpMessage: ChatMessage = {
        role: 'assistant',
        content: `**Available Commands:**

• **/help** - Show this help message
• **/status** - Show current project status and statistics
• **/agents** - List active agents for current project
• **/clear** - Clear chat history
• **/projects** - Navigate to projects page
• **/dashboard** - Navigate to dashboard

You can also chat normally to generate code and get assistance!`,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, helpMessage]);
      return true;
    }

    // Handle /status
    if (cmd === '/status') {
      try {
        const projects = await apiService.getProjects();
        const currentProject = projects.find(p => p.id === projectId);
        const agents = projectId ? await apiService.getProjectAgents(projectId) : [];

        const statusMessage: ChatMessage = {
          role: 'assistant',
          content: `**Project Status:**

📁 **Current Project:** ${currentProject?.name || 'Unknown'}
🤖 **Active Agents:** ${agents.length}
💬 **Messages:** ${messages.length}
📊 **Total Projects:** ${projects.length}`,
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, statusMessage]);
      } catch (error) {
        const errorMessage: ChatMessage = {
          role: 'assistant',
          content: 'Failed to fetch status information.',
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, errorMessage]);
      }
      return true;
    }

    // Handle /agents
    if (cmd === '/agents') {
      try {
        if (!projectId) {
          throw new Error('No project selected');
        }
        const agents = await apiService.getProjectAgents(projectId);

        let agentsContent = '**Active Agents:**\n\n';
        if (agents.length === 0) {
          agentsContent += 'No active agents for this project.';
        } else {
          agents.forEach((agent: any, index: number) => {
            agentsContent += `${index + 1}. **${agent.name || agent.type}** (${agent.status || 'active'})\n`;
          });
        }

        const agentsMessage: ChatMessage = {
          role: 'assistant',
          content: agentsContent,
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, agentsMessage]);
      } catch (error) {
        const errorMessage: ChatMessage = {
          role: 'assistant',
          content: 'Failed to fetch agents information.',
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, errorMessage]);
      }
      return true;
    }

    // Handle /clear
    if (cmd === '/clear') {
      setMessages([]);
      const clearMessage: ChatMessage = {
        role: 'assistant',
        content: 'Chat history cleared.',
        timestamp: new Date().toISOString(),
      };
      setMessages([clearMessage]);
      return true;
    }

    // Handle /projects
    if (cmd === '/projects') {
      navigate('/projects');
      return true;
    }

    // Handle /dashboard
    if (cmd === '/dashboard') {
      navigate('/dashboard');
      return true;
    }

    return false;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading || !wsConnected) return;

    const inputText = input.trim();

    // Check if input is a command
    if (inputText.startsWith('/')) {
      const userMessage: ChatMessage = {
        role: 'user',
        content: inputText,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, userMessage]);
      setInput('');

      const isCommand = await handleCommand(inputText);
      if (isCommand) {
        return; // Command handled, don't send to API
      }
    }

    // Require WebSocket connection
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Not connected to server. Please wait...',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
      setInput('');
      return;
    }

    // Add user message to UI immediately
    const userMessage: ChatMessage = {
      role: 'user',
      content: inputText,
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMessage]);

    // Clear input and set loading
    setInput('');
    setLoading(true);

    // Send message via WebSocket
    wsRef.current.send(JSON.stringify({
      type: 'message',
      content: inputText,
    }));
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-page">
      {/* Header */}
      <header className="chat-header">
        <div className="chat-header-left">
          <Logo size={120} showText={false} />
          {wsConnected ? (
            <span className="connection-status connected" title="Connected">🟢</span>
          ) : (
            <span className="connection-status disconnected" title="Connecting...">🔴</span>
          )}
        </div>

        <div className="chat-header-right">
          <div className="user-menu">
            <button
              className="user-menu-button"
              onClick={() => setShowMenu(!showMenu)}
            >
              <div className="user-avatar">
                {user?.email?.[0].toUpperCase() || 'U'}
              </div>
              <span className="user-email">{user?.email}</span>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 5.293a1 1 0 011.414 0L8 7.586l2.293-2.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>

            {showMenu && (
              <div className="user-menu-dropdown">
                <button className="menu-item" onClick={handleLogout}>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 001 1h12a1 1 0 001-1V4a1 1 0 00-1-1H3zm11 4.414l-4.293 4.293a1 1 0 01-1.414 0L4 7.414 5.414 6l3.293 3.293L13.414 4.586 14.828 6z" clipRule="evenodd" />
                  </svg>
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <Logo size={120} showText={false} />
            <h2 className="empty-title">How can I help you today?</h2>
            <p className="empty-subtitle">Start a conversation with DEV-O AI</p>

            <div className="example-prompts">
              <button
                className="example-prompt"
                onClick={() => setInput("Create a REST API with user authentication")}
              >
                <span className="prompt-icon">🚀</span>
                <span>Create a REST API with user authentication</span>
              </button>
              <button
                className="example-prompt"
                onClick={() => setInput("Build a responsive landing page")}
              >
                <span className="prompt-icon">🎨</span>
                <span>Build a responsive landing page</span>
              </button>
              <button
                className="example-prompt"
                onClick={() => setInput("Set up a database schema for an e-commerce app")}
              >
                <span className="prompt-icon">💾</span>
                <span>Set up a database schema for an e-commerce app</span>
              </button>
            </div>
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
                    <div className="avatar-assistant">
                      <Logo size={32} showText={false} />
                    </div>
                  )}
                </div>
                <div className="message-content">
                  <div className="message-role">
                    {message.role === 'user' ? 'You' : (message.agent_name || 'DEV-O')}
                  </div>
                  <div className="message-text">{message.content}</div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="message message-assistant">
                <div className="message-avatar">
                  <div className="avatar-assistant">
                    <Logo size={32} showText={false} />
                  </div>
                </div>
                <div className="message-content">
                  <div className="message-role">DEV-O</div>
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

      {/* Input */}
      <div className="chat-input-container">
        <div className="chat-input-header">
          <button
            className="command-help-btn"
            onClick={() => setInput('/help')}
            title="Show available commands"
          >
            💡 Commands
          </button>
        </div>
        <form onSubmit={handleSubmit} className="chat-input-form">
          <textarea
            ref={textareaRef}
            className="chat-input"
            placeholder={projectLoading ? "Initializing..." : "Message DEV-O... (Type /help for commands)"}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={loading || projectLoading}
          />
          <button
            type="submit"
            className="chat-send-button"
            disabled={!input.trim() || loading || projectLoading || !wsConnected}
            title={!wsConnected ? 'Connecting to server...' : 'Send message'}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M22 2L11 13" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M22 2L15 22L11 13L2 9L22 2Z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </form>
        <p className="chat-disclaimer">
          DEV-O can make mistakes. Consider checking important information.
        </p>
      </div>
    </div>
  );
};

export default Chat;
