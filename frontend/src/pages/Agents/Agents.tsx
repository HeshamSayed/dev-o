import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../../services/api';
import './Agents.css';

interface Agent {
  id: string;
  name: string;
  type: string;
  status: string;
  project?: {
    id: string;
    name: string;
  };
  created_at?: string;
  last_active?: string;
}

const Agents: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'active' | 'idle'>('all');

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      setLoading(true);
      const agentsList = await apiService.getAgents();
      setAgents(agentsList);
    } catch (error) {
      console.error('Failed to load agents:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'active':
      case 'running':
        return '#22C55E';
      case 'idle':
      case 'waiting':
        return '#FBBF24';
      case 'error':
      case 'failed':
        return '#EF4444';
      default:
        return '#6B7280';
    }
  };

  const getAgentIcon = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'planner':
        return '🧠';
      case 'coder':
      case 'developer':
        return '💻';
      case 'tester':
        return '🧪';
      case 'reviewer':
        return '🔍';
      default:
        return '🤖';
    }
  };

  const filteredAgents = agents.filter(agent => {
    if (filter === 'all') return true;
    if (filter === 'active') return agent.status?.toLowerCase() === 'active' || agent.status?.toLowerCase() === 'running';
    if (filter === 'idle') return agent.status?.toLowerCase() === 'idle' || agent.status?.toLowerCase() === 'waiting';
    return true;
  });

  if (loading) {
    return (
      <div className="agents-page">
        <div className="agents-loading">
          <div className="spinner-large"></div>
          <p>Loading agents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="agents-page">
      <div className="agents-header">
        <div>
          <h1 className="agents-title">AI Agents</h1>
          <p className="agents-subtitle">Monitor and manage your AI agents</p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="agents-filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Agents ({agents.length})
        </button>
        <button
          className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
          onClick={() => setFilter('active')}
        >
          Active ({agents.filter(a => a.status?.toLowerCase() === 'active' || a.status?.toLowerCase() === 'running').length})
        </button>
        <button
          className={`filter-btn ${filter === 'idle' ? 'active' : ''}`}
          onClick={() => setFilter('idle')}
        >
          Idle ({agents.filter(a => a.status?.toLowerCase() === 'idle' || a.status?.toLowerCase() === 'waiting').length})
        </button>
      </div>

      {filteredAgents.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">🤖</div>
          <h2>No Agents Found</h2>
          <p>
            {filter === 'all'
              ? 'Start chatting to create AI agents for your projects'
              : `No ${filter} agents at the moment`}
          </p>
          <Link to="/chat" className="create-agent-btn">
            Start Chat →
          </Link>
        </div>
      ) : (
        <div className="agents-grid">
          {filteredAgents.map((agent) => (
            <div key={agent.id} className="agent-card">
              <div className="agent-card-header">
                <div className="agent-icon">{getAgentIcon(agent.type)}</div>
                <div
                  className="agent-status-indicator"
                  style={{ backgroundColor: getStatusColor(agent.status) }}
                  title={agent.status}
                ></div>
              </div>

              <h3 className="agent-name">{agent.name || agent.type}</h3>
              <p className="agent-type">{agent.type}</p>

              <div className="agent-info">
                <div className="agent-info-item">
                  <span className="info-label">Status:</span>
                  <span className="info-value" style={{ color: getStatusColor(agent.status) }}>
                    {agent.status || 'Unknown'}
                  </span>
                </div>
                {agent.project && (
                  <div className="agent-info-item">
                    <span className="info-label">Project:</span>
                    <span className="info-value">{agent.project.name}</span>
                  </div>
                )}
                {agent.last_active && (
                  <div className="agent-info-item">
                    <span className="info-label">Last Active:</span>
                    <span className="info-value">
                      {new Date(agent.last_active).toLocaleString()}
                    </span>
                  </div>
                )}
              </div>

              <div className="agent-card-footer">
                <Link
                  to={`/chat?project=${agent.project?.id || ''}`}
                  className="agent-link"
                >
                  View in Chat →
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Agents;
