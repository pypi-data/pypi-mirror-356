from client import SpireClient
from sales import *
from customers import *
from inventory import InventoryClient

class Spire:
    def __init__(self, company : str, username : str, password : str):
        self.client = SpireClient(company, username, password)
        self.orders = OrdersClient(self.client)
        self.invoices = InvoiceClient(self.client)
        self.customers = CustomerClient(self.client)
        self.inventory = InventoryClient(self.client)


