import apiClient from './client';

export interface UserProfile {
  display_name?: string;
  show_thinking: boolean;
  theme: string;
  preferences: Record<string, any>;
}

export interface User {
  id: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  profile?: UserProfile;
}

export const userApi = {
  // Get current user
  getMe: () => apiClient.get<User>('/users/me/'),

  // Update user profile
  updateProfile: (data: Partial<UserProfile>) =>
    apiClient.patch<User>('/users/update_profile/', data),
};

export default userApi;