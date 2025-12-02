import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import Logo from '../components/Logo/Logo';
import apiClient from '../api/client';
import { Project } from '../types';
import './ProjectsPage.css';

export default function ProjectsPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    project_type: 'fullstack',
  });

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await apiClient.get('/projects/');
      // Handle paginated response from DRF
      const data: any = response.data;
      setProjects(data.results || data);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/projects/', newProject);
      navigate(`/project/${response.data.id}`);
    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  return (
    <div className="projects-page">
      <header className="projects-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <Logo size={40} showText={false} />
          <h1>My Projects</h1>
        </div>
        <div className="header-actions">
          <button onClick={() => navigate('/pricing')}>Pricing</button>
          <button onClick={() => navigate('/referrals')}>Referrals</button>
          <button onClick={() => navigate('/chat')}>Back to Chat</button>
          <button onClick={() => setShowCreateModal(true)} className="create-btn">
            + New Project
          </button>
        </div>
      </header>

      <div className="projects-grid">
        {loading ? (
          <div>Loading...</div>
        ) : projects.length === 0 ? (
          <div className="empty-state">
            <h2>No projects yet</h2>
            <p>Create your first AI-powered project</p>
            <button onClick={() => setShowCreateModal(true)} className="create-btn">
              Create Project
            </button>
          </div>
        ) : (
          projects.map((project) => (
            <div
              key={project.id}
              className="project-card"
              onClick={() => navigate(`/project/${project.id}`)}
            >
              <h3>{project.name}</h3>
              <p>{project.description}</p>
              <div className="project-meta">
                <span>{project.file_count} files</span>
                <span>{project.project_type}</span>
                <span className={`status-${project.status}`}>{project.status}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Create New Project</h2>
            <form onSubmit={createProject}>
              <input
                type="text"
                placeholder="Project name"
                value={newProject.name}
                onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                required
              />
              <textarea
                placeholder="Description"
                value={newProject.description}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
              />
              <select
                value={newProject.project_type}
                onChange={(e) => setNewProject({ ...newProject, project_type: e.target.value })}
              >
                <option value="fullstack">Full Stack</option>
                <option value="backend">Backend Only</option>
                <option value="frontend">Frontend Only</option>
              </select>
              <div className="modal-actions">
                <button type="button" onClick={() => setShowCreateModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="create-btn">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
