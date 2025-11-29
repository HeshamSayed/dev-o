// Type definitions for the application

export interface Agent {
  id: string;
  name: string;
  role: string;
  level: number;
  description: string;
  color: string;
}

export interface Feature {
  title: string;
  description: string;
  icon: string;
  gradient: string;
}

export interface AgentMessage {
  agent: string;
  message: string;
  timestamp: number;
  type: 'thinking' | 'action' | 'result';
}
