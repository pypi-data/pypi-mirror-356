import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import boto3
from openai import AzureOpenAI, OpenAI
from typing_extensions import override


@dataclass
class LLMResponse:
    content: Optional[str]


class LLMClient(ABC):
    """Abstract interface to be implemented by all LLM providers."""

    @abstractmethod
    def id(self) -> str:
        """
        Returns a unique identifier for the LLM client. For example, an LLM client for the OpenAPI
        GPT-4 model might have an id of `openai:gpt4`. Used to uniquely identify the client.

        :return: LLM client id.
        """
        raise NotImplementedError()

    @abstractmethod
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """
        Calls the underlying LLM provider with the provided prompt.

        :param prompt: Prompt text.
        :return: LLMResponse.
        """
        raise NotImplementedError()


class OpenAILLMClient(LLMClient):
    """LLM client that wraps the OpenAI client."""

    def __init__(self, api_key: str, llm_model: str):
        """
        Initialize the AzureOpenAILLMClient with the provided API key, API version, Azure endpoint, and LLM model.

        :param api_key: Azure OpenAI API key.
        :param api_version: Azure OpenAI API version.
        :param azure_endpoint: Azure OpenAI endpoint.
        :param llm_model: LLM model.
        """
        self.client = OpenAI(api_key=api_key)
        self.temperature = 0.0
        self.llm_model = llm_model

    @classmethod
    def from_existing_client(cls, client: OpenAI, llm_model: str) -> LLMClient:
        """
        Alternative constructor that initializes the AzureOpenAILLMClient with an existing AzureOpenAI client and LLM model.

        :param client: Existing AzureOpenAI client.
        :param llm_model: LLM model.
        :return: An instance of AzureOpenAILLMClient.
        """
        instance = cls.__new__(cls)
        instance.client = client
        instance.llm_model = llm_model
        instance.temperature = 0.0
        return instance

    @override
    def id(self) -> str:
        """
        Returns a unique identifier for the Azure OpenAI LLM client.

        :return: Azure OpenAI LLM client id.
        """
        return f"openai:/{self.llm_model}"

    @override
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """
        Calls the OpenAI LLM provider with the provided prompt.

        :param prompt: Prompt text.
        :return: LLMResponse.
        """
        if not system_prompt:
            system_prompt = "You are a helpful AI assistant"

        response = self.client.chat.completions.create(
            model=self.llm_model,
            temperature=self.temperature,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        )

        return LLMResponse(content=response.choices[0].message.content)


class AzureOpenAILLMClient(LLMClient):
    """LLM client that wraps the AzureOpenAI client."""

    def __init__(self, api_key: str, api_version: str, azure_endpoint: str, llm_model: str):
        """
        Initialize the AzureOpenAILLMClient with the provided API key, API version, Azure endpoint, and LLM model.

        :param api_key: Azure OpenAI API key.
        :param api_version: Azure OpenAI API version.
        :param azure_endpoint: Azure OpenAI endpoint.
        :param llm_model: LLM model.
        """
        self.client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
        self.temperature = 0.0
        self.llm_model = llm_model

    @classmethod
    def from_existing_client(cls, client: AzureOpenAI, llm_model: str) -> LLMClient:
        """
        Alternative constructor that initializes the AzureOpenAILLMClient with an existing AzureOpenAI client and LLM model.

        :param client: Existing AzureOpenAI client.
        :param llm_model: LLM model.
        :return: An instance of AzureOpenAILLMClient.
        """
        instance = cls.__new__(cls)
        instance.client = client
        instance.llm_model = llm_model
        instance.temperature = 0.0
        return instance

    @override
    def id(self) -> str:
        """
        Returns a unique identifier for the Azure OpenAI LLM client.

        :return: Azure OpenAI LLM client id.
        """

        return f"openai:/{self.llm_model}"

    @override
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """
        Calls the Azure OpenAI LLM provider with the provided prompt.

        :param prompt: Prompt text.
        :return: LLMResponse.
        """
        if not system_prompt:
            system_prompt = "You are a helpful AI assistant"

        response = self.client.chat.completions.create(
            model=self.llm_model,
            temperature=self.temperature,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        )

        return LLMResponse(content=response.choices[0].message.content)


class SageMakerFormat:
    BEGIN = "<|begin_of_text|>"
    USER_HEADER = "<|start_header_id|>user<|end_header_id|>"
    SYSTEM_HEADER = "<|start_header_id|>system<|end_header_id|>"
    ASSISTANT_HEADER = "<|start_header_id|>assistant<|end_header_id|>"
    END = "<|eot_id|>"
    END_TEXT = "<|end_of_text|>"


class SageMakerLLMClient(LLMClient):
    """LLM client that wraps the SageMaker client."""

    DEFAULT_MAX_TOKENS = 512
    DEFAULT_TEMPERATURE = 0.7

    def __init__(self, endpoint_name: str, region_name: Optional[str] = None):
        """
        Initialize the SageMakerLLMClient with the provided endpoint name and region name.

        :param endpoint_name: SageMaker endpoint name.
        :param region_name: AWS region name.
        """
        if region_name is None:
            region_name = "us-east-1"
        self.runtime_client = boto3.client("sagemaker-runtime", region_name=region_name)
        self.endpoint_name = endpoint_name

    @override
    def id(self) -> str:
        """
        Returns a unique identifier for the SageMaker LLM client.

        :return: SageMaker LLM client id.
        """
        return f"sagemaker:/{self.endpoint_name}"

    def _generate_prompt(self, messages: list[dict[str, str]]) -> str:
        PROMPT_MAP = {
            "user": SageMakerFormat.USER_HEADER,
            "system": SageMakerFormat.SYSTEM_HEADER,
            "assistant": SageMakerFormat.ASSISTANT_HEADER,
        }

        prompt = ""
        for msg in messages:
            prefix = PROMPT_MAP.get(msg["role"])
            prompt += f'{prefix}\n\n{msg["content"]}{SageMakerFormat.END}'
        return f"{SageMakerFormat.BEGIN}{prompt}{SageMakerFormat.ASSISTANT_HEADER}\n\n{SageMakerFormat.END}{SageMakerFormat.END_TEXT}"

    def _call_once(self, messages: list[dict[str, str]]) -> str:
        prompt = self._generate_prompt(messages)
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": self.DEFAULT_MAX_TOKENS,
                "return_full_text": False,
                "do_sample": True,
                "temperature": self.DEFAULT_TEMPERATURE,
            },
        }

        response = self.runtime_client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            Body=json.dumps(payload),
            ContentType="application/json",
            CustomAttributes="accept_eula=true",
        )

        result = response["Body"].read().decode("utf-8")
        try:
            result_json = json.loads(result)
            content = result_json[0]["generated_text"].strip()

            # Might be unnecessary? but just in case
            content = (
                content.replace(prompt, "")
                .replace(SageMakerFormat.END, "")
                .replace(SageMakerFormat.END_TEXT, "")
                .strip()
            )

        except json.JSONDecodeError:
            content = result

        return str(content)

    @override
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """
        Calls the SageMaker LLM provider with the provided prompt.

        :param prompt: Prompt text.
        :return: LLMResponse.
        """
        if not system_prompt:
            system_prompt = "You are a helpful AI assistant"

        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

        content = self._call_once(messages)
        return LLMResponse(content=content)
