// Types for the application

export interface User {
  id: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  profile?: UserProfile;
}

export interface UserProfile {
  display_name?: string;
  show_thinking: boolean;
  theme: string;
  preferences: Record<string, any>;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  project_type: string;
  status: string;
  file_count: number;
  agents: Agent[];
  file_tree: FileTree;
  created_at: string;
  updated_at: string;
}

export interface ProjectFile {
  id: string;
  path: string;
  content: string;
  language: string;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface Agent {
  id: string;
  name: string;
  type: string;
  system_prompt?: string;
  capabilities?: string[];
}

export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant' | 'agent' | 'system';
  content: string;
  thinking?: string;
  agent_name?: string;
  created_at?: string;
}

export interface Conversation {
  id: string;
  title: string;
  is_project_chat: boolean;
  project?: string;
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface FileTree {
  [key: string]: FileTreeNode;
}

export interface FileTreeNode {
  type: 'file' | 'directory';
  id?: string;
  children?: FileTree;
}

export interface WSMessage {
  type: 'connected' | 'token' | 'done' | 'error' | 'limit_exceeded' | 'project_state' | 'agent_working' | 'file_created' | 'file_tree_update' | 'message_received' | 'thinking_start' | 'thinking' | 'thinking_end' | 'crew_init' | 'agent_started' | 'agent_completed' | 'crew_completed' | 'crew_continuation' | 'agent_failed' | string;
  content?: string;
  error?: string;
  // Limit exceeded fields
  limit_type?: 'chat' | 'project';
  used?: number;
  limit?: number;
  window_info?: {
    minutes_until_reset: number;
  };
  message?: string;
  // Project state fields
  project?: any;
  messages?: ChatMessage[];
  files?: ProjectFile[];
  // Agent fields
  agent?: string | {
    id: string;
    name: string;
    type: string;
    status?: string;
  };
  agents?: Array<{
    name: string;
    status: string;
  }>;
  // File tree fields
  tree?: FileTree;
  // CrewAI fields
  files_created?: number;
  total_files?: number;
  // Continuation fields
  can_continue?: boolean;
  completed_agents?: string[];
  failed_agent?: string;
  continuation_message?: string;
  [key: string]: any;
}
