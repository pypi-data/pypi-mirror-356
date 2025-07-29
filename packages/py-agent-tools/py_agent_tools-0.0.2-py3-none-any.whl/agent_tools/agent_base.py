from abc import ABC, abstractmethod
from typing import Any, Callable

from pydantic_ai.agent import Agent
from pydantic_ai.models.openai import Model
from pydantic_ai.settings import ModelSettings

from agent_tools.agent_factory import AgentFactory
from agent_tools.agent_runner import AgentRunner
from agent_tools.credential_pool_base import CredentialPoolProtocol, ModelCredential, StatusType


class AgentBase(ABC):
    """Base class for all agents.

    Args:
        credential or credential_pool: Exactly one of credential or credential_pool
            must be provided.
        system_prompt: The system prompt to use for the agent.
        max_retries: The maximum number of retries to make when the agent fails.
        model_settings: The model settings to use for the agent.
    """

    def __init__(
        self,
        credential: ModelCredential | None = None,
        credential_pool: CredentialPoolProtocol | None = None,
        system_prompt: str | None = None,
        max_retries: int = 3,
        model_settings: ModelSettings = ModelSettings(temperature=1),
    ):
        if (credential is None) == (credential_pool is None):
            raise ValueError("Exactly one of credential or credential_pool must be None")

        self.credential = credential
        self.credential_pool = credential_pool
        self.max_retries = max_retries
        self.system_prompt: str | None = system_prompt
        self.client = None
        self.model: Model | None = None
        self.agent: Agent[Any, str] | None = None
        self.runner = AgentRunner(
            model_settings=model_settings,
        )

    @classmethod
    async def create(
        cls,
        credential: ModelCredential | None = None,
        credential_pool: CredentialPoolProtocol | None = None,
        system_prompt: str | None = None,
        max_retries: int = 3,
        model_settings: ModelSettings = ModelSettings(temperature=1),
    ) -> "AgentBase":
        instance = cls(credential, credential_pool, system_prompt, max_retries, model_settings)
        instance.credential = await instance._initialize_credential(credential, credential_pool)
        instance.client = instance.create_client()
        return instance

    async def _initialize_credential(
        self,
        credential: ModelCredential | None,
        credential_pool: CredentialPoolProtocol | None,
    ):
        if credential_pool is not None:
            return await credential_pool.get_best()
        elif credential is not None:
            return credential
        else:
            raise ValueError("Either credential or credential_pool must be provided")

    async def _switch_credential(self):
        if self.credential_pool is not None and self.credential is not None:
            await self.credential_pool.update_status(self.credential, StatusType.ERROR)
            self.credential = await self.credential_pool.get_best()
            self.client = self.create_client()
        self.max_retries -= 1
        if self.max_retries <= 0:
            raise ValueError("Max retries reached")

    @abstractmethod
    def create_client(self) -> Any:
        """Create a client for the agent by self.credential"""
        pass

    @abstractmethod
    def create_model(self) -> Model:
        """Create a model for the agent according to model provider"""
        pass

    def create_agent(self) -> Agent[Any, str]:
        """Default agent creation function"""
        self.model = self.create_model()
        return AgentFactory.create_agent(
            self.model,
            system_prompt=self.system_prompt,
        )

    async def run(
        self, prompt: str, postprocess_fn: Callable[[str], Any] | None = None
    ) -> AgentRunner:
        """Run with retries"""
        self.agent = self.create_agent()
        try:
            await self.runner.run(self.agent, prompt, postprocess_fn=postprocess_fn)
        except Exception:
            await self._switch_credential()
            return await self.run(prompt, postprocess_fn=postprocess_fn)
        return self.runner

    async def validate_credential(self) -> bool:
        try:
            await self.run('echo "hello"')
            return True
        except Exception:
            return False

    async def embedding(
        self,
        input: str,
        dimensions: int = 1024,
    ) -> AgentRunner:
        """Embedding with retries"""
        self.model = self.create_model()
        if 'embedding' not in self.model.model_name:
            raise ValueError("Model is not an embedding model, use run instead")
        try:
            await self.runner.embedding(self.client, self.model.model_name, input, dimensions)
        except Exception:
            await self._switch_credential()
            return await self.embedding(input, dimensions)
        return self.runner
