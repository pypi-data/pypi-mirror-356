from enum import Enum

import httpx
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

from agent_tools.agent_base import AgentBase
from agent_tools.credential_pool_base import CredentialPoolBase, ModelCredential
from agent_tools.settings import agent_settings


class VertexModelName(str, Enum):
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_2_0_FLASH_THINKING_EXP_01_21 = "gemini-2.0-flash-thinking-exp-01-21"
    GEMINI_2_5_PRO_EXP_03_25 = "gemini-2.5-pro-exp-03-25"


class VertexAgent(AgentBase):
    def create_client(self) -> httpx.AsyncClient:
        raise NotImplementedError("VertexAgent does not support create_client")

    def create_model(self) -> GeminiModel:
        if self.credential is None:
            raise ValueError("Credential is not initialized")
        return GeminiModel(
            model_name=self.credential.model_name,
            provider=GoogleVertexProvider(
                service_account_info=self.credential.account_info,
                http_client=httpx.AsyncClient(timeout=300),
            ),
        )

    def embedding(self, input: str, dimensions: int = 1024):
        raise NotImplementedError("VertexAgent does not support embedding")


async def validate_fn(credential: ModelCredential) -> bool:
    agent = await VertexAgent.create(credential=credential)
    return await agent.validate_credential()


class VertexCredentialPool(CredentialPoolBase):
    def __init__(self, target_model: VertexModelName):
        super().__init__(
            target_model=target_model,
            account_credentials=agent_settings.vertex.credentials,
            validate_fn=validate_fn,
        )


if __name__ == "__main__":
    import asyncio

    async def test_all_credentials():
        for model_name in VertexModelName:
            credential_pool = VertexCredentialPool(target_model=model_name)
            for credential in credential_pool.model_credentials:
                try:
                    agent = await VertexAgent.create(credential=credential)
                    result = await agent.validate_credential()
                    if result is True:
                        print(f"{credential.id} is valid.")
                    else:
                        print(f"{credential.id} is invalid!")
                except Exception as e:
                    print(f"error: {e}")
                    continue

    async def test_credential_pool_manager():
        credential_pool = VertexCredentialPool(target_model=VertexModelName.GEMINI_2_0_FLASH)
        await credential_pool.start()

        agent = await VertexAgent.create(credential_pool=credential_pool)
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
