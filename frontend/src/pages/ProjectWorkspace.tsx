import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { useAuthStore } from '../store/authStore';
import Logo from '../components/Logo/Logo';
import UsageIndicator from '../components/UsageIndicator';
import UpgradeModal from '../components/UpgradeModal';
import apiClient from '../api/client';
import { Project, ProjectFile, ChatMessage, WSMessage } from '../types';
import { FileStreamParser } from '../utils/fileStreamParser';
import './ProjectWorkspace.css';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

export default function ProjectWorkspace() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuthStore();

  // Redirect if no project ID
  useEffect(() => {
    if (!id || id === 'undefined') {
      navigate('/projects');
    }
  }, [id, navigate]);

  const [project, setProject] = useState<Project | null>(null);
  const [files, setFiles] = useState<ProjectFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<ProjectFile | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [limitInfo, setLimitInfo] = useState<{ used: number; limit: number; minutesUntilReset: number } | null>(null);

  // Real-time editor streaming state
  const [streamingFile, setStreamingFile] = useState<{ path: string; content: string } | null>(null);
  const [editorContent, setEditorContent] = useState<string>('');

  // CrewAI Multi-Agent Mode
  const [useCrewAI, setUseCrewAI] = useState(false);
  const [crewAgents, setCrewAgents] = useState<Array<{ name: string; status: 'pending' | 'working' | 'completed' }>>([]);
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileParserRef = useRef<FileStreamParser>(new FileStreamParser());

  // Helper function to extract agent name from various formats
  const getAgentName = (agent: string | { name: string } | undefined): string => {
    if (!agent) return 'Agent';
    return typeof agent === 'string' ? agent : agent.name;
  };

  useEffect(() => {
    fetchProject();
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [id]);

  const connectWebSocket = () => {
    const token = localStorage.getItem('access_token');
    const ws = new WebSocket(`${WS_URL}/ws/project/${id}/?token=${token}`);

    ws.onopen = () => {
      console.log('Project WebSocket connected');
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
      setTimeout(connectWebSocket, 3000);
    };

    wsRef.current = ws;
  };

  const handleWebSocketMessage = (data: WSMessage) => {
    switch (data.type) {
      case 'project_state':
        setProject(data.project);
        setMessages(data.messages || []);
        if (data.files) {
          fetchFiles();
        }
        break;
      case 'crew_init':
        // Initialize CrewAI agent pipeline
        if (data.agents) {
          setCrewAgents(data.agents.map((a: any) => ({ name: a.name, status: 'pending' })));
          setMessages(prev => [...prev, {
            role: 'system',
            content: '🚀 Initializing CrewAI Multi-Agent System...\n• Product Owner\n• Backend Developer\n• Frontend Developer\n• QA Engineer',
          }]);
        }
        break;
      case 'agent_started':
        // Mark agent as working
        const startedAgentName = getAgentName(data.agent);
        setCurrentAgent(startedAgentName);
        setCrewAgents(prev => prev.map(a => 
          a.name === startedAgentName ? { ...a, status: 'working' } : a
        ));
        setMessages(prev => [...prev, {
          role: 'system',
          content: `🔧 ${startedAgentName} started working...`,
        }]);
        break;
      case 'agent_completed':
        // Mark agent as completed
        const completedAgentName = getAgentName(data.agent);
        setCrewAgents(prev => prev.map(a => 
          a.name === completedAgentName ? { ...a, status: 'completed' } : a
        ));
        setMessages(prev => [...prev, {
          role: 'system',
          content: `✅ ${completedAgentName} completed! Created ${data.files_created || 0} file(s).`,
        }]);
        setCurrentAgent(null);
        break;
      case 'crew_completed':
        setLoading(false);
        setCrewAgents([]);
        setCurrentAgent(null);
        setMessages(prev => [...prev, {
          role: 'system',
          content: `🎉 ${data.message || 'CrewAI pipeline completed successfully!'}\nTotal files: ${data.total_files || 0}`,
        }]);
        break;
      case 'agent_working':
        const workingAgentName = getAgentName(data.agent);
        setMessages(prev => [...prev, {
          role: 'system',
          content: `${workingAgentName} is working on your request...`,
        }]);
        // Reset file parser for new response
        fileParserRef.current.reset();
        break;
      case 'token':
        setLoading(false);
        // Parse token for file tags
        console.log('[DEBUG] Received token:', data.content);
        const { events } = fileParserRef.current.processToken(data.content || '');
        console.log('[DEBUG] Parser emitted events:', events);

        events.forEach(event => {
          switch (event.type) {
            case 'file_start':
              // Open file in editor and start streaming
              const filePath = event.data.path;
              setStreamingFile({ path: filePath, content: '' });
              setEditorContent('');
              setMessages(prev => [...prev, {
                role: 'system',
                content: `Working on ${filePath}...`,
              }]);
              break;

            case 'file_content':
              // Stream content to editor
              setStreamingFile(prev => prev ? {
                ...prev,
                content: prev.content + event.data.content
              } : null);
              setEditorContent(prev => prev + event.data.content);
              break;

            case 'file_end':
              // File complete, show completion message
              setMessages(prev => [...prev, {
                role: 'system',
                content: `✓ Created ${event.data.path}`,
              }]);
              setStreamingFile(null);
              break;

            case 'chat_content':
              // Regular chat content (status messages)
              if (event.data.trim()) {
                setMessages(prev => {
                  const lastIdx = prev.length - 1;
                  const lastMsg = prev[lastIdx];
                  if (lastMsg && lastMsg.role === 'agent') {
                    return [...prev.slice(0, lastIdx), { ...lastMsg, content: lastMsg.content + event.data }];
                  }
                  return [...prev, { role: 'agent', content: event.data }];
                });
              }
              break;
          }
        });
        break;
      case 'file_created':
        fetchFiles();
        break;
      case 'file_tree_update':
        if (project) {
          setProject({ ...project, file_tree: data.tree });
        }
        break;
      case 'done':
        setLoading(false);
        fileParserRef.current.reset();
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
        setMessages(prev => [...prev, { role: 'system', content: `Error: ${data.error}` }]);
        break;
    }
  };

  const fetchProject = async () => {
    try {
      const response = await apiClient.get(`/projects/${id}/`);
      setProject(response.data);
      fetchFiles();
    } catch (error) {
      console.error('Failed to fetch project:', error);
    }
  };

  const fetchFiles = async () => {
    try {
      const response = await apiClient.get(`/projects/${id}/files/`);
      setFiles(response.data);
      if (response.data.length > 0 && !selectedFile) {
        setSelectedFile(response.data[0]);
      }
    } catch (error) {
      console.error('Failed to fetch files:', error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading || !wsConnected) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input.trim(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    // Send appropriate message type based on mode
    const messageType = useCrewAI ? 'crew_message' : 'project_message';
    
    wsRef.current?.send(JSON.stringify({
      type: messageType,
      message: input.trim(),
      show_thinking: true,
    }));
  };

  const renderFileTree = (tree: any, path: string = '') => {
    return Object.keys(tree).map(key => {
      const node = tree[key];
      const fullPath = path ? `${path}/${key}` : key;

      if (node.type === 'directory') {
        return (
          <div key={fullPath} className="tree-directory">
            <div className="tree-directory-name">📁 {key}</div>
            {node.children && (
              <div className="tree-directory-children">
                {renderFileTree(node.children, fullPath)}
              </div>
            )}
          </div>
        );
      } else {
        const file = files.find(f => f.path === fullPath);
        const isSelected = selectedFile?.path === fullPath;
        return (
          <div
            key={fullPath}
            className={`tree-file ${isSelected ? 'selected' : ''}`}
            onClick={() => file && setSelectedFile(file)}
          >
            📄 {key}
          </div>
        );
      }
    });
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (!project) {
    return <div className="loading">Loading project...</div>;
  }

  return (
    <div className="project-workspace">
      <header className="workspace-header">
        <div className="header-left">
          <Logo size={100} showText={false} />
          <div>
            <h1>{project.name}</h1>
            <p>{project.description}</p>
          </div>
        </div>
        <div className="header-center">
          <UsageIndicator compact />
        </div>
        <div className="header-right">
          <button onClick={() => navigate('/pricing')} className="btn-secondary">
            Pricing
          </button>
          <button onClick={() => navigate('/referrals')} className="btn-secondary">
            Referrals
          </button>
          <button onClick={() => navigate('/projects')} className="btn-secondary">
            Back to Projects
          </button>
          <button onClick={() => navigate('/chat')} className="btn-secondary">
            Chat
          </button>
        </div>
      </header>

      <div className="workspace-content">
        <div className="file-panel">
          <div className="file-panel-header">
            <h3>Files</h3>
            <span className="file-count">{files.length} files</span>
          </div>
          <div className="file-tree">
            {project.file_tree && renderFileTree(project.file_tree)}
          </div>
        </div>

        <div className="editor-panel">
          {streamingFile || selectedFile ? (
            <>
              <div className="editor-header">
                <span className="editor-file-name">
                  {streamingFile ? streamingFile.path : selectedFile?.path}
                  {streamingFile && <span style={{ marginLeft: '10px', color: '#10B981' }}>● Streaming...</span>}
                </span>
                <span className="editor-language">
                  {streamingFile ? streamingFile.path.split('.').pop() : selectedFile?.language}
                </span>
              </div>
              <Editor
                height="100%"
                language={streamingFile ? streamingFile.path.split('.').pop() : selectedFile?.language}
                value={streamingFile ? editorContent : selectedFile?.content}
                theme="vs-dark"
                options={{
                  readOnly: streamingFile ? true : false,
                  minimap: { enabled: true },
                  fontSize: 14,
                  lineNumbers: 'on',
                  scrollBeyondLastLine: false,
                }}
              />
            </>
          ) : (
            <div className="editor-empty">
              <p>Select a file to view</p>
            </div>
          )}
        </div>

        <div className="chat-panel">
          <div className="chat-panel-header">
            <h3>Project Chat</h3>
            <div className="header-controls">
              <button 
                className={`mode-toggle ${useCrewAI ? 'crew-mode' : 'single-mode'}`}
                onClick={() => setUseCrewAI(!useCrewAI)}
                title={useCrewAI ? 'Switch to Single-Agent Mode' : 'Switch to Multi-Agent Mode'}
              >
                {useCrewAI ? '👥 Multi-Agent' : '🤖 Single-Agent'}
              </button>
              {wsConnected ? (
                <span className="status-connected">🟢 Connected</span>
              ) : (
                <span className="status-disconnected">🔴 Disconnected</span>
              )}
            </div>
          </div>

          {/* CrewAI Agent Progress Display */}
          {useCrewAI && crewAgents.length > 0 && (
            <div className="crew-progress">
              <div className="crew-progress-title">Multi-Agent Pipeline</div>
              <div className="crew-agents">
                {crewAgents.map((agent, idx) => (
                  <div 
                    key={idx} 
                    className={`crew-agent crew-agent-${agent.status}`}
                  >
                    <div className="agent-icon">
                      {agent.status === 'completed' ? '✅' : 
                       agent.status === 'working' ? '⚙️' : '⏳'}
                    </div>
                    <div className="agent-info">
                      <div className="agent-name">{agent.name}</div>
                      <div className="agent-status">
                        {agent.status === 'completed' ? 'Completed' : 
                         agent.status === 'working' ? 'Working...' : 'Pending'}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-message chat-message-${msg.role}`}>
                <div className="message-role">
                  {msg.role === 'user' ? 'You' : msg.role === 'agent' ? 'DEV-O' : 'System'}
                </div>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}
            {loading && (
              <div className="chat-message chat-message-agent">
                <div className="message-role">DEV-O</div>
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              type="text"
              className="chat-input"
              placeholder="Ask DEV-O to modify your project..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading || !wsConnected}
            />
            <button
              type="submit"
              className="send-button"
              disabled={!input.trim() || loading || !wsConnected}
            >
              Send
            </button>
          </form>
        </div>
      </div>

      {limitInfo && (
        <UpgradeModal
          isOpen={showUpgradeModal}
          onClose={() => setShowUpgradeModal(false)}
          limitType="project"
          used={limitInfo.used}
          limit={limitInfo.limit}
          minutesUntilReset={limitInfo.minutesUntilReset}
        />
      )}
    </div>
  );
}
