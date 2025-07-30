from requests import Request
from typing import Any, Type, Literal

import requests
import os
from dotenv import load_dotenv
from enum import Enum
from abc import ABC

from pydantic import BaseModel

from langchain_core.documents import Document

# Create a shared Response model, tested, that can be passed around


load_dotenv()


class Endpoints(Enum):
    CHAT = "/chat"
    SEARCH = "/search"
    UPLOAD = "/upload-file"
    CLEANUP = "/cleanUp"


class ContentTypes(Enum):
    JSONAPP = "application/json"
    MULTIPART_FORM = "multipart/form-data"


class RequestHeaders(BaseModel):
    content_type: ContentTypes
    authorization: str


class Body(BaseModel):
    content: Any


class QueryBody(Body):
    pass

class SearchBody(Body):
    pass

class CleanUpBody(Body):
    pass

class UploadBody(Body):
    pass


class InvalidRequestError(Exception):
    def __init__(self, message, malformed_parameter: 'MalformedResponseContent'):
        self.message = message
        self.malformed_parameter = malformed_parameter


class MalformedResponseContent(Enum):
    BODY = "body"
    URL = "url"
    HEADERS = "headers"


class Client(BaseModel):
    pat_token: str
    url: str


    def generate_



    def generate_headers(self, body: Body) -> RequestHeaders:
        if isinstance(body, UploadBody) or isinstance(body, CleanUpBody) or isinstance(body, SearchBody):
            content_type = ContentTypes.JSONAPP

        elif isinstance(body, SearchBody):
            content_type = ContentTypes.MULTIPART_FORM

        else:
            raise InvalidRequestError(
                message=f"Unsupported body type: {type(body)}",
                malformed_parameter=MalformedResponseContent.BODY,
            )

        def generate(content_type: ContentTypes) -> RequestHeaders:
            headers = RequestHeaders(
                content_type=content_type,
                authorization=self.pat_token
            )
            return headers

        return generate(content_type=content_type)


    def send_request(self, body: Body):  # -> CustomResponse
        request = Request(
            method="POST",
            url=self.url,
            headers=self.generate_headers(body),
            json=body.content,
            auth=self.pat_token,
        )


    def _send_request(self, headers: RequestHeaders, body: Body, endpoint: Endpoints):  # -> CustomResponse
        requests.post(
            self.url + f'{endpoint}',
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.pat_token,
            },
            json={"query": body.content}
        )

        raise  NotImplementedError()


client = Client(
    pat_token=os.getenv("PAT"),
    url=os.getenv("URL"),
)
client.send(
    endpoint,

)