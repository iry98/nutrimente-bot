import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
SUBSCRIBED_USERS = set()  # Solo per test – in produzione usa un database

def create_checkout_session(chat_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity": 1
        }],
        mode="subscription",
        success_url="https://t.me/ILTUOBOT?start=abbonato",
        cancel_url="https://t.me/ILTUOBOT",
        metadata={"chat_id": chat_id}
    )
    SUBSCRIBED_USERS.add(chat_id)
    return session.url

def is_user_subscribed(chat_id):
    return chat_id in SUBSCRIBED_USERS
