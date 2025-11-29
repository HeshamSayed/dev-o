/**
 * API Service for DEV-O Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  username?: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  agent_name?: string;  // Agent name (Alex, Sarah, Marcus, Elena)
  agent_role?: string;  // Agent role (orchestrator, architect, backend_lead, frontend_lead)
}

interface ExecuteTaskRequest {
  message: string;
  project_id: string;
}

class ApiService {
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    const token = localStorage.getItem('access_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }));

      // Handle different error formats from Django REST Framework
      if (error.detail) {
        throw new Error(error.detail);
      }

      // Handle field-specific errors
      if (typeof error === 'object') {
        const errorMessages = Object.entries(error)
          .map(([field, messages]) => {
            if (Array.isArray(messages)) {
              return `${field}: ${messages.join(', ')}`;
            }
            return `${field}: ${messages}`;
          })
          .join('; ');

        if (errorMessages) {
          throw new Error(errorMessages);
        }
      }

      throw new Error(`HTTP ${response.status}: ${error.message || 'An error occurred'}`);
    }
    return response.json();
  }

  // Authentication
  async login(credentials: LoginCredentials) {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });

    const result = await this.handleResponse<{ user: any; tokens: { access: string; refresh: string } }>(response);

    // Store tokens
    localStorage.setItem('access_token', result.tokens.access);
    localStorage.setItem('refresh_token', result.tokens.refresh);

    return {
      access: result.tokens.access,
      refresh: result.tokens.refresh,
      user: result.user,
    };
  }

  async register(data: RegisterData) {
    console.log('Registration data being sent:', data);

    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    console.log('Registration response status:', response.status);

    const result = await this.handleResponse<{ user: any; tokens: { access: string; refresh: string } }>(response);

    // Store tokens
    localStorage.setItem('access_token', result.tokens.access);
    localStorage.setItem('refresh_token', result.tokens.refresh);

    return {
      access: result.tokens.access,
      refresh: result.tokens.refresh,
      user: result.user,
    };
  }

  async logout() {
    const refresh_token = localStorage.getItem('refresh_token');

    try {
      await fetch(`${API_BASE_URL}/auth/logout/`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ refresh_token }),
      });
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }

  async getCurrentUser() {
    const response = await fetch(`${API_BASE_URL}/auth/me/`, {
      headers: this.getHeaders(),
    });

    return this.handleResponse<any>(response);
  }

  // Chat / Task Execution
  async executeTask(request: ExecuteTaskRequest) {
    if (!request.project_id) {
      throw new Error('Project ID is required');
    }

    const response = await fetch(`${API_BASE_URL}/agents/projects/${request.project_id}/execute/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ message: request.message }),
    });

    return this.handleResponse<any>(response);
  }

  async getAgentMessages(agentId: string) {
    const response = await fetch(`${API_BASE_URL}/agents/${agentId}/messages/`, {
      headers: this.getHeaders(),
    });

    return this.handleResponse<ChatMessage[]>(response);
  }

  // Projects
  async getProjects() {
    const response = await fetch(`${API_BASE_URL}/projects/`, {
      headers: this.getHeaders(),
    });

    return this.handleResponse<any[]>(response);
  }

  async createProject(name: string, description?: string) {
    const response = await fetch(`${API_BASE_URL}/projects/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ name, description }),
    });

    return this.handleResponse<any>(response);
  }

  async updateProject(id: string, name: string, description?: string) {
    const response = await fetch(`${API_BASE_URL}/projects/${id}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify({ name, description }),
    });

    return this.handleResponse<any>(response);
  }

  async deleteProject(id: string) {
    const response = await fetch(`${API_BASE_URL}/projects/${id}/`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });

    if (response.status === 204) {
      return { success: true };
    }

    return this.handleResponse<any>(response);
  }

  async getProjectAgents(projectId: string) {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}/agents/`, {
      headers: this.getHeaders(),
    });

    return this.handleResponse<any[]>(response);
  }

  async getProjectTasks(projectId: string) {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}/tasks/`, {
      headers: this.getHeaders(),
    });

    return this.handleResponse<any[]>(response);
  }

  // Agents
  async getAgents() {
    const response = await fetch(`${API_BASE_URL}/agents/`, {
      headers: this.getHeaders(),
    });

    return this.handleResponse<any[]>(response);
  }

  async getAgentById(agentId: string) {
    const response = await fetch(`${API_BASE_URL}/agents/${agentId}/`, {
      headers: this.getHeaders(),
    });

    return this.handleResponse<any>(response);
  }
}

export const apiService = new ApiService();
export type { LoginCredentials, RegisterData, ChatMessage, ExecuteTaskRequest };
