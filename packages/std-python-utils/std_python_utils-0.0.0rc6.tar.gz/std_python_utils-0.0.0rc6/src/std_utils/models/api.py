import http
from functools import cache
from typing import Any, Literal, Optional

import aiohttp
import requests
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, Json
from requests import Session


DEFAULT_HEADERS = {'Content-Type': 'application/json'}
JsonPrimValue = str | bool | int | float | None


@cache
def get_default_headers() -> dict[str, str]:
    return DEFAULT_HEADERS


@cache
def get_empty_json() -> Json[Any]:
    return {}


class APIHeaders(BaseModel):
    """
    Model that represents a generic API headers.
    """
    model_config = ConfigDict(extra='allow')
    content_type: Literal['application/json'] = Field(
        alias='Content-Type',
        default='application/json',
        serialization_alias='Content-Type'
    )


class APIResponse(BaseModel):
    """
    Model that represents a generic API response.
    """

    status_code: int
    headers: dict = Field(default_factory=get_empty_json)
    data: dict = Field(default_factory=get_empty_json)
    error: Optional[str] = None


class APIRequest(BaseModel):
    """
    Model that represents a generic API request.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    endpoint: HttpUrl
    method: http.HTTPMethod
    headers: dict = Field(default_factory=get_default_headers)
    query_params: dict = Field(default_factory=get_empty_json)
    body: dict = Field(default_factory=get_empty_json)
    session: Optional[Session] = None
    client_session: Optional[aiohttp.ClientSession] = None

    @property
    def full_args(self) -> dict[str, Any]:
        return {
            'method': self.method,
            'url': self.endpoint.unicode_string(),
            'headers': self.headers,
            'params': self.query_params,
            'json': self.body
        }

    def get_args(self, **kwargs) -> dict[str, Any]:
        return {
            **kwargs, **{k: v for k, v in self.full_args if k not in kwargs}
        }

    def send(self, **kwargs) -> Any:
        # Allow overriding the default values
        return self.session.request(
            **kwargs
            ) if self.session else requests.request(**kwargs)

    async def async_send(
        self, ) -> Any:
        if self.client_session:
            return await self.async_send_with_session(
                self.client_session,
                **self.full_args
                )
        else:
            async with aiohttp.ClientSession() as client_session:
                return await self.async_send_with_session(
                    client_session,
                    **self.full_args
                    )

    async def async_send_with_session(
        self, client_session: aiohttp.ClientSession, **kwargs
    ) -> Any:
        args = self.get_args(**kwargs)
        method_func_map = {
            http.HTTPMethod.GET: client_session.get,
            http.HTTPMethod.POST: client_session.post,
            http.HTTPMethod.PUT: client_session.put,
            http.HTTPMethod.DELETE: client_session.delete,
            http.HTTPMethod.PATCH: client_session.patch,
        }
        return await method_func_map[self.method](**args)
