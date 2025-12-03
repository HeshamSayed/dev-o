/**
 * Billing and subscription API endpoints.
 */

import apiClient from './client';

export interface Plan {
  id: string;
  name: string;
  plan_type: 'free' | 'pro' | 'team' | 'enterprise';
  price_monthly: number;
  price_yearly: number;
  messages_per_window: number;
  max_conversations: number;
  context_window: number;
  max_active_projects: number;
  max_archived_projects: number;
  max_files_per_project: number;
  project_requests_per_window: number;
  available_agents: string[];
  max_concurrent_agents: number;
  storage_limit_mb: number;
  max_file_size_kb: number;
  retention_days: number;
  model_tier: string;
  max_output_tokens: number;
  requests_per_minute: number;
  max_concurrent_connections: number;
  queue_priority: number;
  has_thinking_mode: boolean;
  has_download: boolean;
  has_git_integration: boolean;
  has_api_access: boolean;
  has_chat_search: boolean;
  is_active: boolean;
}

export interface UsageSummary {
  plan: {
    name: string;
    type: string;
  };
  window: {
    start: string;
    end: string;
    minutes_until_reset: number;
  };
  chat: {
    used: number;
    limit: number;
    remaining: number;
  };
  projects: {
    used: number;
    limit: number;
    remaining: number;
  };
  features: {
    thinking_mode: boolean;
    download: boolean;
    git_integration: boolean;
    api_access: boolean;
    chat_search: boolean;
  };
}

export const billingAPI = {
  /**
   * Get all available pricing plans.
   */
  async getPlans(): Promise<Plan[]> {
    const response = await apiClient.get('/billing/plans/');
    // Handle paginated response from DRF
    const data: any = response.data;
    return data.results || data;
  },

  /**
   * Get current usage summary with limits and time until reset.
   */
  async getUsageSummary(): Promise<UsageSummary> {
    const response = await apiClient.get('/billing/usage/summary/');
    return response.data;
  },
};

export default billingAPI;
