import stripe
import os
from fastapi import HTTPException

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_51234567890abcdef")

class StripeService:
    @staticmethod
    def create_payment_intent(amount_cents: int, currency: str = "usd", metadata: dict = None):
        """Create a Stripe payment intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return intent
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    
    @staticmethod
    def confirm_payment(payment_intent_id: str):
        """Confirm a payment intent"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return intent.status == "succeeded"
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    
    @staticmethod
    def create_checkout_session(
        amount_cents: int, 
        success_url: str, 
        cancel_url: str,
        metadata: dict = None
    ):
        """Create a Stripe checkout session"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Dataset Purchase',
                            'description': f"Purchase of {metadata.get('rows', 0)} data rows"
                        },
                        'unit_amount': amount_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata or {}
            )
            return session
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")