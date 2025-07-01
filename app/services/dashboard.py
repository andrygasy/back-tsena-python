from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import User, Order, Product

def get_stats(session: Session) -> dict:
    total_users = session.scalar(select(func.count()).select_from(User))
    total_orders = session.scalar(select(func.count()).select_from(Order))
    total_revenue = session.scalar(select(func.sum(Order.total))) or 0
    active_products = session.scalar(
        select(func.count()).select_from(Product).where(Product.status == 'active')
    )
    pending_requests = session.scalar(
        select(func.count()).select_from(Product).where(Product.status == 'pending')
    )
    return {
        'total_users': total_users or 0,
        'total_orders': total_orders or 0,
        'total_revenue': float(total_revenue or 0),
        'active_products': active_products or 0,
        'pending_requests': pending_requests or 0,
    }
