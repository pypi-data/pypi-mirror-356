from enum import Enum

from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from agent_tools.agent_base import AgentBase
from agent_tools.credential_pool_base import CredentialPoolBase, ModelCredential
from agent_tools.settings import agent_settings


class OpenAIModelName(str, Enum):
    GPT_4O_2024_11_20 = "gpt-4o-2024-11-20"
    GPT_4O_MINI_2024_07_18 = "gpt-4o-mini-2024-07-18"
    O3_MINI_2025_01_31 = "o3-mini-2025-01-31"
    O4_MINI_2025_04_16 = "o4-mini-2025-04-16"


class OpenAIEmbeddingModelName(str, Enum):
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"


class OpenAIAgent(AgentBase):

    def create_client(self):
        if self.credential is None:
            raise ValueError("Credential is not initialized")
        return AsyncOpenAI(
            api_key=self.credential.api_key,
            base_url=self.credential.base_url,
        )

    def create_model(self):
        if self.credential is None:
            raise ValueError("Credential is not initialized")
        client = self.create_client()
        return OpenAIModel(
            model_name=self.credential.model_name,
            provider=OpenAIProvider(openai_client=client),
        )


async def validate_fn(credential: ModelCredential) -> bool:
    agent = await OpenAIAgent.create(credential=credential)
    return await agent.validate_credential()


class OpenAICredentialPool(CredentialPoolBase):
    def __init__(self, target_model: OpenAIModelName):
        super().__init__(
            target_model=target_model,
            account_credentials=agent_settings.openai.credentials,
            validate_fn=validate_fn,
        )


if __name__ == "__main__":
    import asyncio

    async def test_all_credentials():
        for model_name in OpenAIModelName:
            credential_pool = OpenAICredentialPool(target_model=model_name)
            for credential in credential_pool.model_credentials:
                if "embedding" in model_name.value:
                    continue
                try:
                    agent = await OpenAIAgent.create(credential=credential)
                    result = await agent.validate_credential()
                    if result is True:
                        print(f"{credential.id} is valid.")
                    else:
                        print(f"{credential.id} is invalid!")
                except Exception as e:
                    print(f"error: {e}")
                    continue

    async def test_credential_pool_manager():
        credential_pool = OpenAICredentialPool(target_model=OpenAIModelName.GPT_4O_2024_11_20)
        await credential_pool.start()

        agent = await OpenAIAgent.create(credential_pool=credential_pool)
        result = await agent.run('this is a test, just echo "hello"')
        print(result)

        credential_pool.stop()

    async def test():
        """Main function that runs all tests with proper cleanup."""
        await test_all_credentials()
        await test_credential_pool_manager()

    try:
        asyncio.run(test())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            print("Tests completed successfully (cleanup warning ignored)")
        else:
            raise
