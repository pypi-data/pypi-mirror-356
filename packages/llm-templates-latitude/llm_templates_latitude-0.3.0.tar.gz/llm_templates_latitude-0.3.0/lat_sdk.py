"""
Latitude SDK client module

This module uses the official Latitude Python SDK for API interactions.
It provides the same interface as lat.py for seamless migration.
"""

import asyncio
from typing import Any, Dict, Optional

from latitude_sdk import Latitude, LatitudeOptions

from utils import (
    LatitudeAPIError,
    LatitudeAuthenticationError,
    LatitudeNotFoundError,
    convert_latitude_variables,
    filter_problematic_fields,
    strip_yaml_frontmatter,
)


class LatitudeClient:
    """Client for interacting with Latitude using official SDK"""

    def __init__(self, api_key: str, project_id: Optional[str] = None):
        """
        Initialize Latitude SDK client

        Args:
            api_key: Latitude API key
            project_id: Optional project ID for SDK initialization
        """
        self.api_key = api_key
        self.current_project_id = project_id
        self.current_version_uuid = None

        # Initialize SDK with project ID if provided
        if project_id:
            self.sdk = Latitude(api_key, LatitudeOptions(project_id=int(project_id)))
        else:
            self.sdk = Latitude(api_key)

    def get_document(
        self, project_id: str, version_uuid: str, document_path: str
    ) -> Dict[str, Any]:
        """
        Get a specific document from Latitude using SDK

        Args:
            project_id: Latitude project ID
            version_uuid: Version UUID
            document_path: Path to the document

        Returns:
            dict: Document data from Latitude SDK

        Raises:
            LatitudeAPIError: If the request fails
        """
        try:
            # For SDK, we need to update the project/version context if different
            if (
                self.current_project_id != project_id
                or self.current_version_uuid != version_uuid
            ):
                # Reinitialize SDK with correct project and version
                self.sdk = Latitude(
                    self.api_key,
                    LatitudeOptions(
                        project_id=int(project_id), version_uuid=version_uuid
                    ),
                )
                self.current_project_id = project_id
                self.current_version_uuid = version_uuid

            # Use SDK to get the prompt
            result = asyncio.run(self._async_get_document(document_path))

            # Convert SDK response to expected format
            return self._normalize_sdk_response(result)

        except Exception as e:
            error_str = str(e).lower()
            if "authentication" in error_str or "unauthorized" in error_str:
                raise LatitudeAuthenticationError(f"Invalid Latitude API key: {e}")
            elif "not found" in error_str or "404" in error_str:
                raise LatitudeNotFoundError(f"Document not found: {document_path}")
            elif (
                "no address associated with hostname" in error_str
                or "could not resolve host" in error_str
            ):
                raise LatitudeAPIError(f"Failed to connect to Latitude API: {e}")
            else:
                raise LatitudeAPIError(f"Error loading document from Latitude SDK: {e}")

    async def _async_get_document(self, document_path: str) -> Any:
        """Async method to get document using SDK"""
        return await self.sdk.prompts.get(document_path)

    def _normalize_sdk_response(self, sdk_response: Any) -> Dict[str, Any]:
        """
        Normalize SDK response to match expected format

        Args:
            sdk_response: Response from Latitude SDK

        Returns:
            dict: Normalized response matching HTTP client format
        """
        # The SDK response structure may differ from HTTP API
        # This method normalizes it to maintain compatibility

        if hasattr(sdk_response, "__dict__"):
            # Convert SDK object to dict
            response_dict = vars(sdk_response)
        else:
            response_dict = sdk_response

        # VERY conservative approach: Only extract the absolute minimum fields
        # to avoid any "Extra inputs are not permitted" errors
        normalized = {}

        # 1. REQUIRED: prompt content
        prompt_content = None
        for content_field in ["content", "prompt", "text"]:
            if content_field in response_dict and response_dict[content_field]:
                prompt_content = response_dict[content_field]
                break

        if not prompt_content:
            raise LatitudeAPIError("No prompt content found in SDK response")

        # If prompt content has YAML frontmatter, we need to extract just the content part
        # Latitude prompts often have frontmatter like:
        # ---
        # provider: product_litellm
        # model: carto::gpt-4.1-mini
        # ---
        # Actual prompt content here

        # Strip YAML frontmatter and convert variable syntax
        prompt_content = strip_yaml_frontmatter(prompt_content)
        converted_prompt = convert_latitude_variables(prompt_content)
        normalized["prompt"] = converted_prompt

        # 2. OPTIONAL: system prompt (only if non-empty)
        for system_field in ["system", "system_prompt", "systemPrompt"]:
            if system_field in response_dict and response_dict[system_field]:
                if (
                    isinstance(response_dict[system_field], str)
                    and response_dict[system_field].strip()
                ):
                    # Convert Latitude's {{variable}} syntax to LLM's $variable syntax
                    system_prompt = convert_latitude_variables(
                        response_dict[system_field]
                    )
                    normalized["system"] = system_prompt
                    break

        # 3. OPTIONAL: defaults/parameters (only if it's a non-empty dict)
        for param_field in ["parameters", "params", "variables", "defaults"]:
            if param_field in response_dict and response_dict[param_field]:
                if (
                    isinstance(response_dict[param_field], dict)
                    and response_dict[param_field]
                ):
                    normalized["defaults"] = response_dict[param_field]
                    break

        # 4. OPTIONAL: model options (only if it's a non-empty dict)
        # IMPORTANT: Filter out problematic fields like 'model' and 'provider'
        for option_field in ["model_config", "modelConfig", "config", "options"]:
            if option_field in response_dict and response_dict[option_field]:
                if (
                    isinstance(response_dict[option_field], dict)
                    and response_dict[option_field]
                ):
                    # Filter out fields that cause "Extra inputs are not permitted" errors
                    filtered_options = filter_problematic_fields(
                        response_dict[option_field]
                    )

                    # Only include options if there are any valid fields left
                    if filtered_options:
                        normalized["options"] = filtered_options
                    break

        # 5. OPTIONAL: schema (only if non-empty)
        for schema_field in ["schema", "json_schema", "jsonSchema", "schema_object"]:
            if schema_field in response_dict and response_dict[schema_field]:
                normalized["schema_object"] = response_dict[schema_field]
                break

        # EXPLICITLY EXCLUDE fields that might cause "Extra inputs" errors:
        # - model, provider, modelName, recommended_model, etc.
        # - Any field not in the whitelist above

        return normalized


# All utility functions have been moved to utils.py and are imported at the top


def get_client_implementation() -> str:
    """
    Get the current client implementation being used

    Returns:
        str: "sdk" for SDK implementation, "http" for HTTP client
    """
    return "sdk"
