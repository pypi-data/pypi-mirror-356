from enum import Enum

from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from agent_tools.agent_base import AgentBase
from agent_tools.credential_pool_base import CredentialPoolBase, ModelCredential
from agent_tools.settings import agent_settings


class BailianModelName(str, Enum):
    QWEN_TURBO_LATEST = "qwen-turbo-latest"
    QWEN_PLUS_LATEST = "qwen-plus-latest"
    DEEPSEEK_R1 = "deepseek-r1"
    DEEPSEEK_V3 = "deepseek-v3"


class BailianAgent(AgentBase):
    """Bailian agent.

    Args:
        model_settings: The model settings to use for the agent.
        可配置参数：
        https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.2eac7b08zY6yxZ&tab=api#/api/?type=model&url=https%3A%2F%2Fhelp.aliyun.com%2Fdocument_detail%2F2712576.html
        限制思考长度：
        https://help.aliyun.com/zh/model-studio/deep-thinking?spm=0.0.0.i0#e7c0002fe4meu
    """

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

    def embedding(self) -> OpenAIModel:
        raise NotImplementedError("Bailian does not support embedding.")


async def validate_fn(credential: ModelCredential) -> bool:
    agent = await BailianAgent.create(credential=credential)
    return await agent.validate_credential()


class BailianCredentialPool(CredentialPoolBase):
    def __init__(self, target_model: BailianModelName):
        super().__init__(
            target_model=target_model,
            account_credentials=agent_settings.bailian.credentials,
            validate_fn=validate_fn,
        )


if __name__ == "__main__":
    import asyncio

    async def test_all_credentials():
        for model_name in BailianModelName:
            credential_pool = BailianCredentialPool(target_model=model_name)
            for credential in credential_pool.model_credentials:
                try:
                    agent = await BailianAgent.create(credential=credential)
                    result = await agent.validate_credential()
                    if result is True:
                        print(f"{credential.id} is valid.")
                    else:
                        print(f"{credential.id} is invalid!")
                except Exception as e:
                    print(f"error: {e}")
                    continue

    async def test_credential_pool_manager():
        credential_pool = BailianCredentialPool(target_model=BailianModelName.QWEN_TURBO_LATEST)
        await credential_pool.start()

        agent = await BailianAgent.create(credential_pool=credential_pool)
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
