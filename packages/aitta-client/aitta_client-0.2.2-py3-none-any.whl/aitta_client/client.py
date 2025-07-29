# SPDX-FileCopyrightText: 2024 CSC - IT Center for Science Oy
#
# SPDX-License-Identifier: MIT

from typing import Iterable, Dict, Any
import pydantic
import requests
from .api import data_structures
from .api.errors import MalformedAPIResponse, handle_error_responses
from .api.wrappers import ModelBasicReference, ModelData, TaskData
from .authentication import AccessTokenSource


class Client:
    """Main API client implementation.

    Arguments:
        - url: The base URL of the API server, as a string.
        - access_token_source: An `AccessTokenSource` instances which provides an access token for API requests.
        - request_timeout_ms: The maximum waiting time for establishing a connection and receiving a response from the API.
    """

    def __init__(
        self,
        url: str,
        access_token_source: AccessTokenSource,
        request_timeout_ms: int = 1000,
    ) -> None:
        self._url = url

        self._token_source = access_token_source
        self._timeout_ms = request_timeout_ms

    @property
    def access_token_source(self) -> AccessTokenSource:
        return self._token_source

    def _endpoint_to_url(self, endpoint: str) -> str:
        return self._url + endpoint

    def _make_request_headers(self) -> Dict[str, str]:
        headers = {
            "Authorization": "Bearer " + self.access_token_source.get_access_token()
        }
        return headers

    def _make_request(
        self, endpoint: str, json: Any = None, method: str | None = None
    ) -> requests.Response:
        if method is None:
            if json is not None:
                method = "POST"
            else:
                method = "GET"
        headers = self._make_request_headers()
        url = self._endpoint_to_url(endpoint)
        response = requests.request(
            method, url, headers=headers, timeout=self._timeout_ms, json=json
        )
        handle_error_responses(response)
        return response

    def get_model_list(self) -> Iterable[ModelBasicReference]:
        """Lists all models served by the API that can be accessed with the configured access credentials.

        Returns:
            an iterable collection of models represented as `ModelBasicReference` instances, consiting of the model name/id and their main API endpoints
        """
        response = self._make_request("/model")

        try:
            model_list = data_structures.ModelList.model_validate_json(response.content)
            return [
                ModelBasicReference(model_link.name, model_link.href)
                for model_link in model_list.links.item
            ]
        except pydantic.ValidationError as e:
            raise MalformedAPIResponse(
                "The API server response could not be parsed."
            ) from e

    def get_model(self, model_reference: ModelBasicReference) -> ModelData:
        """Retrieves detailed information about a model.

        Arguments:
            - model_reference: A `ModelBasicReference` instance representing the API endpoints of the model for which detailed information should be retrieved.

        Returns:
            detailed information of the model as a `ModelData` object
        """
        response = self._make_request(model_reference.url_endpoint)

        try:
            model_data = data_structures.Model.model_validate_json(response.content)
            return ModelData(model_data)
        except pydantic.ValidationError as e:
            raise MalformedAPIResponse(
                "The API server response could not be parsed."
            ) from e

    def start_inference(
        self, model: ModelData, inputs: Dict[str, Any], params: Dict[str, Any]
    ) -> TaskData:
        """Starts a model inference task for the given model.

        This is a low-level implementation of API requests. You probably want to use `Model.start_inference` instead.

        This method does not block until the inference task is completed. Use the `get_task` method
        with the returned `TaskData` object to fetch updated progress information and results of the task.

        Does not currently perform any input processing or validation.

        Arguments:
            - model: A `ModelData` instance of the model with which to perform inference.
            - inputs: A dictionary of (batched) inputs to the model for the inference task.
                    See the model description in the `ModelData` instance of the model for details on accepted inputs and formats.
            - params: A dictionary of parameters that affect the model's behaviour during inference.
                    See the model description in the `ModelData` instance of the model for details on accepted parameters.

        Returns:
            a `TaskData` object containing details about the inference task and its API interaction endpoints.
        """
        response = self._make_request(
            model.infer_url_endpoint, json={**inputs, **params}
        )

        try:
            task_data = data_structures.Task.model_validate_json(response.content)
            return TaskData(task_data)
        except pydantic.ValidationError as e:
            raise MalformedAPIResponse(
                "The API server response could not be parsed."
            ) from e

    def get_task(self, task: TaskData) -> TaskData:
        """Obtain updated model inference task data.

        This is a low-level implementation of API requests. You probably want to use `Task.update` instead.

        Arguments:
            - task: A `TaskData` instance of the task for which to fetch updated information from the API.

        Returns:
            a `TaskData` instance containing current information about the task
        """
        response = self._make_request(task.url_endpoint)

        try:
            task_data = data_structures.Task.model_validate_json(response.content)
            return TaskData(task_data)
        except pydantic.ValidationError as e:
            raise MalformedAPIResponse(
                "The API server response could not be parsed."
            ) from e


__all__ = ["Client"]
