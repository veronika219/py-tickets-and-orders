from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession

from django.db.models import QuerySet


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None,
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date
            order.save()

        tickets_ = [
            Ticket(
                order=order,
                movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
                row=ticket["row"],
                seat=ticket["seat"],
            )
            for ticket in tickets
        ]

        order.ticket_set.bulk_create(tickets_)
        return order


def get_orders(username: str = None) -> QuerySet:
    with transaction.atomic():
        if username:
            return Order.objects.filter(user__username=username)
        else:
            return Order.objects.all()
