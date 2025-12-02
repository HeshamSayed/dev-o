/**
 * Referral API client
 */

import api from './client';

export interface ReferralCode {
  id: string;
  code: string;
  referral_link: string;
  clicks: number;
  signups: number;
  conversions: number;
  created_at: string;
}

export interface Referral {
  id: string;
  referrer_email: string;
  referee_email: string | null;
  status: 'clicked' | 'signed_up' | 'converted';
  clicked_at: string;
  signed_up_at: string | null;
  converted_at: string | null;
}

export interface ReferralReward {
  id: string;
  reward_type: 'extra_messages' | 'extra_requests' | 'discount' | 'free_upgrade';
  amount: number;
  description: string;
  status: 'pending' | 'active' | 'redeemed' | 'expired';
  valid_from: string;
  valid_until: string;
  is_valid: boolean;
  days_remaining: number | null;
  created_at: string;
  redeemed_at: string | null;
}

export interface ReferralStats {
  code: string;
  referral_link: string;
  total_clicks: number;
  total_signups: number;
  total_conversions: number;
  conversion_rate: number;
  total_rewards: number;
  active_rewards: number;
  referrals: Referral[];
}

export interface BonusQuota {
  messages: number;
  requests: number;
}

/**
 * Get user's referral code
 */
export const getMyReferralCode = async (): Promise<ReferralCode> => {
  const response = await api.get('/billing/referrals/my_code/');
  return response.data;
};

/**
 * Get comprehensive referral stats
 */
export const getReferralStats = async (): Promise<ReferralStats> => {
  const response = await api.get('/billing/referrals/stats/');
  return response.data;
};

/**
 * Get all referrals made by user
 */
export const getReferrals = async (): Promise<Referral[]> => {
  const response = await api.get('/billing/referrals/');
  return response.data;
};

/**
 * Get all rewards for user
 */
export const getRewards = async (): Promise<ReferralReward[]> => {
  const response = await api.get('/billing/rewards/');
  return response.data;
};

/**
 * Get active rewards for user
 */
export const getActiveRewards = async (): Promise<ReferralReward[]> => {
  const response = await api.get('/billing/rewards/active/');
  return response.data;
};

/**
 * Get bonus quota from active rewards
 */
export const getBonusQuota = async (): Promise<BonusQuota> => {
  const response = await api.get('/billing/rewards/bonus_quota/');
  return response.data;
};

/**
 * Track referral click (called when user clicks referral link)
 * This is a public endpoint that doesn't require authentication
 */
export const trackReferralClick = async (referralCode: string): Promise<{ referral_id: string }> => {
  const response = await api.post('/billing/referrals/track/', {
    referral_code: referralCode,
  });
  return response.data;
};
