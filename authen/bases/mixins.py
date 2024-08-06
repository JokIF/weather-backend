from django.db.models import Model, BooleanField
from django.db.models.functions import Now

from authen.utils.tickets import Ticket

from datetime import timedelta


class TicketsMixin:
    def get_tickets(self):
        return Ticket(5 - self.gis_response.filter(time_at__gte=Now()-timedelta(days=1)).count()) # 5 заменить
