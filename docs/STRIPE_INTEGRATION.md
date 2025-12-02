# Stripe Integration Guide for DEV-O

This guide provides step-by-step instructions for integrating Stripe payment processing into the DEV-O platform.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Webhook Configuration](#webhook-configuration)
5. [Testing](#testing)
6. [Production Deployment](#production-deployment)

---

## Prerequisites

### 1. Create Stripe Account

1. Sign up at [https://stripe.com](https://stripe.com)
2. Complete account verification
3. Get your API keys from [Dashboard → Developers → API Keys](https://dashboard.stripe.com/apikeys)
   - **Publishable key** (starts with `pk_test_` or `pk_live_`)
   - **Secret key** (starts with `sk_test_` or `sk_live_`)

### 2. Install Stripe Dependencies

**Backend:**
```bash
cd backend
pip install stripe==8.0.0
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install @stripe/stripe-js @stripe/react-stripe-js
```

---

## Backend Setup

### Step 1: Add Stripe Configuration

**File:** `backend/config/settings.py`

```python
# Add to settings.py

# Stripe Configuration
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

# Stripe Price IDs (create these in Stripe Dashboard)
STRIPE_PRICE_IDS = {
    'pro_monthly': os.getenv('STRIPE_PRICE_ID_PRO_MONTHLY', ''),
    'pro_yearly': os.getenv('STRIPE_PRICE_ID_PRO_YEARLY', ''),
    'team_monthly': os.getenv('STRIPE_PRICE_ID_TEAM_MONTHLY', ''),
    'team_yearly': os.getenv('STRIPE_PRICE_ID_TEAM_YEARLY', ''),
}
```

**File:** `.env`

```bash
# Add to .env file

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Stripe Price IDs (get these from Stripe Dashboard)
STRIPE_PRICE_ID_PRO_MONTHLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_ID_PRO_YEARLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_ID_TEAM_MONTHLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_ID_TEAM_YEARLY=price_xxxxxxxxxxxxx
```

### Step 2: Create Stripe Service

**File:** `backend/services/stripe_service.py`

```python
"""
Stripe payment processing service.
"""

import stripe
from django.conf import settings
from typing import Dict, Optional

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Service for handling Stripe operations."""

    @staticmethod
    def create_checkout_session(
        user_email: str,
        plan_type: str,
        billing_cycle: str,
        success_url: str,
        cancel_url: str,
    ) -> Dict:
        """
        Create Stripe Checkout Session.

        Args:
            user_email: User's email address
            plan_type: 'pro' or 'team'
            billing_cycle: 'monthly' or 'yearly'
            success_url: URL to redirect after success
            cancel_url: URL to redirect after cancel

        Returns:
            Dictionary with session_id and checkout_url
        """
        # Get price ID from settings
        price_key = f"{plan_type}_{billing_cycle}"
        price_id = settings.STRIPE_PRICE_IDS.get(price_key)

        if not price_id:
            raise ValueError(f"No Stripe price configured for {price_key}")

        try:
            # Create Checkout Session
            session = stripe.checkout.Session.create(
                customer_email=user_email,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                metadata={
                    'plan_type': plan_type,
                    'billing_cycle': billing_cycle,
                    'user_email': user_email,
                },
                allow_promotion_codes=True,  # Allow discount codes
                billing_address_collection='required',
            )

            return {
                'session_id': session.id,
                'checkout_url': session.url,
            }

        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def create_customer_portal_session(
        stripe_customer_id: str,
        return_url: str,
    ) -> Dict:
        """
        Create Customer Portal Session for managing subscription.

        Args:
            stripe_customer_id: Stripe customer ID
            return_url: URL to return after portal session

        Returns:
            Dictionary with portal_url
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=stripe_customer_id,
                return_url=return_url,
            )

            return {'portal_url': session.url}

        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    @staticmethod
    def get_subscription(subscription_id: str) -> Optional[Dict]:
        """
        Retrieve subscription details from Stripe.

        Args:
            subscription_id: Stripe subscription ID

        Returns:
            Subscription data or None
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_start': subscription.current_period_start,
                'current_period_end': subscription.current_period_end,
                'cancel_at_period_end': subscription.cancel_at_period_end,
                'customer': subscription.customer,
            }
        except stripe.error.StripeError:
            return None

    @staticmethod
    def cancel_subscription(subscription_id: str, at_period_end: bool = True) -> Dict:
        """
        Cancel a subscription.

        Args:
            subscription_id: Stripe subscription ID
            at_period_end: Cancel at period end (True) or immediately (False)

        Returns:
            Updated subscription data
        """
        try:
            if at_period_end:
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True,
                )
            else:
                subscription = stripe.Subscription.delete(subscription_id)

            return {
                'status': subscription.status,
                'cancel_at_period_end': subscription.cancel_at_period_end,
            }

        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")
```

### Step 3: Update Billing Views

**File:** `backend/apps/billing/views.py`

Add these methods to your existing `SubscriptionViewSet`:

```python
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from services.stripe_service import StripeService

class SubscriptionViewSet(viewsets.ModelViewSet):
    # ... existing code ...

    @action(detail=False, methods=['post'])
    def create_checkout_session(self, request):
        """
        Create Stripe Checkout Session for subscription.

        POST /api/v1/billing/subscriptions/create_checkout_session/
        Body: {
            "plan_type": "pro",
            "billing_cycle": "monthly"
        }
        """
        plan_type = request.data.get('plan_type')
        billing_cycle = request.data.get('billing_cycle', 'monthly')

        if plan_type not in ['pro', 'team']:
            return Response(
                {'error': 'Invalid plan type. Must be "pro" or "team".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if billing_cycle not in ['monthly', 'yearly']:
            return Response(
                {'error': 'Invalid billing cycle. Must be "monthly" or "yearly".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already has active subscription
        if hasattr(request.user, 'subscription') and request.user.subscription.is_active:
            return Response(
                {'error': 'You already have an active subscription. Please cancel it first.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            stripe_service = StripeService()
            session_data = stripe_service.create_checkout_session(
                user_email=request.user.email,
                plan_type=plan_type,
                billing_cycle=billing_cycle,
                success_url=f"{settings.FRONTEND_URL}/subscription/success",
                cancel_url=f"{settings.FRONTEND_URL}/pricing",
            )

            return Response(session_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def create_portal_session(self, request):
        """
        Create Stripe Customer Portal Session.

        POST /api/v1/billing/subscriptions/create_portal_session/
        """
        try:
            subscription = request.user.subscription

            if not subscription.stripe_customer_id:
                return Response(
                    {'error': 'No Stripe customer found for this user.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            stripe_service = StripeService()
            portal_data = stripe_service.create_customer_portal_session(
                stripe_customer_id=subscription.stripe_customer_id,
                return_url=f"{settings.FRONTEND_URL}/account",
            )

            return Response(portal_data, status=status.HTTP_200_OK)

        except Subscription.DoesNotExist:
            return Response(
                {'error': 'No subscription found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def config(self, request):
        """
        Get Stripe publishable key for frontend.

        GET /api/v1/billing/subscriptions/config/
        """
        return Response({
            'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        })
```

### Step 4: Create Webhook Handler

**File:** `backend/apps/billing/webhooks.py`

```python
"""
Stripe webhook handlers.
"""

import stripe
import logging
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import Subscription, Plan

User = get_user_model()
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handle Stripe webhooks.

    Webhook URL: https://yourdomain.com/api/v1/billing/webhook/
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid webhook payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid webhook signature")
        return HttpResponse(status=400)

    # Handle the event
    event_type = event['type']
    data = event['data']['object']

    logger.info(f"Received Stripe webhook: {event_type}")

    # Checkout session completed - create subscription
    if event_type == 'checkout.session.completed':
        handle_checkout_completed(data)

    # Subscription created
    elif event_type == 'customer.subscription.created':
        handle_subscription_created(data)

    # Subscription updated
    elif event_type == 'customer.subscription.updated':
        handle_subscription_updated(data)

    # Subscription deleted (canceled)
    elif event_type == 'customer.subscription.deleted':
        handle_subscription_deleted(data)

    # Payment succeeded
    elif event_type == 'invoice.payment_succeeded':
        handle_payment_succeeded(data)

    # Payment failed
    elif event_type == 'invoice.payment_failed':
        handle_payment_failed(data)

    return JsonResponse({'status': 'success'})


def handle_checkout_completed(session):
    """Handle successful checkout session."""
    customer_email = session.get('customer_email')
    subscription_id = session.get('subscription')
    customer_id = session.get('customer')
    metadata = session.get('metadata', {})

    try:
        user = User.objects.get(email=customer_email)
        plan_type = metadata.get('plan_type', 'pro')
        billing_cycle = metadata.get('billing_cycle', 'monthly')

        # Get plan
        plan = Plan.objects.get(plan_type=plan_type)

        # Get subscription details from Stripe
        stripe_subscription = stripe.Subscription.retrieve(subscription_id)

        # Create or update subscription
        subscription, created = Subscription.objects.update_or_create(
            user=user,
            defaults={
                'plan': plan,
                'status': 'active',
                'billing_cycle': billing_cycle,
                'stripe_subscription_id': subscription_id,
                'stripe_customer_id': customer_id,
                'current_period_start': timezone.datetime.fromtimestamp(
                    stripe_subscription.current_period_start
                ),
                'current_period_end': timezone.datetime.fromtimestamp(
                    stripe_subscription.current_period_end
                ),
            }
        )

        logger.info(f"Subscription {'created' if created else 'updated'} for {user.email}")

    except User.DoesNotExist:
        logger.error(f"User not found: {customer_email}")
    except Plan.DoesNotExist:
        logger.error(f"Plan not found: {plan_type}")
    except Exception as e:
        logger.error(f"Error handling checkout: {str(e)}")


def handle_subscription_created(subscription):
    """Handle subscription creation."""
    logger.info(f"Subscription created: {subscription.id}")
    # Usually handled in checkout.session.completed


def handle_subscription_updated(subscription):
    """Handle subscription updates."""
    subscription_id = subscription.id
    status = subscription.status

    try:
        sub = Subscription.objects.get(stripe_subscription_id=subscription_id)
        sub.status = status
        sub.current_period_start = timezone.datetime.fromtimestamp(
            subscription.current_period_start
        )
        sub.current_period_end = timezone.datetime.fromtimestamp(
            subscription.current_period_end
        )

        if subscription.cancel_at_period_end:
            sub.cancelled_at = timezone.now()

        sub.save()
        logger.info(f"Subscription updated: {subscription_id}")

    except Subscription.DoesNotExist:
        logger.error(f"Subscription not found: {subscription_id}")


def handle_subscription_deleted(subscription):
    """Handle subscription cancellation."""
    subscription_id = subscription.id

    try:
        sub = Subscription.objects.get(stripe_subscription_id=subscription_id)
        sub.status = 'cancelled'
        sub.cancelled_at = timezone.now()
        sub.save()
        logger.info(f"Subscription cancelled: {subscription_id}")

    except Subscription.DoesNotExist:
        logger.error(f"Subscription not found: {subscription_id}")


def handle_payment_succeeded(invoice):
    """Handle successful payment."""
    subscription_id = invoice.get('subscription')

    try:
        sub = Subscription.objects.get(stripe_subscription_id=subscription_id)
        sub.status = 'active'
        sub.save()
        logger.info(f"Payment succeeded for subscription: {subscription_id}")

    except Subscription.DoesNotExist:
        logger.error(f"Subscription not found: {subscription_id}")


def handle_payment_failed(invoice):
    """Handle failed payment."""
    subscription_id = invoice.get('subscription')

    try:
        sub = Subscription.objects.get(stripe_subscription_id=subscription_id)
        sub.status = 'past_due'
        sub.save()
        logger.info(f"Payment failed for subscription: {subscription_id}")

    except Subscription.DoesNotExist:
        logger.error(f"Subscription not found: {subscription_id}")
```

### Step 5: Add Webhook URL

**File:** `backend/apps/billing/urls.py`

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionViewSet, UsageViewSet, UsageLogViewSet
from .webhooks import stripe_webhook

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'usage', UsageViewSet, basename='usage')
router.register(r'logs', UsageLogViewSet, basename='usage-log')

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', stripe_webhook, name='stripe-webhook'),  # NEW
]
```

### Step 6: Add Frontend URL to Settings

**File:** `backend/config/settings.py`

```python
# Frontend URL for redirects
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
```

**File:** `.env`

```bash
FRONTEND_URL=http://localhost:3000
```

---

## Frontend Setup

### Step 1: Update Billing API

**File:** `frontend/src/api/billing.ts`

Add these methods:

```typescript
export const billingAPI = {
  // ... existing methods ...

  /**
   * Get Stripe configuration (publishable key).
   */
  async getStripeConfig(): Promise<{ publishable_key: string }> {
    const response = await apiClient.get('/billing/subscriptions/config/');
    return response.data;
  },

  /**
   * Create Stripe Checkout Session.
   */
  async createCheckoutSession(
    planType: 'pro' | 'team',
    billingCycle: 'monthly' | 'yearly'
  ): Promise<{ session_id: string; checkout_url: string }> {
    const response = await apiClient.post('/billing/subscriptions/create_checkout_session/', {
      plan_type: planType,
      billing_cycle: billingCycle,
    });
    return response.data;
  },

  /**
   * Create Stripe Customer Portal Session.
   */
  async createPortalSession(): Promise<{ portal_url: string }> {
    const response = await apiClient.post('/billing/subscriptions/create_portal_session/');
    return response.data;
  },
};
```

### Step 2: Update PricingPage

**File:** `frontend/src/pages/PricingPage.tsx`

Replace the `handleSelectPlan` function:

```typescript
const handleSelectPlan = async (plan: Plan) => {
  // Enterprise - contact sales
  if (plan.plan_type === 'enterprise') {
    window.location.href = 'mailto:sales@dev-o.ai?subject=Enterprise Plan Inquiry';
    return;
  }

  // Free plan - just inform user they're already on it
  if (plan.plan_type === 'free') {
    alert('You are currently on the Free plan. Sign up to get started!');
    return;
  }

  // Pro or Team - create Stripe checkout session
  try {
    setLoading(true);

    const { checkout_url } = await billingAPI.createCheckoutSession(
      plan.plan_type as 'pro' | 'team',
      billingCycle
    );

    // Redirect to Stripe Checkout
    window.location.href = checkout_url;

  } catch (error: any) {
    console.error('Failed to create checkout session:', error);
    alert(error.response?.data?.error || 'Failed to start checkout. Please try again.');
  } finally {
    setLoading(false);
  }
};
```

Add loading state at the top of component:

```typescript
const [loading, setLoading] = useState(false);
```

Update the button to show loading state:

```typescript
<button
  className="select-plan-btn"
  onClick={() => handleSelectPlan(plan)}
  disabled={loading}
>
  {loading ? 'Loading...' :
   plan.plan_type === 'free' ? 'Get Started' :
   plan.plan_type === 'enterprise' ? 'Contact Sales' :
   'Upgrade Now'}
</button>
```

### Step 3: Create Success Page

**File:** `frontend/src/pages/SubscriptionSuccess.tsx`

```typescript
import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Logo from '../components/Logo/Logo';
import './SubscriptionSuccess.css';

const SubscriptionSuccess: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    // Countdown redirect
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          navigate('/chat');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [navigate]);

  return (
    <div className="subscription-success">
      <div className="success-card">
        <Logo size={100} />

        <div className="success-icon">✅</div>

        <h1>Subscription Successful!</h1>

        <p className="success-message">
          Thank you for upgrading to DEV-O Pro/Team!
          Your subscription is now active.
        </p>

        <div className="success-details">
          <div className="detail-item">
            <span className="detail-icon">🚀</span>
            <span>All 4 expert AI agents unlocked</span>
          </div>
          <div className="detail-item">
            <span className="detail-icon">⚡</span>
            <span>10x-50x more capacity per window</span>
          </div>
          <div className="detail-item">
            <span className="detail-icon">✨</span>
            <span>Advanced features enabled</span>
          </div>
        </div>

        <div className="redirect-info">
          Redirecting to chat in {countdown} seconds...
        </div>

        <button
          className="go-to-chat-btn"
          onClick={() => navigate('/chat')}
        >
          Go to Chat Now
        </button>

        {sessionId && (
          <p className="session-id">
            Session ID: {sessionId}
          </p>
        )}
      </div>
    </div>
  );
};

export default SubscriptionSuccess;
```

**File:** `frontend/src/pages/SubscriptionSuccess.css`

```css
.subscription-success {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0B1220 0%, #1E293B 100%);
  padding: 20px;
}

.success-card {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 20px;
  padding: 60px 40px;
  max-width: 600px;
  text-align: center;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
}

.success-icon {
  font-size: 80px;
  margin: 20px 0;
  animation: scaleIn 0.5s ease;
}

@keyframes scaleIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

.success-card h1 {
  font-size: 32px;
  color: #60a5fa;
  margin-bottom: 16px;
}

.success-message {
  font-size: 18px;
  color: #cbd5e1;
  margin-bottom: 40px;
  line-height: 1.6;
}

.success-details {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  color: #e2e8f0;
  font-size: 16px;
}

.detail-icon {
  font-size: 24px;
}

.redirect-info {
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 20px;
}

.go-to-chat-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.go-to-chat-btn:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.5);
}

.session-id {
  margin-top: 20px;
  font-size: 11px;
  color: #64748b;
}
```

### Step 4: Add Route for Success Page

**File:** `frontend/src/App.tsx`

```typescript
import SubscriptionSuccess from './pages/SubscriptionSuccess';

// Add this route
<Route path="/subscription/success" element={<SubscriptionSuccess />} />
```

### Step 5: Add Manage Subscription Button

Add to user account/settings page:

```typescript
const handleManageSubscription = async () => {
  try {
    const { portal_url } = await billingAPI.createPortalSession();
    window.location.href = portal_url;
  } catch (error) {
    console.error('Failed to open portal:', error);
  }
};

<button onClick={handleManageSubscription}>
  Manage Subscription
</button>
```

---

## Webhook Configuration

### Step 1: Create Stripe Products and Prices

1. Go to [Stripe Dashboard → Products](https://dashboard.stripe.com/products)
2. Create products for each plan:

**Pro Plan**:
- Name: "DEV-O Pro"
- Monthly price: $19
- Yearly price: $190 (save price ID)

**Team Plan**:
- Name: "DEV-O Team"
- Monthly price: $49
- Yearly price: $490 (save price ID)

3. Copy the Price IDs and add them to your `.env` file

### Step 2: Set Up Webhook Endpoint

#### For Local Development (using Stripe CLI):

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login to Stripe
stripe login

# Forward webhooks to local server
stripe listen --forward-to http://localhost:8001/api/v1/billing/webhook/

# Copy the webhook signing secret (starts with whsec_) to .env
```

#### For Production:

1. Go to [Stripe Dashboard → Developers → Webhooks](https://dashboard.stripe.com/webhooks)
2. Click "Add endpoint"
3. Enter your webhook URL: `https://yourdomain.com/api/v1/billing/webhook/`
4. Select events to listen for:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
5. Copy the signing secret to your production `.env` file

---

## Testing

### Test Mode

1. Use Stripe test mode keys (start with `pk_test_` and `sk_test_`)
2. Use test card numbers from [Stripe Testing Documentation](https://stripe.com/docs/testing):
   - **Success:** `4242 4242 4242 4242`
   - **Decline:** `4000 0000 0000 0002`
   - **3D Secure:** `4000 0027 6000 3184`
   - Any future expiry date, any CVC, any ZIP

### Testing Checklist

- [ ] Create checkout session successfully
- [ ] Complete payment with test card
- [ ] Verify subscription created in database
- [ ] Check webhook events received
- [ ] Test subscription status updates
- [ ] Test subscription cancellation
- [ ] Test customer portal access
- [ ] Verify usage limits update based on plan
- [ ] Test upgrade flow (Free → Pro → Team)
- [ ] Test payment failure scenario

---

## Production Deployment

### Pre-Deployment Checklist

1. **Switch to Live Keys**
   ```bash
   # Update .env with live keys
   STRIPE_SECRET_KEY=sk_live_...
   STRIPE_PUBLISHABLE_KEY=pk_live_...
   ```

2. **Update Price IDs**
   - Create live products in Stripe
   - Update `.env` with live price IDs

3. **Configure Live Webhook**
   - Add production webhook endpoint in Stripe Dashboard
   - Update `STRIPE_WEBHOOK_SECRET` with live secret

4. **Test Production Flow**
   - Test with real card (then refund)
   - Verify webhooks are received
   - Check subscription creation

5. **Security**
   - Use HTTPS for all endpoints
   - Verify webhook signatures
   - Rate limit webhook endpoint
   - Monitor for suspicious activity

6. **Monitoring**
   - Set up Stripe Dashboard notifications
   - Monitor webhook logs
   - Track failed payments
   - Set up alerts for errors

### Environment Variables Summary

```bash
# Production .env
STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx

STRIPE_PRICE_ID_PRO_MONTHLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_ID_PRO_YEARLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_ID_TEAM_MONTHLY=price_xxxxxxxxxxxxx
STRIPE_PRICE_ID_TEAM_YEARLY=price_xxxxxxxxxxxxx

FRONTEND_URL=https://dev-o.ai
```

---

## Troubleshooting

### Common Issues

**Webhook not receiving events:**
- Check webhook URL is correct
- Verify webhook secret matches
- Check firewall/security rules
- Use Stripe CLI for local testing

**Checkout session creation fails:**
- Verify price IDs are correct
- Check API keys are set
- Ensure user email is valid

**Subscription not created:**
- Check webhook handler logs
- Verify database connection
- Check user exists in database

**Payment fails:**
- Use test cards correctly
- Check card details validation
- Verify 3D Secure handling

---

## Support

- **Stripe Documentation:** [https://stripe.com/docs](https://stripe.com/docs)
- **Stripe Support:** [https://support.stripe.com](https://support.stripe.com)
- **DEV-O Support:** support@dev-o.ai

---

**Last Updated:** 2025-01-XX
