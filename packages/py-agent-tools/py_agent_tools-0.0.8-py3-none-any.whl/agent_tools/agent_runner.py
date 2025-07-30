import time
import traceback
from typing import Any, Callable

from pydantic_ai.agent import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.usage import Usage

from agent_tools._log import log


class AgentRunner:
    """
    AgentRunner is a class that
    1. keep model settings.
    2. runs an agent and returns the result.
    3. keep attempts, usage, and time_elapsed.
    """

    def __init__(
        self,
        elapsed_time: float = 0.0,
        attempts: int = 0,
        usage: Usage = Usage(),
        model_settings: ModelSettings = ModelSettings(),
    ):
        self.elapsed_time = elapsed_time
        self.attempts = attempts
        self.model_settings = model_settings
        self.usage = usage
        self.result: Any | None = None

    async def run(
        self,
        agent: Agent[Any, str],
        prompt: str,
        postprocess_fn: Callable[[str], str] | None = None,
    ) -> None:
        try:
            start_time = time.perf_counter()
            result = await agent.run(
                prompt,
                model_settings=self.model_settings,
            )
            self.usage += result.usage()
            self.elapsed_time = self.elapsed_time + (time.perf_counter() - start_time)
            self.result = result.output
        except Exception as e:
            self.attempts = self.attempts + 1
            log.error(traceback.format_exc())
            log.error(f'AgentRunner failed: {self.attempts} attempts')
            raise e

        if postprocess_fn:
            try:
                self.result = postprocess_fn(self.result)
            except Exception as e:
                self.attempts = self.attempts + 1
                log.error(traceback.format_exc())
                log.error(f'Postprocess function failed: {self.attempts} attempts')
                raise e

    async def embedding(
        self,
        client: Any,
        model_name: str,
        input: str,
        dimensions: int = 1024,
    ) -> None:
        try:
            start_time = time.perf_counter()
            response = await client.embeddings.create(
                model=model_name,
                input=input,
                dimensions=dimensions,
            )
            self.usage += response.usage()
            self.elapsed_time = self.elapsed_time + (time.perf_counter() - start_time)
            self.result = response.data[0].embedding
        except Exception as e:
            self.attempts = self.attempts + 1
            log.error(traceback.format_exc())
            log.error(f'Embedding failed: {self.attempts} attempts')
            raise e
