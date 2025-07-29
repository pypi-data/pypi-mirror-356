import json
import os
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import loguru

from ..logs import configure_logging, set_correlation_id
from ..types import ApiVersion, RequestData


class AiriaBaseClient:
    """Base client containing shared functionality for Airia API clients."""

    openai = None
    anthropic = None

    def __init__(
        self,
        base_url: str = "https://api.airia.ai/",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        log_requests: bool = False,
        custom_logger: Optional["loguru.Logger"] = None,
    ):
        """
        Initialize the Airia API client base class.

        Args:
            api_key: API key for authentication. If not provided, will attempt to use AIRIA_API_KEY environment variable.
            timeout: Request timeout in seconds.
            log_requests: Whether to log API requests and responses. Default is False.
            custom_logger: Optional custom logger object to use for logging. If not provided, will use a default logger when `log_requests` is True.
        """
        # Resolve API key: parameter takes precedence over environment variable
        self.api_key = self.__class__._get_api_key(api_key)

        # Store configuration
        self.base_url = base_url
        self.timeout = timeout
        self.log_requests = log_requests

        # Initialize logger
        self.logger = configure_logging() if custom_logger is None else custom_logger

    @staticmethod
    def _get_api_key(api_key: Optional[str] = None):
        """
        Get the API key from either the provided parameter or environment variable.

        Args:
            api_key (Optional[str]): The API key provided as a parameter. Defaults to None.

        Returns:
            str: The resolved API key.

        Raises:
            ValueError: If no API key is provided through either method.
        """
        api_key = api_key or os.environ.get("AIRIA_API_KEY")

        if not api_key:
            raise ValueError(
                "API key must be provided either as a parameter or through the AIRIA_API_KEY environment variable."
            )

        return api_key

    def _prepare_request(
        self,
        url: str,
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
    ):
        # Set correlation ID if provided or generate a new one
        correlation_id = set_correlation_id(correlation_id)

        # Add the X-API-KEY header and correlation ID
        headers = {
            "X-API-KEY": self.api_key,
            "X-Correlation-ID": correlation_id,
            "Content-Type": "application/json",
        }

        # Log the request if enabled
        if self.log_requests:
            # Create a sanitized copy of headers and params for logging
            log_headers = headers.copy()
            log_params = params.copy() if params is not None else {}

            # Filter out sensitive headers
            if "X-API-KEY" in log_headers:
                log_headers["X-API-KEY"] = "[REDACTED]"

            # Process payload for logging
            log_payload = payload.copy() if payload is not None else {}
            if "images" in log_payload and log_payload["images"] is not None:
                log_payload["images"] = f"{len(log_payload['images'])} images"
            if "files" in log_payload and log_payload["files"] is not None:
                log_payload["files"] = f"{len(log_payload['files'])} files"
            log_payload = json.dumps(log_payload)

            self.logger.info(
                f"API Request: POST {url}\n"
                f"Headers: {json.dumps(log_headers)}\n"
                f"Payload: {log_payload}"
                f"Params: {json.dumps(log_params)}\n"
            )

        return RequestData(
            **{
                "url": url,
                "payload": payload,
                "headers": headers,
                "params": params,
                "correlation_id": correlation_id,
            }
        )

    def _pre_execute_pipeline(
        self,
        pipeline_id: str,
        user_input: str,
        debug: bool = False,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        async_output: bool = False,
        include_tools_response: bool = False,
        images: Optional[List[str]] = None,
        files: Optional[List[str]] = None,
        data_source_folders: Optional[Dict[str, Any]] = None,
        data_source_files: Optional[Dict[str, Any]] = None,
        in_memory_messages: Optional[List[Dict[str, str]]] = None,
        current_date_time: Optional[str] = None,
        save_history: bool = True,
        additional_info: Optional[List[Any]] = None,
        prompt_variables: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
        api_version: str = ApiVersion.V2.value,
    ):
        if api_version not in ApiVersion.as_list():
            raise ValueError(
                f"Invalid API version: {api_version}. Valid versions are: {', '.join(ApiVersion.as_list())}"
            )
        url = urljoin(self.base_url, f"{api_version}/PipelineExecution/{pipeline_id}")

        payload = {
            "userInput": user_input,
            "debug": debug,
            "userId": user_id,
            "conversationId": conversation_id,
            "asyncOutput": async_output,
            "includeToolsResponse": include_tools_response,
            "images": images,
            "files": files,
            "dataSourceFolders": data_source_folders,
            "dataSourceFiles": data_source_files,
            "inMemoryMessages": in_memory_messages,
            "currentDateTime": current_date_time,
            "saveHistory": save_history,
            "additionalInfo": additional_info,
            "promptVariables": prompt_variables,
        }

        request_data = self._prepare_request(
            url=url, payload=payload, correlation_id=correlation_id
        )

        return request_data

    def _pre_get_projects(
        self,
        correlation_id: Optional[str] = None,
        api_version: str = ApiVersion.V1.value,
    ):
        if api_version not in ApiVersion.as_list():
            raise ValueError(
                f"Invalid API version: {api_version}. Valid versions are: {', '.join(ApiVersion.as_list())}"
            )
        url = urljoin(self.base_url, f"{api_version}/Project/paginated")
        request_data = self._prepare_request(url, correlation_id=correlation_id)

        return request_data

    def _pre_get_active_pipelines_ids(
        self,
        project_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        api_version: str = ApiVersion.V1.value,
    ):
        if api_version not in ApiVersion.as_list():
            raise ValueError(
                f"Invalid API version: {api_version}. Valid versions are: {', '.join(ApiVersion.as_list())}"
            )
        url = urljoin(self.base_url, f"{api_version}/PipelinesConfig")
        params = {"projectId": project_id} if project_id is not None else None
        request_data = self._prepare_request(
            url, params=params, correlation_id=correlation_id
        )

        return request_data

    def _pre_get_pipeline_config(
        self,
        pipeline_id: str,
        correlation_id: Optional[str] = None,
        api_version: str = ApiVersion.V1.value,
    ):
        if api_version not in ApiVersion.as_list():
            raise ValueError(
                f"Invalid API version: {api_version}. Valid versions are: {', '.join(ApiVersion.as_list())}"
            )
        url = urljoin(
            self.base_url, f"{api_version}/PipelinesConfig/export/{pipeline_id}"
        )
        request_data = self._prepare_request(url, correlation_id=correlation_id)

        return request_data

    def _pre_get_projects(
        self,
        correlation_id: Optional[str] = None,
        api_version: str = ApiVersion.V1.value,
    ):
        if api_version not in ApiVersion.as_list():
            raise ValueError(
                f"Invalid API version: {api_version}. Valid versions are: {', '.join(ApiVersion.as_list())}"
            )
        url = urljoin(self.base_url, f"{api_version}/Project/paginated")
        request_data = self._prepare_request(url, correlation_id=correlation_id)

        return request_data
