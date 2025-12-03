import api from './client';

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface ConversationDetail extends Conversation {
  messages: Message[];
}

export const chatApi = {
  // Get all conversations
  getConversations: () => api.get<Conversation[]>('/conversations/'),

  // Get conversation with messages
  getConversation: (id: string) => api.get<ConversationDetail>(`/conversations/${id}/`),

  // Create new conversation
  createConversation: (title: string = 'New Chat') =>
    api.post<Conversation>('/conversations/', { title }),

  // Delete conversation
  deleteConversation: (id: string) => api.delete(`/conversations/${id}/`),
};
