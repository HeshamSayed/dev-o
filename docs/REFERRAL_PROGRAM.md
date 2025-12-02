# Referral Program - Feature Specification

## ⚠️ Implementation Status

**Status:** ❌ **NOT IMPLEMENTED**

The Referral Program was mentioned in the "Next Steps" section but has **NOT been built yet**. This document provides a complete specification for implementing it in the future.

---

## Overview

A referral program allows existing users to invite friends and earn rewards (extra usage quota, credits, or discounts) when their referrals sign up and upgrade to paid plans.

## Benefits

- **Viral growth**: Users become advocates
- **Lower customer acquisition cost**: Referrals convert better
- **User engagement**: Incentivizes continued platform use
- **Trust signals**: Friend recommendations are powerful

---

## Feature Specification

### Core Functionality

1. **Unique Referral Codes**
   - Each user gets a unique referral code (e.g., `DEV-O-ALEX123`)
   - Shareable link: `https://dev-o.ai/signup?ref=DEV-O-ALEX123`

2. **Rewards System**
   - **Referrer rewards**: When someone signs up with their code
   - **Referee rewards**: When new user signs up (welcome bonus)

3. **Reward Types**
   - Extra messages per window (e.g., +10 messages for 1 month)
   - Extra project requests (e.g., +5 requests for 1 month)
   - Account credits (e.g., $10 off next payment)
   - Extended features (e.g., unlock Pro features for 7 days)

4. **Tracking**
   - Track referral clicks
   - Track signups from referrals
   - Track upgrades (conversions)
   - Track reward redemptions

---

## Database Schema

### New Models

**File:** `backend/apps/billing/models.py`

```python
class ReferralCode(models.Model):
    """Unique referral code for each user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_code'
    )
    code = models.CharField(max_length=20, unique=True, db_index=True)

    # Stats
    clicks = models.IntegerField(default=0)
    signups = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)  # Upgrades to paid

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'billing_referral_code'

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class Referral(models.Model):
    """Track individual referrals."""

    STATUS_CHOICES = [
        ('clicked', 'Clicked'),
        ('signed_up', 'Signed Up'),
        ('converted', 'Converted to Paid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referrals_made'
    )
    referee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referred_by',
        null=True,
        blank=True
    )
    referral_code = models.ForeignKey(
        ReferralCode,
        on_delete=models.CASCADE,
        related_name='referrals'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='clicked')

    # Tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    clicked_at = models.DateTimeField(auto_now_add=True)
    signed_up_at = models.DateTimeField(null=True, blank=True)
    converted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'billing_referral'
        indexes = [
            models.Index(fields=['referrer', 'status']),
            models.Index(fields=['referral_code']),
        ]


class ReferralReward(models.Model):
    """Rewards earned from referrals."""

    REWARD_TYPES = [
        ('extra_messages', 'Extra Messages'),
        ('extra_requests', 'Extra Project Requests'),
        ('account_credit', 'Account Credit'),
        ('feature_unlock', 'Feature Unlock'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('redeemed', 'Redeemed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_rewards'
    )
    referral = models.ForeignKey(
        Referral,
        on_delete=models.CASCADE,
        related_name='rewards'
    )

    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Reward details
    amount = models.IntegerField(default=0)  # e.g., 10 messages, $10 credit
    description = models.TextField()

    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    redeemed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'billing_referral_reward'
```

---

## Implementation Steps

### Backend Implementation

#### 1. Generate Referral Codes

**File:** `backend/apps/billing/utils.py`

```python
import random
import string

def generate_referral_code(username: str) -> str:
    """Generate unique referral code."""
    # Create base from username
    base = username.upper()[:4] if len(username) >= 4 else username.upper()

    # Add random suffix
    suffix = ''.join(random.choices(string.digits, k=4))

    code = f"DEVO-{base}{suffix}"

    # Ensure uniqueness
    from apps.billing.models import ReferralCode
    while ReferralCode.objects.filter(code=code).exists():
        suffix = ''.join(random.choices(string.digits, k=4))
        code = f"DEVO-{base}{suffix}"

    return code
```

#### 2. Create Referral Code on User Signup

**File:** `backend/apps/accounts/signals.py`

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.billing.models import ReferralCode
from apps.billing.utils import generate_referral_code

User = get_user_model()

@receiver(post_save, sender=User)
def create_referral_code(sender, instance, created, **kwargs):
    """Create referral code when user signs up."""
    if created:
        code = generate_referral_code(instance.username)
        ReferralCode.objects.create(
            user=instance,
            code=code
        )
```

#### 3. Track Referral Clicks

**File:** `backend/apps/billing/views.py`

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def track_referral_click(request):
    """
    Track referral link click.

    POST /api/v1/billing/referral/track/
    Body: { "code": "DEVO-ALEX1234" }
    """
    code = request.data.get('code')

    try:
        referral_code = ReferralCode.objects.get(code=code)

        # Create referral tracking
        referral = Referral.objects.create(
            referrer=referral_code.user,
            referral_code=referral_code,
            status='clicked',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )

        # Increment click count
        referral_code.clicks += 1
        referral_code.save()

        # Store in session for signup attribution
        request.session['referral_id'] = str(referral.id)

        return Response({'success': True})

    except ReferralCode.DoesNotExist:
        return Response(
            {'error': 'Invalid referral code'},
            status=status.HTTP_404_NOT_FOUND
        )
```

#### 4. Attribute Signups

**File:** `backend/apps/accounts/views.py` (in signup view)

```python
def signup(request):
    # ... existing signup logic ...

    # After user is created
    referral_id = request.session.get('referral_id')
    if referral_id:
        try:
            referral = Referral.objects.get(id=referral_id)
            referral.referee = new_user
            referral.status = 'signed_up'
            referral.signed_up_at = timezone.now()
            referral.save()

            # Update referral code stats
            referral.referral_code.signups += 1
            referral.referral_code.save()

            # Give welcome bonus to new user
            create_welcome_bonus(new_user, referral)

            # Give reward to referrer
            create_referrer_reward(referral.referrer, referral)

        except Referral.DoesNotExist:
            pass
```

#### 5. Track Conversions

**File:** `backend/apps/billing/webhooks.py` (in handle_checkout_completed)

```python
def handle_checkout_completed(session):
    # ... existing code ...

    # Check if user was referred
    try:
        referral = Referral.objects.get(referee=user, status='signed_up')
        referral.status = 'converted'
        referral.converted_at = timezone.now()
        referral.save()

        # Update referral code stats
        referral.referral_code.conversions += 1
        referral.referral_code.save()

        # Give conversion bonus to referrer
        create_conversion_bonus(referral.referrer, referral)

    except Referral.DoesNotExist:
        pass
```

---

### Frontend Implementation

#### 1. Referral Dashboard Component

**File:** `frontend/src/components/ReferralDashboard/ReferralDashboard.tsx`

```typescript
const ReferralDashboard: React.FC = () => {
  const [referralCode, setReferralCode] = useState('');
  const [stats, setStats] = useState({ clicks: 0, signups: 0, conversions: 0 });
  const [rewards, setRewards] = useState([]);

  const referralLink = `${window.location.origin}/signup?ref=${referralCode}`;

  const copyLink = () => {
    navigator.clipboard.writeText(referralLink);
    // Show success toast
  };

  return (
    <div className="referral-dashboard">
      <h2>Refer Friends, Get Rewards!</h2>

      <div className="referral-link-section">
        <input value={referralLink} readOnly />
        <button onClick={copyLink}>Copy Link</button>
      </div>

      <div className="referral-stats">
        <div className="stat">
          <span className="stat-value">{stats.clicks}</span>
          <span className="stat-label">Clicks</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stats.signups}</span>
          <span className="stat-label">Signups</span>
        </div>
        <div className="stat">
          <span className="stat-value">{stats.conversions}</span>
          <span className="stat-label">Conversions</span>
        </div>
      </div>

      <div className="rewards-section">
        <h3>Your Rewards</h3>
        {rewards.map(reward => (
          <div key={reward.id} className="reward-card">
            <span>{reward.description}</span>
            <span>{reward.amount}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
```

#### 2. Track Referral on Signup Page

**File:** `frontend/src/pages/LoginPage.tsx`

```typescript
useEffect(() => {
  // Check for referral code in URL
  const params = new URLSearchParams(window.location.search);
  const refCode = params.get('ref');

  if (refCode) {
    // Track referral click
    axios.post('/api/v1/billing/referral/track/', { code: refCode })
      .catch(err => console.error('Failed to track referral:', err));
  }
}, []);
```

---

## Reward Suggestions

### For Referrer (Person Who Refers)

**On Signup:**
- +10 chat messages for next month
- +5 project requests for next month

**On Conversion (Referee upgrades to paid):**
- $10 account credit
- OR 1 month of Pro features free
- OR 50 bonus messages + 25 bonus requests

### For Referee (New User)

**On Signup with Referral Code:**
- +5 chat messages for first month
- +2 project requests for first month
- 7-day trial of Pro features

---

## Analytics & Reporting

Track and display:
- Total referrals made
- Conversion rate (signups → paid)
- Top referrers leaderboard
- Reward redemption rates
- Revenue generated from referrals

---

## Future Enhancements

1. **Tiered Rewards**: More referrals = better rewards
2. **Leaderboard**: Top referrers get special badges
3. **Social Sharing**: One-click share to Twitter, LinkedIn
4. **Email Templates**: Automated referral emails
5. **Expiring Rewards**: Create urgency
6. **Referral Contests**: Limited-time 2x rewards

---

## Cost-Benefit Analysis

**Costs:**
- Development time: ~40 hours
- Reward costs: $5-10 per conversion
- Infrastructure for tracking

**Benefits:**
- Lower CAC (Customer Acquisition Cost)
- Higher conversion rates (referred users convert 3-4x better)
- Viral coefficient > 1 = exponential growth
- Community building

**ROI:** Typically 300-500% for well-executed referral programs

---

## Implementation Priority

**Phase 1 (MVP):**
- Basic referral code generation
- Click tracking
- Signup attribution
- Simple rewards (extra messages)

**Phase 2:**
- Referral dashboard
- Advanced analytics
- Tiered rewards
- Leaderboard

**Phase 3:**
- Social sharing
- Automated emails
- Contest system
- A/B testing

---

## Conclusion

The Referral Program is **NOT currently implemented** but is a high-value feature for growth. This specification provides everything needed to build it when ready.

**Estimated Implementation Time:** 3-5 days for Phase 1 MVP

---

**Status:** 📋 Specification Only (Not Implemented)
**Priority:** High (for growth phase)
**Last Updated:** 2025-01-XX
