import React, { useEffect, useState } from 'react';
import { apiService } from '../../services/api';
import './Tasks.css';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: string;
  priority?: string;
  agent?: {
    id: string;
    name: string;
    type: string;
  };
  project?: {
    id: string;
    name: string;
  };
  created_at?: string;
  completed_at?: string;
  result?: string;
}

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending' | 'failed'>('all');
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const projectId = localStorage.getItem('current_project_id');
      if (projectId) {
        const tasksList = await apiService.getProjectTasks(projectId);
        setTasks(tasksList);
      } else {
        // If no project selected, get all projects and their tasks
        const projects = await apiService.getProjects();
        let allTasks: Task[] = [];
        for (const project of projects) {
          const projectTasks = await apiService.getProjectTasks(project.id);
          allTasks = [...allTasks, ...projectTasks];
        }
        setTasks(allTasks);
      }
    } catch (error) {
      console.error('Failed to load tasks:', error);
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'completed':
      case 'success':
        return '#22C55E';
      case 'pending':
      case 'in_progress':
      case 'running':
        return '#FBBF24';
      case 'failed':
      case 'error':
        return '#EF4444';
      default:
        return '#6B7280';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'completed':
      case 'success':
        return '✅';
      case 'pending':
      case 'in_progress':
      case 'running':
        return '⏳';
      case 'failed':
      case 'error':
        return '❌';
      default:
        return '📝';
    }
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    if (filter === 'completed') return task.status?.toLowerCase() === 'completed' || task.status?.toLowerCase() === 'success';
    if (filter === 'pending') return task.status?.toLowerCase() === 'pending' || task.status?.toLowerCase() === 'in_progress' || task.status?.toLowerCase() === 'running';
    if (filter === 'failed') return task.status?.toLowerCase() === 'failed' || task.status?.toLowerCase() === 'error';
    return true;
  });

  if (loading) {
    return (
      <div className="tasks-page">
        <div className="tasks-loading">
          <div className="spinner-large"></div>
          <p>Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tasks-page">
      <div className="tasks-header">
        <div>
          <h1 className="tasks-title">Task History</h1>
          <p className="tasks-subtitle">View and manage task execution history</p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="tasks-filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Tasks ({tasks.length})
        </button>
        <button
          className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
          onClick={() => setFilter('completed')}
        >
          Completed ({tasks.filter(t => t.status?.toLowerCase() === 'completed' || t.status?.toLowerCase() === 'success').length})
        </button>
        <button
          className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
          onClick={() => setFilter('pending')}
        >
          Pending ({tasks.filter(t => t.status?.toLowerCase() === 'pending' || t.status?.toLowerCase() === 'in_progress' || t.status?.toLowerCase() === 'running').length})
        </button>
        <button
          className={`filter-btn ${filter === 'failed' ? 'active' : ''}`}
          onClick={() => setFilter('failed')}
        >
          Failed ({tasks.filter(t => t.status?.toLowerCase() === 'failed' || t.status?.toLowerCase() === 'error').length})
        </button>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">📝</div>
          <h2>No Tasks Found</h2>
          <p>
            {filter === 'all'
              ? 'Start chatting to create tasks'
              : `No ${filter} tasks at the moment`}
          </p>
        </div>
      ) : (
        <div className="tasks-list">
          {filteredTasks.map((task) => (
            <div
              key={task.id}
              className="task-item"
              onClick={() => setSelectedTask(task)}
            >
              <div className="task-item-header">
                <div className="task-status-badge" style={{ backgroundColor: getStatusColor(task.status) }}>
                  <span className="task-status-icon">{getStatusIcon(task.status)}</span>
                  <span className="task-status-text">{task.status}</span>
                </div>
                {task.priority && (
                  <span className="task-priority">{task.priority}</span>
                )}
              </div>

              <h3 className="task-title">{task.title || task.description || 'Untitled Task'}</h3>

              {task.description && task.title && (
                <p className="task-description">{task.description}</p>
              )}

              <div className="task-meta">
                {task.agent && (
                  <span className="task-meta-item">
                    🤖 {task.agent.name || task.agent.type}
                  </span>
                )}
                {task.project && (
                  <span className="task-meta-item">
                    📁 {task.project.name}
                  </span>
                )}
                {task.created_at && (
                  <span className="task-meta-item">
                    🕐 {new Date(task.created_at).toLocaleString()}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Task Detail Modal */}
      {selectedTask && (
        <div className="modal-overlay" onClick={() => setSelectedTask(null)}>
          <div className="modal-content task-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Task Details</h2>
              <button className="modal-close" onClick={() => setSelectedTask(null)}>×</button>
            </div>

            <div className="task-detail-content">
              <div className="task-detail-header">
                <div className="task-status-badge large" style={{ backgroundColor: getStatusColor(selectedTask.status) }}>
                  <span className="task-status-icon">{getStatusIcon(selectedTask.status)}</span>
                  <span className="task-status-text">{selectedTask.status}</span>
                </div>
              </div>

              <h3 className="task-detail-title">{selectedTask.title || selectedTask.description || 'Untitled Task'}</h3>

              {selectedTask.description && selectedTask.title && (
                <div className="task-detail-section">
                  <h4>Description</h4>
                  <p>{selectedTask.description}</p>
                </div>
              )}

              {selectedTask.result && (
                <div className="task-detail-section">
                  <h4>Result</h4>
                  <pre className="task-result">{selectedTask.result}</pre>
                </div>
              )}

              <div className="task-detail-section">
                <h4>Information</h4>
                <div className="task-detail-info">
                  {selectedTask.agent && (
                    <div className="info-row">
                      <span className="info-label">Agent:</span>
                      <span className="info-value">{selectedTask.agent.name || selectedTask.agent.type}</span>
                    </div>
                  )}
                  {selectedTask.project && (
                    <div className="info-row">
                      <span className="info-label">Project:</span>
                      <span className="info-value">{selectedTask.project.name}</span>
                    </div>
                  )}
                  {selectedTask.priority && (
                    <div className="info-row">
                      <span className="info-label">Priority:</span>
                      <span className="info-value">{selectedTask.priority}</span>
                    </div>
                  )}
                  {selectedTask.created_at && (
                    <div className="info-row">
                      <span className="info-label">Created:</span>
                      <span className="info-value">{new Date(selectedTask.created_at).toLocaleString()}</span>
                    </div>
                  )}
                  {selectedTask.completed_at && (
                    <div className="info-row">
                      <span className="info-label">Completed:</span>
                      <span className="info-value">{new Date(selectedTask.completed_at).toLocaleString()}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Tasks;
