from typing import Any, Dict
import os
import requests
import uuid
import aiohttp
import asyncio
from af_client_sdk.types import GuardedResult, AnalysisContext
from af_client_sdk.utils import retry_with_exponential_backoff, async_retry_with_exponential_backoff
import logging

logger = logging.getLogger("af_client_sdk")


class ActiveFenceClient:
    """SDK Client for easier communication with ActiveFence API"""

    def __init__(
        self,
        api_key: str = os.environ.get("AF_API_KEY"),
        app_name: str = os.environ.get("AF_APP_NAME", "unknown"),
        base_url: str = os.environ.get("AF_URL_OVERRIDE", "https://apis.activefence.com"),
        provider: str = os.environ.get("AF_MODEL_PROVIDER", "unknown"),
        model_name: str = os.environ.get("AF_MODEL_NAME", "unknown"),
        model_version: str = os.environ.get("AF_MODEL_VERSION", "unknown"),
        platform: str = os.environ.get("AF_PLATFORM", "unknown"),
        api_timeout: int = int(os.environ.get("AF_API_TIMEOUT", 5)),
    ) -> None:
        """
        Initialize the ActiveFenceClient with configuration values.
        :param api_key: The supplied AF API key - provide if you want to override the env var or not use it
        :param app_name: Name of the app that is calling the API - provide if you want to override the env var
        :param base_url: Base URL for the ActiveFence API - provide if you want to override the env var
        :param provider: Default value for which LLM provider the client is analyzing (e.g. openai, anthropic, deepseek)
        :param model_name: Default value for name of the LLM model being used (e.g. gpt-3.5-turbo, claude-2)
        :param model_version: Default value for version of the LLM model being used (e.g. 2023-05-15)
        :param platform: Default value for cloud platform where the model is hosted (e.g. aws, azure, databricks)
        :param api_timeout: Timeout for API requests in seconds (default is 5 seconds)
        """
        self.base_url = base_url
        self.api_url = self.base_url + "/v1/evaluate/message"
        self.headers = {
            "Content-Type": "application/json",
            "af-api-key": api_key,
        }
        self.app_name = app_name

        self.provider = provider
        self.model_name = model_name
        self.model_version = model_version
        self.platform = platform

        self.api_timeout = api_timeout
        if asyncio.get_event_loop().is_running():
            self.http_client = aiohttp.ClientSession(
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
                },
                connector=aiohttp.TCPConnector(limit=5000, force_close=False),
            )
            self.timeout_seconds = aiohttp.ClientTimeout(total=self.api_timeout)

    def create_request_body(
        self,
        model: str,
        platform: str,
        provider: str,
        session_id: str,
        text: str,
        type: str,
        user_id: str,
        version: str,
    ) -> Dict:
        body = {
            "text": text,
            "message_type": type,
            "session_id": session_id or str(uuid.uuid4()),
            "user_id": user_id or str(uuid.uuid4()),
            "app_name": self.app_name,
            "model_context": {
                "provider": provider or self.provider,
                "name": model or self.model_name,
                "version": version or self.model_version,
                "cloud_platform": platform or self.platform,
            },
        }
        logger.debug("API request: %s", body)
        return body

    def handle_api_response(self, original_text: str, detection: Dict) -> GuardedResult:
        logger.debug("API response: %s", detection)

        action = detection["action"]
        blocked = action == "BLOCK"
        reason = detection["detections"][0]["type"] if len(detection["detections"]) > 0 else None
        response_text = original_text
        if action != "ALLOW":
            response_text = (
                detection["action_text"]
                if "action_text" in detection
                else "BLOCKED" if blocked else "*****"
            )

        return GuardedResult(
            blocked=blocked,
            reason=reason,
            final_response=response_text,
        )

    @retry_with_exponential_backoff(
        max_retries=int(os.environ.get("AF_RETRY_MAX", "3")),
        base_delay=float(os.environ.get("AF_RETRY_BASE_DELAY", "1")),
    )
    def sync_internal_call(
        self,
        text: str,
        type: str,
        session_id: str,
        user_id: str,
        provider: str,
        model: str,
        version: str,
        platform: str,
    ) -> GuardedResult:
        body = self.create_request_body(
            model, platform, provider, session_id, text, type, user_id, version
        )
        detection_response = requests.post(
            self.api_url,
            headers=self.headers,
            json=body,
            timeout=self.api_timeout,
        )
        if detection_response.status_code >= 300:
            raise Exception(f"{detection_response.status_code}:{detection_response.text}")

        return self.handle_api_response(text, detection_response.json())

    @async_retry_with_exponential_backoff(
        max_retries=int(os.environ.get("AF_RETRY_MAX", "3")),
        base_delay=float(os.environ.get("AF_RETRY_BASE_DELAY", "1")),
    )
    async def async_internal_call(
        self,
        text: str,
        type: str,
        session_id: str,
        user_id: str,
        provider: str,
        model: str,
        version: str,
        platform: str,
    ) -> GuardedResult:
        body = self.create_request_body(
            model, platform, provider, session_id, text, type, user_id, version
        )

        async with self.http_client.post(
            self.api_url,
            headers=self.headers,
            json=body,
            timeout=self.timeout_seconds,
        ) as detection_response:
            if detection_response.status >= 300:
                raise Exception(f"{detection_response.status}:{detection_response.text}")
            return self.handle_api_response(text, await detection_response.json())

    def evaluate_prompt_sync(self, prompt: str, context: AnalysisContext) -> GuardedResult:
        """
        Evaluate a user prompt that is sent to an LLM
        :param prompt: The text of the prompt to analyze
        :param context: Metadata for evaluation, fields that are not supplied will be taken from env vars
            session_id and user_id are required to group texts in the AF platform
        :return: GuardedResult object with analysis and detection results
        """
        return self.sync_internal_call(
            type="prompt",
            text=prompt,
            session_id=context.session_id,
            user_id=context.user_id,
            provider=context.provider,
            model=context.model,
            version=context.version,
            platform=context.platform,
        )

    def evaluate_response_sync(self, response: Any, context: AnalysisContext) -> GuardedResult:
        """
        Evaluate a return LLM response to a prompt.
        :param response: The LLM response to a given prompt
        :param context: Metadata for evaluation, fields that are not supplied will be taken from env vars
            session_id and user_id are required to group texts in the AF platform
        :return: GuardedResult object with analysis and detection results
        """
        return self.sync_internal_call(
            type="response",
            text=str(response),
            session_id=context.session_id,
            user_id=context.user_id,
            provider=context.provider,
            model=context.model,
            version=context.version,
            platform=context.platform,
        )

    async def evaluate_prompt(self, prompt: str, context: AnalysisContext) -> GuardedResult:
        """
        Evaluate a user prompt that is sent to an LLM, using asyncio
        :param prompt: The text of the prompt to analyze
        :param context: Metadata for evaluation, fields that are not supplied will be taken from env vars
            session_id and user_id are required to group texts in the AF platform
        :return: GuardedResult object with analysis and detection results
        """
        return await self.async_internal_call(
            type="prompt",
            text=prompt,
            session_id=context.session_id,
            user_id=context.user_id,
            provider=context.provider,
            model=context.model,
            version=context.version,
            platform=context.platform,
        )

    async def evaluate_response(self, response: Any, context: AnalysisContext) -> GuardedResult:
        """
        Evaluate a return LLM response to a prompt, using asyncio.
        :param response: The LLM response to a given prompt
        :param context: Metadata for evaluation, fields that are not supplied will be taken from env vars
            session_id and user_id are required to group texts in the AF platform
        :return: GuardedResult object with analysis and detection results
        """
        return await self.async_internal_call(
            type="response",
            text=str(response),
            session_id=context.session_id,
            user_id=context.user_id,
            provider=context.provider,
            model=context.model,
            version=context.version,
            platform=context.platform,
        )
