
"""
>Cannot Convert Invoice to Quote
>Inactive Item
>invalide Syntax for date time
>A database error has occurred:\n\nA value passed to the database was too long for the column - Country Name 
>Order Number Exists
>Invalid Customer
>Missing Parent/Child errror -> id of addresses

Contacts 3
Request Failure
Not Found
invalid Field for filter


{'status_code': 422, 'url': 'https://red-wave-8362.spirelan.com:10880/api/v2/companies/intertest/sales/orders/31308/invoice', 
'content': {'type': 'error', 'message': 'Cannot post a deleted order', 'traceback': '', 'error_type': 'BusinessViolationError'}}
"""

class CreateRequestError(Exception):
    """
    Exception raised when a create (POST) request to the API fails.
    """

    def __init__(self, endpoint: str, status_code: int, error_message: str = "", response_body: dict = None):
        self.endpoint = endpoint
        self.status_code = status_code
        self.error_message = error_message or "Unknown error occurred"
        self.response_body = response_body or {}

        super().__init__(self.__str__())

    def __str__(self):
        return (
            f"Create request to '{self.endpoint}' failed with status {self.status_code}: {self.error_message}"
        )

    def to_dict(self):
        return {
            "endpoint": self.endpoint,
            "status_code": self.status_code,
            "error_message": self.error_message,
            "response_body": self.response_body,
        }