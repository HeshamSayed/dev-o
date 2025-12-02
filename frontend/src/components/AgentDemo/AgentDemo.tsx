import React, { useState, useEffect } from 'react';
import './AgentDemo.css';

interface Agent {
  id: string;
  name: string;
  role: string;
  color: string;
  level: number;
}

interface AgentAction {
  agentId: string;
  action: string;
  status: 'thinking' | 'working' | 'completed';
  timestamp: number;
}

const agents: Agent[] = [
  { id: 'orchestrator', name: 'Orchestrator', role: 'Project Manager', color: '#2563EB', level: 0 },
  { id: 'architect', name: 'Architect', role: 'Technical Lead', color: '#A855F7', level: 1 },
  { id: 'backend', name: 'Backend Lead', role: 'API Development', color: '#06B6D4', level: 2 },
  { id: 'frontend', name: 'Frontend Lead', role: 'UI Development', color: '#60A5FA', level: 2 },
];

const demoActions: AgentAction[] = [
  { agentId: 'orchestrator', action: 'Analyzing project requirements...', status: 'completed', timestamp: 0 },
  { agentId: 'orchestrator', action: 'Breaking down into tasks', status: 'completed', timestamp: 1000 },
  { agentId: 'architect', action: 'Designing system architecture', status: 'completed', timestamp: 2000 },
  { agentId: 'architect', action: 'Choosing tech stack: Django + React', status: 'completed', timestamp: 3000 },
  { agentId: 'backend', action: 'Creating database models', status: 'completed', timestamp: 4000 },
  { agentId: 'backend', action: 'Building REST API endpoints', status: 'working', timestamp: 5000 },
  { agentId: 'frontend', action: 'Setting up React components', status: 'thinking', timestamp: 6000 },
];

const AgentDemo: React.FC = () => {
  const [visibleActions, setVisibleActions] = useState<AgentAction[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < demoActions.length) {
      const timer = setTimeout(() => {
        setVisibleActions([...visibleActions, demoActions[currentIndex]]);
        setCurrentIndex(currentIndex + 1);
      }, 800);
      return () => clearTimeout(timer);
    } else {
      // Reset animation after completion
      const resetTimer = setTimeout(() => {
        setVisibleActions([]);
        setCurrentIndex(0);
      }, 3000);
      return () => clearTimeout(resetTimer);
    }
  }, [currentIndex, visibleActions]);

  return (
    <section className="agent-demo" id="demo">
      <div className="container">
        <div className="demo-header">
          <h2 className="demo-title">
            Watch <span className="gradient-text">Agents Orchestrate</span>
          </h2>
          <p className="demo-subtitle">
            See how multiple AI agents work together to build your application
          </p>
        </div>

        <div className="demo-content">
          {/* Agent Cards */}
          <div className="agents-panel">
            <h3 className="panel-title">Active Agents</h3>
            <div className="agents-list">
              {agents.map((agent) => {
                const isActive = visibleActions.some(a => a.agentId === agent.id);
                const currentAction = visibleActions
                  .filter(a => a.agentId === agent.id)
                  .slice(-1)[0];

                return (
                  <div
                    key={agent.id}
                    className={`agent-card ${isActive ? 'active' : ''}`}
                    style={{ '--agent-color': agent.color } as React.CSSProperties}
                  >
                    <div className="agent-avatar" style={{ background: agent.color }}>
                      <span className="agent-level">L{agent.level}</span>
                    </div>
                    <div className="agent-info">
                      <div className="agent-name">{agent.name}</div>
                      <div className="agent-role">{agent.role}</div>
                      {currentAction && (
                        <div className={`agent-status status-${currentAction.status}`}>
                          {currentAction.status === 'thinking' && 'Thinking'}
                          {currentAction.status === 'working' && 'Working'}
                          {currentAction.status === 'completed' && 'Completed'}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Activity Timeline */}
          <div className="timeline-panel">
            <h3 className="panel-title">Activity Timeline</h3>
            <div className="timeline">
              {visibleActions.map((action, index) => {
                const agent = agents.find(a => a.id === action.agentId);
                return (
                  <div
                    key={index}
                    className={`timeline-item status-${action.status}`}
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div
                      className="timeline-marker"
                      style={{ background: agent?.color }}
                    ></div>
                    <div className="timeline-content">
                      <div className="timeline-agent" style={{ color: agent?.color }}>
                        {agent?.name}
                      </div>
                      <div className="timeline-action">{action.action}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Code Output Preview */}
        <div className="output-preview">
          <div className="output-header">
            <span className="output-icon">📁</span>
            <span className="output-title">Generated Code</span>
          </div>
          <div className="output-body">
            <pre className="code-block">
              <code>{`// models.py - Generated by Backend Lead
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

// views.py - Generated by Backend Lead
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer`}</code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AgentDemo;
