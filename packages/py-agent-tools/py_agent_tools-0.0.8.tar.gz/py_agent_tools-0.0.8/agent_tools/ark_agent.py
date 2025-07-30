from enum import Enum

from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from agent_tools.agent_base import AgentBase
from agent_tools.credential_pool_base import CredentialPoolBase, ModelCredential
from agent_tools.settings import agent_settings


class ArkModelName(str, Enum):
    DEEPSEEK_R1_250528 = "deepseek-r1-250528"
    DEEPSEEK_V3_250324 = "deepseek-v3-250324"
    DOUBAO_SEED_1_6_250615 = "doubao-seed-1-6-250615"
    DOUBAO_SEED_1_6_THINKING_250615 = "doubao-seed-1-6-thinking-250615"
    DOUBAO_SEED_1_6_FLASH_250615 = "doubao-seed-1-6-flash-250615"


class ArkEmbeddingModelName(str, Enum):
    DOUBAO_EMBEDDING_VISION_250328 = "doubao-embedding-vision-250328"
    DOUBAO_EMBEDDING_LARGE_TEXT_240915 = "doubao-embedding-large-text-240915"


class ArkAgent(AgentBase):
    def create_client(self) -> AsyncOpenAI:
        if self.credential is None:
            raise ValueError("Credential is not initialized")
        return AsyncOpenAI(
            api_key=self.credential.api_key,
            base_url=self.credential.base_url,
        )

    def create_model(self) -> OpenAIModel:
        if self.credential is None:
            raise ValueError("Credential is not initialized")
        client = self.create_client()
        return OpenAIModel(
            model_name=self.credential.model_name,
            provider=OpenAIProvider(openai_client=client),
        )


async def validate_fn(credential: ModelCredential) -> bool:
    agent = await ArkAgent.create(credential=credential)
    return await agent.validate_credential()


class ArkCredentialPool(CredentialPoolBase):
    def __init__(self, target_model: ArkModelName):
        super().__init__(
            target_model=target_model,
            account_credentials=agent_settings.ark.credentials,
            validate_fn=validate_fn,
        )


if __name__ == "__main__":
    import asyncio

    async def test_all_credentials():
        for model_name in ArkModelName:
            credential_pool = ArkCredentialPool(target_model=model_name)
            for credential in credential_pool.model_credentials:
                if "embedding" in model_name.value:
                    continue
                try:
                    agent = await ArkAgent.create(credential=credential)
                    result = await agent.validate_credential()
                    if result is True:
                        print(f"{credential.id} is valid.")
                    else:
                        print(f"{credential.id} is invalid!")
                except Exception as e:
                    print(f"error: {e}")
                    continue

    async def test_credential_pool_manager():
        credential_pool = ArkCredentialPool(target_model=ArkModelName.DOUBAO_SEED_1_6_250615)
        await credential_pool.start()

        agent = await ArkAgent.create(credential_pool=credential_pool)
        runner = await agent.run("hello")
        print(runner.result)

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
