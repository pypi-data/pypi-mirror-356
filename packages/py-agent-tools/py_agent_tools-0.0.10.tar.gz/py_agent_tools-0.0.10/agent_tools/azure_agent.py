from enum import Enum

from openai import AsyncAzureOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from agent_tools.agent_base import AgentBase
from agent_tools.credential_pool_base import CredentialPoolBase, ModelCredential
from agent_tools.settings import agent_settings


class AzureModelName(str, Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    O3_MINI = "o3-mini"
    O4_MINI = "o4-mini"
    O3 = "o3"


class AzureEmbeddingModelName(str, Enum):
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"


class AzureAgent(AgentBase):
    def create_client(self) -> AsyncAzureOpenAI:
        if self.credential is None:
            raise ValueError("Credential is not initialized")
        return AsyncAzureOpenAI(
            api_version=self.credential.api_version,
            azure_endpoint=self.credential.base_url,
            api_key=self.credential.api_key,
            azure_deployment=self.credential.deployment,
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
    agent = await AzureAgent.create(credential=credential)
    return await agent.validate_credential()


class AzureCredentialPool(CredentialPoolBase):
    def __init__(self, target_model: AzureModelName):
        super().__init__(
            target_model=target_model,
            account_credentials=agent_settings.azure.credentials,
            validate_fn=validate_fn,
        )


if __name__ == "__main__":
    import asyncio

    async def test_all_credentials():
        for model_name in AzureModelName:
            credential_pool = AzureCredentialPool(target_model=model_name)
            for credential in credential_pool.model_credentials:
                if "embedding" in model_name.value:
                    continue
                try:
                    agent = await AzureAgent.create(credential=credential)
                    result = await agent.validate_credential()
                    if result is True:
                        print(f"{credential.id} is valid.")
                    else:
                        print(f"{credential.id} is invalid!")
                except Exception as e:
                    print(f"error: {e}")
                    continue

    async def test_credential_pool_manager():
        credential_pool = AzureCredentialPool(target_model=AzureModelName.GPT_4O)
        await credential_pool.start()

        agent = await AzureAgent.create(credential_pool=credential_pool)
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
