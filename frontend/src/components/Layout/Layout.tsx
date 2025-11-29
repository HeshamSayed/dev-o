import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { apiService } from '../../services/api';
import Logo from '../Logo/Logo';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

interface Project {
  id: string;
  name: string;
  description?: string;
  status?: string;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showProjectMenu, setShowProjectMenu] = useState(false);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const projectsList = await apiService.getProjects();
      setProjects(projectsList);

      // Load current project from localStorage or use first project
      const savedProjectId = localStorage.getItem('current_project_id');
      if (savedProjectId) {
        const project = projectsList.find((p: Project) => p.id === savedProjectId);
        if (project) {
          setCurrentProject(project);
          return;
        }
      }

      if (projectsList.length > 0) {
        setCurrentProject(projectsList[0]);
        localStorage.setItem('current_project_id', projectsList[0].id);
      }
    } catch (error) {
      console.error('Failed to load projects:', error);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const switchProject = (project: Project) => {
    setCurrentProject(project);
    localStorage.setItem('current_project_id', project.id);
    setShowProjectMenu(false);
    // Reload the current page to refresh data
    window.location.reload();
  };

  const isActive = (path: string) => location.pathname === path;

  const navItems = [
    { path: '/dashboard', icon: '📊', label: 'Dashboard' },
    { path: '/chat', icon: '💬', label: 'Chat' },
    { path: '/projects', icon: '📁', label: 'Projects' },
    { path: '/agents', icon: '🤖', label: 'Agents' },
    { path: '/tasks', icon: '📝', label: 'Tasks' },
    { path: '/settings', icon: '⚙️', label: 'Settings' },
  ];

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-header">
          <Link to="/dashboard" className="sidebar-logo">
            <Logo size={sidebarCollapsed ? 40 : 60} showText={false} />
            {!sidebarCollapsed && <span className="sidebar-logo-text">DEV-O</span>}
          </Link>
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            aria-label="Toggle sidebar"
          >
            {sidebarCollapsed ? '→' : '←'}
          </button>
        </div>

        {/* Project Selector */}
        {!sidebarCollapsed && currentProject && (
          <div className="project-selector">
            <button
              className="project-selector-button"
              onClick={() => setShowProjectMenu(!showProjectMenu)}
            >
              <div className="project-info">
                <span className="project-icon">📁</span>
                <div className="project-details">
                  <span className="project-name">{currentProject.name}</span>
                  <span className="project-status">{projects.length} projects</span>
                </div>
              </div>
              <span className="dropdown-arrow">▼</span>
            </button>

            {showProjectMenu && (
              <div className="project-menu-dropdown">
                <div className="project-menu-header">Switch Project</div>
                <div className="project-menu-list">
                  {projects.map((project) => (
                    <button
                      key={project.id}
                      className={`project-menu-item ${project.id === currentProject.id ? 'active' : ''}`}
                      onClick={() => switchProject(project)}
                    >
                      <span className="project-menu-icon">📁</span>
                      <div className="project-menu-info">
                        <span className="project-menu-name">{project.name}</span>
                        {project.description && (
                          <span className="project-menu-desc">{project.description}</span>
                        )}
                      </div>
                      {project.id === currentProject.id && (
                        <span className="project-menu-check">✓</span>
                      )}
                    </button>
                  ))}
                </div>
                <Link to="/projects" className="project-menu-footer" onClick={() => setShowProjectMenu(false)}>
                  <span>+</span> New Project
                </Link>
              </div>
            )}
          </div>
        )}

        {/* Navigation */}
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${isActive(item.path) ? 'active' : ''}`}
              title={sidebarCollapsed ? item.label : ''}
            >
              <span className="nav-icon">{item.icon}</span>
              {!sidebarCollapsed && <span className="nav-label">{item.label}</span>}
            </Link>
          ))}
        </nav>

        {/* User Menu */}
        <div className="sidebar-footer">
          <div className="user-section">
            <button
              className="user-button"
              onClick={() => setShowUserMenu(!showUserMenu)}
            >
              <div className="user-avatar">
                {user?.email?.[0].toUpperCase() || 'U'}
              </div>
              {!sidebarCollapsed && (
                <div className="user-info">
                  <span className="user-name">{user?.first_name || user?.email?.split('@')[0]}</span>
                  <span className="user-email">{user?.email}</span>
                </div>
              )}
            </button>

            {showUserMenu && (
              <div className="user-menu-dropdown">
                <Link to="/settings" className="user-menu-item" onClick={() => setShowUserMenu(false)}>
                  <span>⚙️</span> Settings
                </Link>
                <button className="user-menu-item" onClick={handleLogout}>
                  <span>🚪</span> Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

export default Layout;
export type { Project };
