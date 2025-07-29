# SPDX-FileCopyrightText: 2024 CSC - IT Center for Science Oy
#
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, Field
import enum
from typing import List, Dict, Any, Optional


class TaskState(str, enum.Enum):
    Pending = "Pending"
    Running = "Running"
    Success = "Success"
    Failure = "Failure"


class HTTPMethod(str, enum.Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    PATCH = "PATCH"


class Link(BaseModel):
    """A hypertext application language link object, linking one resource to another."""

    href: str = Field(description="The URI of the linked resource.")
    name: str | None = Field(
        default=None,
        description="A unique name for the linked resource from the perspective of the linking resource.",
    )
    title: str | None = Field(
        default=None, description="A human-readable label for the link."
    )
    method: HTTPMethod = Field(
        default=HTTPMethod.GET, description="The HTTP method to use with the link."
    )

    model_config = {"frozen": True}


class ModelLinks(BaseModel):
    self: Link
    infer: Link
    collection: Link
    openai_chat_completion: Optional[Link] = Field(None, alias="openai-chat-completion")
    openai: Optional[Link] = None


class Model(BaseModel):
    """Detailed information about a model served by the API.

    NOTE(2023-11-15): Since the API is still in development, details about inputs and outputs for models are not yet available via the API in a parseable manner.
    """

    id: str = Field(description="A unique identifier for the model.")
    description: str = Field(
        description="A human-readable description of the model and expected inputs and outputs."
    )
    capabilities: set[str] = Field(description="A set of capabilities of the model.")
    links: ModelLinks = Field(
        alias="_links",
        description="Links to interact with the resource and obtain information about related resources.",
    )


class ModelListLinks(BaseModel):
    self: Link
    item: List[Link]


class ModelList(BaseModel):
    """A list of models served by the API with URIs from which more information for each model can be obtained.

    The following links are provided:
    - self: Refer back to the resource itself.
    - item: Obtain information about any particular model in the list.
    """

    links: ModelListLinks = Field(
        alias="_links",
        description="Links to interact with the resource and obtain information about related resources.",
    )


class TaskProgress(BaseModel):
    progress: int = Field(
        description="Processing progress of the inference request. Each increment corresponds to an unspecified amount of progress. The total number of increments (maximum value of progress) is available from the total_progress field, if known.",
        ge=0,
    )
    total_progress: int | None = Field(
        description="The total number of progress increments, i.e., maximum value of the progress field. May be None, which indicates that the total number of increments is unknown.",
        gt=0,
    )


class TaskLinks(BaseModel):
    self: Link
    stop: Link
    model: Link


class Task(BaseModel):
    """Information about an ongoing or completed inference task.

    The following links are provided:
    - self: Refer back to the resource itself.
    - stop: Revoke an inference request that is pending execution.
    - model: Obtain information about the model serving this task.
    """

    id: str = Field(description="A unique identifier for the task.")
    model_id: str = Field(
        description="The unique identifier of the model to which the inference request is made."
    )
    state: TaskState = Field(
        description="The current state of the task, i.e., whether it is pending execution, currently being executed, completed or failed."
    )
    error: Any | None = Field(
        description="Contains further information about an encountered error if the task completed with a failure."
    )
    results: Any | None = Field(
        description="Contains the result of the inference task if the task completed successfully."
    )
    progress: TaskProgress | None = Field(
        description="Information on the current progress of the task. Only set if `state` is `Running` and if progress information is available for the task/model."
    )
    links: TaskLinks = Field(
        alias="_links",
        description="Links to interact with the resource and obtain information about related resources.",
    )

    model_config = {"protected_namespaces": ()}


class APIError(BaseModel):
    error: str
    error_description: str | None = Field(
        default=None, description="Human-readable text providing additional information"
    )
    error_uri: str | None = Field(
        default=None,
        description="A URI identifying a human-readable web page with information about the error, used to provide the user with additional information about the error.",
    )
    details: Dict[str, Any] | None = Field(
        default=None,
        description="A JSON object containing further information on the cause of the error, if applicable.",
    )


class AccessToken(BaseModel):
    """The response for an access token request. Follows in large parts the OAuth2 reponse format (https://datatracker.ietf.org/doc/html/rfc6749#section-5.1) but excludes scope information."""

    access_token: str = Field(
        description="The access token that must be provided as HTTP bearer token to all API calls."
    )
    expires_in: int = Field(
        description="The remaining lifetime of the token (in seconds), after which it can no longer be used."
    )
    token_type: str = Field(
        default="Bearer",
        description="The type of the token issued as described in the OAuth2 specification. Always 'Bearer'.",
    )
    refresh_token: str | None = Field(
        default=None,
        description="An optional refresh token, which can be used to obtain new access tokens if provided.",
    )
