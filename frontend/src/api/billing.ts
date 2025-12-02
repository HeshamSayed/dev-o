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

export interface Subscription {
  id: string;
  user: string;
  plan: Plan;
  status: 'active' | 'cancelled' | 'expired' | 'past_due' | 'trialing';
  billing_cycle: 'monthly' | 'yearly';
  stripe_subscription_id?: string;
  stripe_customer_id?: string;
  current_period_start: string;
  current_period_end: string;
  trial_end?: string;
  cancelled_at?: string;
  created_at: string;
  updated_at: string;
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

export interface UsageTracker {
  id: string;
  user: string;
  window_start: string;
  window_end: string;
  chat_messages_used: number;
  chat_tokens_used: number;
  project_requests_used: number;
  project_tokens_used: number;
  storage_used_bytes: number;
  created_at: string;
  updated_at: string;
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
   * Get specific plan by ID.
   */
  async getPlan(id: string): Promise<Plan> {
    const response = await apiClient.get(`/billing/plans/${id}/`);
    return response.data;
  },

  /**
   * Get current user's subscription.
   */
  async getCurrentSubscription(): Promise<Subscription | null> {
    const response = await apiClient.get('/billing/subscriptions/current/');
    return response.data.subscription || null;
  },

  /**
   * Create new subscription.
   */
  async createSubscription(planId: string, billingCycle: 'monthly' | 'yearly'): Promise<Subscription> {
    const response = await apiClient.post('/billing/subscriptions/', {
      plan_id: planId,
      billing_cycle: billingCycle,
    });
    return response.data;
  },

  /**
   * Get current usage summary with limits and time until reset.
   */
  async getUsageSummary(): Promise<UsageSummary> {
    const response = await apiClient.get('/billing/usage/summary/');
    return response.data;
  },

  /**
   * Get usage for current 2-hour window.
   */
  async getCurrentWindow(): Promise<UsageTracker> {
    const response = await apiClient.get('/billing/usage/current_window/');
    return response.data;
  },

  /**
   * Get usage history.
   */
  async getUsageHistory(days: number = 7, limit: number = 50): Promise<UsageTracker[]> {
    const response = await apiClient.get('/billing/usage/history/', {
      params: { days, limit },
    });
    return response.data;
  },

  /**
   * Get detailed usage logs.
   */
  async getUsageLogs(days: number = 7, type?: string): Promise<any[]> {
    const response = await apiClient.get('/billing/logs/', {
      params: { days, type },
    });
    return response.data;
  },
};

export default billingAPI;
