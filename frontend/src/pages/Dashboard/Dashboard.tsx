import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../../services/api';
import './Dashboard.css';

interface Stats {
  totalProjects: number;
  activeAgents: number;
  tasksCompleted: number;
  tasksInProgress: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<Stats>({
    totalProjects: 0,
    activeAgents: 0,
    tasksCompleted: 0,
    tasksInProgress: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const projects = await apiService.getProjects();
      const currentProjectId = localStorage.getItem('current_project_id');

      if (currentProjectId) {
        const agents = await apiService.getProjectAgents(currentProjectId);
        // Mock tasks data for now
        setStats({
          totalProjects: projects.length,
          activeAgents: agents?.length || 0,
          tasksCompleted: 12, // Will be replaced with real data
          tasksInProgress: 3, // Will be replaced with real data
        });
      } else {
        setStats({
          totalProjects: projects.length,
          activeAgents: 0,
          tasksCompleted: 0,
          tasksInProgress: 0,
        });
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="dashboard-loading">
          <div className="spinner-large"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Dashboard</h1>
          <p className="dashboard-subtitle">Welcome back! Here's your project overview.</p>
        </div>
        <Link to="/chat" className="dashboard-action-btn">
          <span>💬</span> Start Chat
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon projects">📁</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalProjects}</div>
            <div className="stat-label">Total Projects</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon agents">🤖</div>
          <div className="stat-content">
            <div className="stat-value">{stats.activeAgents}</div>
            <div className="stat-label">Active Agents</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon completed">✅</div>
          <div className="stat-content">
            <div className="stat-value">{stats.tasksCompleted}</div>
            <div className="stat-label">Tasks Completed</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon progress">⏳</div>
          <div className="stat-content">
            <div className="stat-value">{stats.tasksInProgress}</div>
            <div className="stat-label">In Progress</div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2 className="section-title">Quick Actions</h2>
        <div className="actions-grid">
          <Link to="/chat" className="action-card">
            <span className="action-icon">💬</span>
            <h3>Start Chat</h3>
            <p>Begin a conversation with AI agents</p>
          </Link>

          <Link to="/projects" className="action-card">
            <span className="action-icon">📁</span>
            <h3>New Project</h3>
            <p>Create a new development project</p>
          </Link>

          <Link to="/agents" className="action-card">
            <span className="action-icon">🤖</span>
            <h3>View Agents</h3>
            <p>See all active AI agents</p>
          </Link>

          <Link to="/tasks" className="action-card">
            <span className="action-icon">📝</span>
            <h3>Task History</h3>
            <p>Review completed and pending tasks</p>
          </Link>
        </div>
      </div>

      {/* Getting Started */}
      {stats.totalProjects === 0 && (
        <div className="getting-started">
          <div className="getting-started-content">
            <h2>🚀 Getting Started with DEV-O</h2>
            <p>Welcome to DEV-O! Here's how to get started:</p>
            <ol>
              <li>
                <strong>Create a Project</strong> - Your first project is already created!
              </li>
              <li>
                <strong>Start Chatting</strong> - Go to the Chat page and describe what you want to build
              </li>
              <li>
                <strong>Let AI Work</strong> - Our agents will collaborate to build your solution
              </li>
              <li>
                <strong>Review & Iterate</strong> - Check the generated code and refine as needed
              </li>
            </ol>
            <Link to="/chat" className="get-started-btn">
              Start Your First Chat →
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
