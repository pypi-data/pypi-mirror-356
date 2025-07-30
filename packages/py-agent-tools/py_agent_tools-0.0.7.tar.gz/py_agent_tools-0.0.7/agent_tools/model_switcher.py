from enum import Enum
from typing import Dict, List

from agent_tools.ark_agent import ArkCredentialPool, ArkModelName
from agent_tools.azure_agent import AzureOpenAICredentialPool, AzureOpenAIModelName
from agent_tools.bailian_agent import BailianCredentialPool, BailianModelName
from agent_tools.credential_pool_base import CredentialPoolBase
from agent_tools.openai_agent import OpenAICredentialPool, OpenAIModelName
from agent_tools.vertex_agent import VertexCredentialPool, VertexModelName


class ModelProvider(Enum):
    ARK = "ark"
    AZURE = "azure"
    BAILIAN = "bailian"
    OPENAI = "openai"
    VERTEX = "vertex"


class ModelSwitcher:
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider
        self._credential_pools: Dict[str, CredentialPoolBase] = {}
        self._initialize_credential_pools()

    def _initialize_credential_pools(self):
        """Initialize all credential pools for the specified provider."""
        if self.model_provider == ModelProvider.ARK:
            for model_name in ArkModelName:
                pool = ArkCredentialPool(target_model=model_name)
                self._credential_pools[model_name.value] = pool

        elif self.model_provider == ModelProvider.AZURE:
            for model_name in AzureOpenAIModelName:
                pool = AzureOpenAICredentialPool(target_model=model_name)
                self._credential_pools[model_name.value] = pool

        elif self.model_provider == ModelProvider.BAILIAN:
            for model_name in BailianModelName:
                pool = BailianCredentialPool(target_model=model_name)
                self._credential_pools[model_name.value] = pool

        elif self.model_provider == ModelProvider.OPENAI:
            for model_name in OpenAIModelName:
                pool = OpenAICredentialPool(target_model=model_name)
                self._credential_pools[model_name.value] = pool

        elif self.model_provider == ModelProvider.VERTEX:
            for model_name in VertexModelName:
                pool = VertexCredentialPool(target_model=model_name)
                self._credential_pools[model_name.value] = pool

    def get_model_provider(self) -> ModelProvider:
        return self.model_provider

    def get_available_models(self) -> List[str]:
        """Get list of available model names for the provider."""
        return list(self._credential_pools.keys())

    def get_credential_pool(self, model_name: str) -> CredentialPoolBase:
        """Get credential pool for a specific model."""
        if model_name not in self._credential_pools:
            raise ValueError(
                f"Model '{model_name}' not found for provider '{self.model_provider.value}'"
            )
        return self._credential_pools[model_name]

    async def start_all_pools(self):
        """Start all credential pools for health checking."""
        for pool in self._credential_pools.values():
            await pool.start()

    def stop_all_pools(self):
        """Stop all credential pools."""
        for pool in self._credential_pools.values():
            pool.stop()

    def get_pool_statistics(self) -> Dict[str, Dict]:
        """Get statistics for all credential pools."""
        stats = {}
        for model_name, pool in self._credential_pools.items():
            stats[model_name] = {
                "total_credentials": len(pool.model_credentials),
                "active_credentials": len(
                    [c for c in pool.credential_pool.values() if c.status.value == "active"]
                ),
                "inactive_credentials": len(
                    [c for c in pool.credential_pool.values() if c.status.value == "inactive"]
                ),
                "error_credentials": len(
                    [c for c in pool.credential_pool.values() if c.status.value == "error"]
                ),
                "rate_limited_credentials": len(
                    [c for c in pool.credential_pool.values() if c.status.value == "rate_limited"]
                ),
            }
        return stats


if __name__ == "__main__":
    import asyncio

    async def test_model_switcher():
        """Test the ModelSwitcher functionality."""
        # Test with different providers
        for provider in ModelProvider:
            print(f"\n=== Testing {provider.value.upper()} Provider ===")

            switcher = ModelSwitcher(provider)
            print(f"Available models: {switcher.get_available_models()}")

            # Start all pools for health checking
            await switcher.start_all_pools()

            # Get statistics
            stats = switcher.get_pool_statistics()
            print("Pool statistics:")
            for model, stat in stats.items():
                print(f"  {model}: {stat}")

            # Stop all pools
            switcher.stop_all_pools()
            print(f"Stopped all pools for {provider.value}")

    # Run the test
    try:
        asyncio.run(test_model_switcher())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            print("Tests completed successfully (cleanup warning ignored)")
        else:
            raise
