import requests
from config import BASE_URL
from typing import TypeVar, Optional, Type, Generic, List, Union, Tuple, Dict, Any
from pydantic import BaseModel
import json
import urllib.parse

T = TypeVar('T', bound=BaseModel)

class SpireClient():
    
    def __init__(self, company, username, password,):
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({
            "accept": "application/json",
            "content-type": "application/json"
        })
        self.base_url = f"{BASE_URL}/{company}"

    def _get(self, endpoint, params=None):

        """
        Send a GET request to the Spire API.

        This method constructs the full URL using the provided endpoint,
        sends an HTTP GET request with optional query parameters, and returns
        the parsed JSON response. Raises an HTTPError if the response contains
        an unsuccessful status code.

        Args:
            endpoint (str): The relative API endpoint (e.g., 'inventory/items/123').
            params (dict, optional): A dictionary of query parameters to include
                in the request (e.g., {'status': 'active'}). Defaults to None.

        Returns:
            dict: The JSON-decoded response from the API.

        Raises:
            requests.exceptions.HTTPError: If the response contains an HTTP error status.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url , params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, data=data, json=json)
        return self._handle_response(response)

    def _put(self, endpoint, data=None, json=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, data=data, json=json)
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url)
        return response.status_code == 200 or response.status_code == 204 or response.status_code == 202
    
    def _handle_response(self, response):
        
        try:
            content = response.json()
        except ValueError:
            content = response.text
        return{
            "status_code": response.status_code,
            "url": response.url,
            "content": content,
            "headers" : response.headers
        }

    def _query(
        self,
        endpoint: str,
        resource_cls: Type["APIResource[T]"],
        *,
        all: bool = False,
        limit: int = 1000,
        start: int = 0,
        query: Optional[str] = None,
        filter: Optional[Dict[str, Any]] = None,
        sort: Optional[Dict[str, str]] = None,
        **extra_params
    ) -> List["APIResource[T]"]:
        """
        Query a list of resources from a Spire API endpoint with support for
        pagination, searching, filtering, and multi-level sorting.

        Args:
            endpoint (str): The API endpoint (e.g., 'sales/orders').
            resource_cls (Type[APIResource[T]]): The resource wrapper class (e.g., SalesOrderResource).
            all (bool, optional): If True, fetches all available pages of results.
            limit (int, optional): Number of results per page (max 1000). Default is 1000.
            start (int, optional): Starting offset for pagination. Default is 0.
            q (str, optional): Free-text search query.
            filter (dict, optional): Dictionary of filter criteria, which will be JSON-encoded.
            sort (dict, optional): Dictionary of sorting rules (e.g., {"orderDate": "desc", "orderNo": "asc"}).
            **extra_params: Any additional query parameters to pass to the API.

        Returns:
            List[APIResource[T]]: A list of wrapped resource instances.
        """
        collected = []
        current_start = start

        while True:
            # Build the query params as a list of tuples to allow repeated keys like 'sort'
            params: List[Tuple[str, Any]] = [
                ("start", current_start),
                ("limit", min(limit, 1000))
            ]

            if query:
                params.append(("q", query))

            if filter:
                encoded_filter = json.dumps(filter)
                params.append(("filter", encoded_filter))

            if sort:
                for field, direction in sort.items():
                    prefix = "-" if direction.lower() == "desc" else ""
                    params.append(("sort", f"{prefix}{field}"))

            # Add any additional custom parameters
            for k, v in extra_params.items():
                params.append((k, v))

            response = self._get(endpoint.rstrip("/"), params=params)
            items = response.get("records", [])
            count = response.get("count", 0)

            for item in items:
                collected.append(resource_cls.from_json(item, self))

            if not all or (current_start + limit >= count):
                break

            current_start += limit

        return collected


class APIResource(Generic[T]):
    """Active-record-like wrapper that knows a *session* and a *model*."""
    _model: T
    _client: SpireClient
    Model: type
    endpoint: str   

    def __init__(self, model: T, client: SpireClient, **kwargs):
        object.__setattr__(self, "_model", model)
        object.__setattr__(self, "_client", client)

        # Let child classes handle extra kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, item):
        """  delegate unknown attributes to the Pydantic model. 
        if you try to access an attribute on your wrapper class that doesn't exist in that class.
        It will automatically forward the request to self._model """
        
        return getattr(self._model, item)
    
    def __setattr__(self, key, value):
        """
        Delegate attribute setting to the Pydantic model unless the attribute 
        starts with an underscore (which indicates internal fields like _model or _client).
        """
        if key.startswith("_"):
            object.__setattr__(self, key, value)
        else:
            setattr(self._model, key, value)
  
    def __str__(self):
        return self._model.model_dump_json(indent=2)
    
    @property
    def model(self) -> T:
        """
        Accessor for the underlying Pydantic model.

        Returns:
            T: The internal Pydantic model instance.
        """
        return self._model
    
    @classmethod
    def from_json(cls, json_data: dict, client: SpireClient, **kwargs) -> "APIResource":
        model_instance = cls.Model(**json_data)
        return cls(model_instance, client, **kwargs)
    
    def refresh(self):
        updated = self._client._get(f"{self.endpoint}/{self.id}")
        self._model = self.Model(**updated)
        return self

    def to_dict(self):
        return self._model.model_dump(exclude_unset=True, exclude_none=True)
    

    

