class Ticket:
    def __init__(self, ticket_amount) -> None:
        self.ticket_amount = ticket_amount

    @property
    def tickets(self):
        return self.ticket_amount if self.ticket_amount >= 0 else 0
    
    def __str__(self) -> str:
        return self.tickets
