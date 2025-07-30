"""Core MCP server implementation using the Model Context Protocol."""

import json
import logging
from asyncio.exceptions import CancelledError
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any, cast

import httpx
from anyio import WouldBlock
from fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData

from . import __version__
from .api_client import FabricApiClient
from .config import get_default_model

DEFAULT_MCP_HTTP_PATH = "/message"

DEFAULT_VENDOR = "openai"
DEFAULT_MODEL = "gpt-4o"  # Default model if none specified in config


@dataclass
class PatternExecutionConfig:  # pylint: disable=too-many-instance-attributes
    """Configuration for pattern execution parameters."""

    model_name: str | None = None
    vendor_name: str | None = None
    strategy_name: str | None = None
    variables: dict[str, str] | None = None
    attachments: list[str] | None = None
    temperature: float | None = None
    top_p: float | None = None
    presence_penalty: float | None = None
    frequency_penalty: float | None = None


class FabricMCP(FastMCP[None]):
    """Base class for the Model Context Protocol server."""

    def __init__(self, log_level: str = "INFO"):
        """Initialize the MCP server with a model."""
        super().__init__(f"Fabric MCP v{__version__}")
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level

        # Load default model configuration from Fabric environment
        self._default_model: str | None = None
        self._default_vendor: str | None = None
        self._load_default_config()

        # Explicitly register tool methods
        for fn in (
            self.fabric_list_patterns,
            self.fabric_get_pattern_details,
            self.fabric_run_pattern,
            self.fabric_list_models,
            self.fabric_list_strategies,
            self.fabric_get_configuration,
        ):
            self.tool(fn)

    def _load_default_config(self) -> None:
        """Load default model configuration from Fabric environment.

        This method loads DEFAULT_MODEL and DEFAULT_VENDOR from the Fabric
        environment configuration (~/.config/fabric/.env) and stores them
        as instance variables for use in pattern execution.

        Errors during configuration loading are logged but do not prevent
        server startup to ensure graceful degradation.
        """
        try:
            self._default_model, self._default_vendor = get_default_model()
            if self._default_model and self._default_vendor:
                self.logger.info(
                    "Loaded default model configuration: %s (%s)",
                    self._default_model,
                    self._default_vendor,
                )
            elif self._default_model:
                self.logger.info(
                    "Loaded ONLY default model: %s (no vendor)", self._default_model
                )
            elif self._default_vendor:
                self.logger.info(
                    "Loaded ONLY default vendor: %s (no model)", self._default_vendor
                )
            else:
                self.logger.info("No default model configuration found")
        except (OSError, ValueError, TypeError) as e:
            self.logger.warning(
                "Failed to load default model configuration: %s. "
                "Pattern execution will use hardcoded defaults.",
                e,
            )

    def _make_fabric_api_request(
        self,
        endpoint: str,
        pattern_name: str | None = None,
        operation: str = "API request",
    ) -> Any:
        """Make a request to the Fabric API with consistent error handling.

        Args:
            endpoint: The API endpoint to call (e.g., "/patterns/names")
            pattern_name: Pattern name for pattern-specific error messages
            operation: Description of the operation for error messages

        Returns:
            The parsed JSON response from the API

        Raises:
            McpError: For any API errors, connection issues, or parsing problems
        """
        try:
            api_client = FabricApiClient()
            try:
                response = api_client.get(endpoint)
                return response.json()
            finally:
                api_client.close()
        except httpx.RequestError as e:
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message="Failed to connect to Fabric API",
                )
            ) from e
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500 and pattern_name:
                # Check for pattern not found (500 with file not found message)
                error_message = e.response.text or ""
                if "no such file or directory" in error_message:
                    raise McpError(
                        ErrorData(
                            code=-32602,  # Invalid params - pattern doesn't exist
                            message=f"Pattern '{pattern_name}' not found",
                        )
                    ) from e
                # Other 500 errors for pattern requests
                raise McpError(
                    ErrorData(
                        code=-32603,  # Internal error
                        message=f"Fabric API internal error: {error_message}",
                    )
                ) from e
            # Generic HTTP status errors
            status_code = e.response.status_code
            reason = e.response.reason_phrase or "Unknown error"
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message=f"Fabric API error: {status_code} {reason}",
                )
            ) from e
        except Exception as e:
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message=f"Unexpected error during {operation}: {e}",
                )
            ) from e

    def fabric_list_patterns(self) -> list[str]:
        """Return a list of available fabric patterns."""
        response_data = self._make_fabric_api_request(
            "/patterns/names", operation="retrieving patterns"
        )

        # Validate response data type
        if not isinstance(response_data, list):
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message="Invalid response from Fabric API: "
                    "expected list of patterns",
                )
            )

        # Cast to expected type
        response_data = cast(list[Any], response_data)

        for item in response_data:
            # Ensure each item is a string
            if not isinstance(item, str):
                raise McpError(
                    ErrorData(
                        code=-32603,  # Internal error
                        message="Invalid pattern name in response: "
                        f"expected string, got {type(item).__name__}",
                    )
                )

        patterns = cast(list[str], response_data)

        return patterns

    def fabric_get_pattern_details(self, pattern_name: str) -> dict[str, str]:
        """Retrieve detailed information for a specific Fabric pattern."""
        # Use helper method for API request with pattern-specific error handling
        response_data = self._make_fabric_api_request(
            f"/patterns/{pattern_name}",
            pattern_name=pattern_name,
            operation="retrieving pattern details",
        )

        # Validate response data type
        if not isinstance(response_data, dict):
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message="Invalid response from Fabric API: "
                    "expected dict for pattern details",
                )
            )

        response_data = cast(dict[str, Any], response_data)

        # Validate required fields in the response
        if not all(key in response_data for key in ("Name", "Description", "Pattern")):
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message="Invalid pattern details response: missing required fields",
                )
            )

        # Transform Fabric API response to MCP expected format
        details = {
            "name": response_data["Name"],
            "description": response_data["Description"],
            "system_prompt": response_data["Pattern"],
        }

        return details

    def fabric_run_pattern(
        self,
        pattern_name: str,
        input_text: str = "",
        stream: bool = False,
        config: PatternExecutionConfig | None = None,
        model_name: str | None = None,
        vendor_name: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        strategy_name: str | None = None,
        variables: dict[str, str] | None = None,
        attachments: list[str] | None = None,
    ) -> dict[str, Any] | Generator[dict[str, Any], None, None]:
        """
        Execute a Fabric pattern with input text and return output.

        This tool calls the Fabric API's /chat endpoint to execute a named pattern
        with the provided input text. Returns either complete output (non-streaming)
        or a generator of chunks (streaming) based on the stream parameter.

        Args:
            pattern_name: The name of the fabric pattern to run (required).
            input_text: The input text to be processed by the pattern (optional).
            stream: Whether to stream the output. If True, returns a generator of
            chunks.
            config: Optional configuration for execution parameters.
            model_name: Optional model name override (e.g., "gpt-4", "claude-3-opus").
            vendor_name: Optional vendor name override (e.g., "openai", "anthropic").
            temperature: Optional temperature for LLM (0.0-2.0, controls randomness).
            top_p: Optional top-p for LLM (0.0-1.0, nucleus sampling).
            presence_penalty: Optional presence penalty (-2.0-2.0, reduces repetition).
            frequency_penalty: Optional frequency penalty (-2.0-2.0, reduces frequency).
            strategy_name: Optional strategy name for pattern execution.
            variables: Optional map of key-value strings for pattern variables.
            attachments: Optional list of file paths/URLs to attach to the pattern.

        Returns:
            dict[Any, Any] | Generator: For non-streaming, returns dict with
            'output_format' and 'output_text'.
            For streaming, returns a generator yielding dict chunks
            with 'type', 'format', and 'content'.

        Raises:
            McpError: For any API errors, connection issues, or parsing problems.
        """

        # Validate new parameters
        self._validate_execution_parameters(
            model_name,
            vendor_name,
            temperature,
            top_p,
            presence_penalty,
            frequency_penalty,
            strategy_name,
            variables,
            attachments,
        )

        # Merge parameters with config
        merged_config = self._merge_execution_config(
            config,
            model_name,
            vendor_name,
            temperature,
            top_p,
            presence_penalty,
            frequency_penalty,
            strategy_name,
            variables,
            attachments,
        )

        try:
            return self._execute_fabric_pattern(
                pattern_name, input_text, merged_config, stream
            )
        except RuntimeError as e:
            error_message = str(e)
            # Check for pattern not found (500 with file not found message)
            if (
                "Fabric API returned error 500" in error_message
                and "no such file or directory" in error_message
            ):
                raise McpError(
                    ErrorData(
                        code=-32602,  # Invalid params - pattern doesn't exist
                        message=f"Pattern '{pattern_name}' not found",
                    )
                ) from e
            # Check for other HTTP status errors
            if "Fabric API returned error" in error_message:
                raise McpError(
                    ErrorData(
                        code=-32603,  # Internal error
                        message=f"Error executing pattern '{pattern_name}': {e}",
                    )
                ) from e
            # Other runtime errors
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message=f"Error executing pattern '{pattern_name}': {e}",
                )
            ) from e
        except ConnectionError as e:
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message=f"Error executing pattern '{pattern_name}': {e}",
                )
            ) from e
        except ValueError as e:
            raise McpError(
                ErrorData(
                    code=-32602,  # Invalid params
                    message=f"Invalid parameter for pattern '{pattern_name}': {e}",
                )
            ) from e

    def fabric_list_models(self) -> dict[Any, Any]:
        """Retrieve configured Fabric models by vendor."""
        # This is a placeholder for the actual implementation
        return {
            "models": ["gpt-4o", "gpt-3.5-turbo", "claude-3-opus"],
            "vendors": {
                "openai": ["gpt-4o", "gpt-3.5-turbo"],
                "anthropic": ["claude-3-opus"],
            },
        }

    def fabric_list_strategies(self) -> dict[Any, Any]:
        """Retrieve available Fabric strategies."""
        # Use helper method for API request
        response_data = self._make_fabric_api_request(
            "/strategies", operation="retrieving strategies"
        )

        # Validate response data type
        if not isinstance(response_data, list):
            raise McpError(
                ErrorData(
                    code=-32603,  # Internal error
                    message="Invalid response from Fabric API: "
                    "expected list of strategies",
                )
            )

        response_data = cast(list[Any], response_data)
        # Ensure all items are dictionaries
        for item in response_data:
            if not isinstance(item, dict):
                raise McpError(
                    ErrorData(
                        code=-32603,  # Internal error
                        message="Invalid strategy object in response: "
                        f"expected dict, got {type(item).__name__}",
                    )
                )

        # Cast to expected type
        response_data = cast(list[dict[str, Any]], response_data)

        # Validate each strategy object and build response
        validated_strategies: list[dict[str, str]] = []
        for item in response_data:
            name = item.get("name", "")
            description = item.get("description", "")
            prompt = item.get("prompt", "")

            # Type check all fields as strings and ensure name/description not empty
            if (
                isinstance(name, str)
                and isinstance(description, str)
                and isinstance(prompt, str)
                and name.strip()  # Name must not be empty/whitespace
                and description.strip()  # Description must not be empty/whitespace
                # Note: prompt can be empty string - that's valid
            ):
                validated_strategies.append(
                    {"name": name, "description": description, "prompt": prompt}
                )
            else:
                # Log warning but continue with valid strategies
                self.logger.warning(
                    "Strategy object missing required string fields: %s",
                    cast(Any, item),
                )

        return {"strategies": validated_strategies}

    def fabric_get_configuration(self) -> dict[Any, Any]:
        """Retrieve Fabric configuration with sensitive values redacted."""
        # This is a placeholder for the actual implementation
        return {
            "openai_api_key": "[REDACTED_BY_MCP_SERVER]",
            "ollama_url": "http://localhost:11434",
            "anthropic_api_key": "[REDACTED_BY_MCP_SERVER]",
            "fabric_config_dir": "~/.config/fabric",
        }

    def http_streamable(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
        mcp_path: str = DEFAULT_MCP_HTTP_PATH,
    ):
        """Run the MCP server with StreamableHttpTransport."""
        try:
            self.run(transport="streamable-http", host=host, port=port, path=mcp_path)
        except (KeyboardInterrupt, CancelledError, WouldBlock) as e:
            # Handle graceful shutdown
            self.logger.debug("Exception details: %s: %s", type(e).__name__, e)
            self.logger.info("Server stopped by user.")

    def stdio(self):
        """Run the MCP server."""
        try:
            self.run()
        except (KeyboardInterrupt, CancelledError, WouldBlock):
            # Handle graceful shutdown
            self.logger.info("Server stopped by user.")

    def get_vendor_and_model(self, config: PatternExecutionConfig) -> tuple[str, str]:
        """Get the vendor and model based on the provided configuration."""
        vendor_name = config.vendor_name or self._default_vendor
        if not vendor_name:
            self.logger.debug(
                "Vendor name is None or empty. Set to hardcoded default vendor: %s",
                DEFAULT_VENDOR,
            )
            vendor_name = DEFAULT_VENDOR

        model_name = config.model_name or self._default_model
        if not model_name:
            self.logger.debug(
                "Model name is None or empty. Set to hardcoded default model: %s",
                DEFAULT_MODEL,
            )
            model_name = DEFAULT_MODEL

        return vendor_name, model_name

    def _execute_fabric_pattern(
        self,
        pattern_name: str,
        input_text: str,
        config: PatternExecutionConfig | None,
        stream: bool = False,
    ) -> dict[Any, Any] | Generator[dict[str, Any], None, None]:
        """
        Execute a Fabric pattern against the API.

        Separated from the tool method to reduce complexity.
        """
        # AC5: Client-side validation
        if not pattern_name or not pattern_name.strip():
            raise ValueError("pattern_name is required and cannot be empty")

        # Use default config if none provided
        if config is None:
            config = PatternExecutionConfig()

        vendor, model_name = self.get_vendor_and_model(config)

        # AC3: Construct proper JSON payload for Fabric API /chat endpoint
        prompt_data: dict[str, Any] = {
            "userInput": input_text,
            "patternName": pattern_name.strip(),
            "model": model_name,
            "vendor": vendor,
            "contextName": "",
            "strategyName": config.strategy_name or "",
        }

        # Add variables if provided
        if config.variables is not None:
            prompt_data["variables"] = config.variables

        # Add attachments if provided
        if config.attachments is not None:
            prompt_data["attachments"] = config.attachments

        request_payload = {
            "prompts": [prompt_data],
            "language": "en",
            "temperature": config.temperature
            if config.temperature is not None
            else 0.7,
            "topP": config.top_p if config.top_p is not None else 0.9,
            "frequencyPenalty": config.frequency_penalty
            if config.frequency_penalty is not None
            else 0.0,
            "presencePenalty": config.presence_penalty
            if config.presence_penalty is not None
            else 0.0,
        }

        # AC1: Use FabricApiClient to call Fabric's /chat endpoint
        api_client = FabricApiClient()
        try:
            # AC4: Handle Server-Sent Events (SSE) stream response
            response = api_client.post("/chat", json_data=request_payload)
            response.raise_for_status()  # Raise HTTPError for bad responses

            if stream:
                # Return generator for streaming mode
                return self._parse_sse_stream(response)
            else:
                # Return accumulated result for non-streaming mode
                return self._parse_sse_response(response)

        except httpx.ConnectError as e:
            self.logger.error("Failed to connect to Fabric API: %s", e)
            raise ConnectionError(f"Unable to connect to Fabric API: {e}") from e
        except httpx.HTTPStatusError as e:
            self.logger.error("Fabric API HTTP error: %s", e)
            error_text = e.response.text
            status_code = e.response.status_code
            raise RuntimeError(
                f"Fabric API returned error {status_code}: {error_text}"
            ) from e
        except Exception as e:
            self.logger.error("Unexpected error calling Fabric API: %s", e)
            raise RuntimeError(f"Unexpected error executing pattern: {e}") from e
        finally:
            api_client.close()

    def _parse_sse_response(self, response: httpx.Response) -> dict[str, str]:
        """
        Parse Server-Sent Events response from Fabric API.

        Returns:
            dict[str, str]: Contains 'output_format' and 'output_text' fields.
        """
        # Process SSE stream to collect all content
        output_chunks: list[str] = []
        output_format = "text"  # default
        has_data = False  # Track if we received any actual data

        # Parse SSE response line by line
        for line in response.iter_lines():
            line = line.strip()
            if not line:
                continue

            # SSE lines start with "data: "
            if line.startswith("data: "):
                has_data = True
                try:
                    data = json.loads(line[6:])  # Remove "data: " prefix

                    if data.get("type") == "content":
                        # Collect content chunks
                        content = data.get("content", "")
                        output_chunks.append(content)
                        # Update format if provided
                        output_format = data.get("format", output_format)

                    elif data.get("type") == "complete":
                        # End of stream
                        break

                    elif data.get("type") == "error":
                        # Handle error from Fabric API
                        error_msg = data.get("content", "Unknown Fabric API error")
                        raise RuntimeError(f"Fabric API error: {error_msg}")

                except json.JSONDecodeError as e:
                    self.logger.warning("Failed to parse SSE JSON: %s", e)
                    # For malformed SSE data, raise an error after logging
                    raise RuntimeError(f"Malformed SSE data: {e}") from e

        # Check if we received no data at all
        if not has_data:
            raise RuntimeError("Empty SSE stream - no data received")

        # AC6: Return structured response
        return {
            "output_format": output_format,
            "output_text": "".join(output_chunks),
        }

    def _parse_sse_stream(
        self, response: httpx.Response
    ) -> Generator[dict[str, Any], None, None]:
        """
        Parse Server-Sent Events response from Fabric API in streaming mode.

        Yields chunks in real-time as they arrive from the Fabric API.

        Yields:
            dict[str, Any]: Each chunk contains 'type', 'format', and 'content' fields.

        Raises:
            RuntimeError: If the SSE data is malformed or empty.
        """
        has_data = False  # Track if we received any actual data

        # Parse SSE response line by line
        for line in response.iter_lines():
            line = line.strip()
            if not line:
                continue

            # SSE lines start with "data: "
            if line.startswith("data: "):
                has_data = True
                try:
                    data = json.loads(line[6:])  # Remove "data: " prefix

                    if data.get("type") == "content":
                        # Yield content chunks in real-time
                        yield {
                            "type": "content",
                            "format": data.get("format", "text"),
                            "content": data.get("content", ""),
                        }

                    elif data.get("type") == "complete":
                        # Yield completion signal and end stream
                        yield {
                            "type": "complete",
                            "format": data.get("format", "text"),
                            "content": data.get("content", ""),
                        }
                        return

                    elif data.get("type") == "error":
                        # Yield error and end stream
                        error_msg = data.get("content", "Unknown Fabric API error")
                        raise RuntimeError(f"Fabric API error: {error_msg}")
                    else:
                        # Handle unexpected types gracefully
                        self.logger.warning(
                            "Unexpected SSE type: %s", data.get("type", "unknown")
                        )
                        raise RuntimeError(
                            "Unexpected SSE data type "
                            f"received: {data.get('type', 'unknown')}"
                        )

                except json.JSONDecodeError as e:
                    self.logger.warning("Failed to parse SSE JSON: %s", e)
                    raise RuntimeError(f"Malformed SSE data: {e}") from e

        # Check if we received no data at all
        if not has_data:
            raise RuntimeError("Empty SSE stream - no data received")

    def get_default_model_config(self) -> tuple[str | None, str | None]:
        """Get the current default model configuration.

        Returns:
            Tuple of (default_model, default_vendor). Either or both can be None.

        Note:
            This method is primarily intended for testing and introspection.
        """
        return self._default_model, self._default_vendor

    def _validate_numeric_parameter(
        self, name: str, value: float | None, min_value: float, max_value: float
    ) -> None:
        """Validate a single parameter against its expected range.

        Args:
            name: The name of the parameter (for error messages)
            value: The value of the parameter to validate
            min_value: The minimum acceptable value
            max_value: The maximum acceptable value

        Raises:
            McpError: If the parameter is invalid
        """
        if value is not None:
            try:
                if not min_value <= value <= max_value:
                    raise McpError(
                        ErrorData(
                            code=-32602,  # Invalid params
                            message=f"{name} must be a number between"
                            f" {min_value} and {max_value}",
                        )
                    )
            except TypeError as exc:
                raise McpError(
                    ErrorData(
                        code=-32602,  # Invalid params
                        message=f"{name} must be a number between {min_value}"
                        f" and {max_value}",
                    )
                ) from exc

    def _validate_string_parameter(self, name: str, value: str | None) -> None:
        """Validate a string parameter to ensure it is not empty.

        Args:
            name: The name of the parameter (for error messages)
            value: The value of the parameter to validate

        Raises:
            McpError: If the parameter is invalid
        """
        if value is not None and not value.strip():
            raise McpError(
                ErrorData(
                    code=-32602,  # Invalid params
                    message=f"{name} must be a non-empty string",
                )
            )

    def _validate_variables_parameter(self, variables: Any | None) -> None:
        """Validate variables parameter: dict with string keys and values.

        Args:
            variables: The variables parameter to validate

        Raises:
            McpError: If the parameter is invalid
        """
        if variables is not None:
            if not isinstance(variables, dict):
                raise McpError(
                    ErrorData(
                        code=-32602,  # Invalid params
                        message="variables must be a dictionary",
                    )
                )
            variable_keys_and_values: list[Any] = list(
                cast(list[Any], variables.values())
            ) + list(cast(list[Any], variables.keys()))
            if any(not isinstance(item, str) for item in variable_keys_and_values):
                raise McpError(
                    ErrorData(
                        code=-32602,  # Invalid params
                        message="variables must be a dictionary "
                        "with string keys and values",
                    )
                )

    def _validate_attachments_parameter(self, attachments: Any | None) -> None:
        """Validate an attachments parameter to ensure it is a list of strings.

        Args:
            attachments: The attachments parameter to validate

        Raises:
            McpError: If the parameter is invalid
        """
        if attachments is not None:
            if not isinstance(attachments, list):
                raise McpError(
                    ErrorData(
                        code=-32602,  # Invalid params
                        message="attachments must be a list",
                    )
                )
            if any(not isinstance(item, str) for item in cast(list[Any], attachments)):
                raise McpError(
                    ErrorData(
                        code=-32602,  # Invalid params
                        message="attachments must be a list of strings",
                    )
                )

    def _validate_execution_parameters(
        self,
        model_name: str | None = None,
        _vendor_name: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        strategy_name: str | None = None,
        variables: dict[str, str] | None = None,
        attachments: list[str] | None = None,
    ) -> None:
        """Validate execution control parameters."""
        # Validate temperature range
        self._validate_numeric_parameter("temperature", temperature, 0.0, 2.0)

        # Validate top_p range
        self._validate_numeric_parameter("top_p", top_p, 0.0, 1.0)

        # Validate presence_penalty range
        self._validate_numeric_parameter(
            "presence_penalty", presence_penalty, -2.0, 2.0
        )

        # Validate frequency_penalty range
        self._validate_numeric_parameter(
            "frequency_penalty", frequency_penalty, -2.0, 2.0
        )

        # Validate model_name format (basic validation - not empty string)
        self._validate_string_parameter("model_name", model_name)

        # Validate strategy_name format (basic validation - not empty string)
        self._validate_string_parameter("strategy_name", strategy_name)

        # Validate variables parameter format
        self._validate_variables_parameter(variables)

        # Validate attachments parameter format
        self._validate_attachments_parameter(attachments)

    def _merge_execution_config(
        self,
        config: PatternExecutionConfig | None,
        model_name: str | None = None,
        vendor_name: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        strategy_name: str | None = None,
        variables: dict[str, str] | None = None,
        attachments: list[str] | None = None,
    ) -> PatternExecutionConfig:
        """Merge execution parameters with existing config.

        Parameters provided directly to the tool take precedence over
        those in the config object.

        Args:
            config: Existing configuration (optional)
            model_name: Model name override (optional)
            temperature: Temperature override (optional)
            top_p: Top-p override (optional)
            presence_penalty: Presence penalty override (optional)
            frequency_penalty: Frequency penalty override (optional)
            strategy_name: Strategy name override (optional)
            variables: Variables override (optional)
            attachments: Attachments override (optional)

        Returns:
            Merged PatternExecutionConfig with parameter precedence
        """
        # Start with existing config or create new one
        if config is None:
            config = PatternExecutionConfig()

        # Create new config with parameter precedence
        return PatternExecutionConfig(
            # Use the provided model_name if available; otherwise, fall back
            # to the existing config's model_name
            model_name=model_name or config.model_name,
            # Use the provided vendor_name if available; otherwise, fall back
            # to the existing config's vendor_name
            vendor_name=vendor_name or config.vendor_name,
            # Use the provided strategy_name if available; otherwise, fall back
            # to the existing config's strategy_name
            strategy_name=strategy_name or config.strategy_name,
            # Use the provided variables if available; otherwise, fall back
            # to the existing config's variables
            variables=variables if variables is not None else config.variables,
            # Use the provided attachments if available; otherwise, fall back
            # to the existing config's attachments
            attachments=attachments if attachments is not None else config.attachments,
            # Use the provided temperature if not None; otherwise, fall back
            # to the existing config's temperature
            temperature=temperature if temperature is not None else config.temperature,
            # Use the provided top_p if not None; otherwise, fall back
            # to the existing config's top_p
            top_p=top_p if top_p is not None else config.top_p,
            # Use the provided presence_penalty if not None; otherwise, fall back
            # to the existing config's presence_penalty
            presence_penalty=(
                presence_penalty
                if presence_penalty is not None
                else config.presence_penalty
            ),
            # Use the provided frequency_penalty if not None; otherwise,
            # fall back to the existing config's frequency_penalty
            frequency_penalty=(
                frequency_penalty
                if frequency_penalty is not None
                else config.frequency_penalty
            ),
        )
