from django.core.mail import EmailMessage


def send_email(order):
    subject = f"Order #{order.id} status update"
    message = f"Your order #{order.id} status has been updated to {order.status}"
    to = [order.user.email]
    email = EmailMessage(subject, message, to=to)
    email.send()
