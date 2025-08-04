import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import litellm
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from minisweagent.models import GLOBAL_MODEL_STATS

logger = logging.getLogger("litellm_model")


@dataclass
class LitellmModelConfig:
    model_name: str
    model_kwargs: dict[str, Any] = field(default_factory=dict)
    litellm_model_registry: Path | None = None


class LitellmModel:
    def __init__(self, **kwargs):
        self.config = LitellmModelConfig(**kwargs)
        self.cost = 0.0
        self.n_calls = 0
        if self.config.litellm_model_registry is not None:
            litellm.utils.register_model(json.loads(Path(self.config.litellm_model_registry).read_text()))

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        retry=retry_if_not_exception_type(
            (
                litellm.exceptions.UnsupportedParamsError,
                litellm.exceptions.NotFoundError,
                litellm.exceptions.PermissionDeniedError,
                litellm.exceptions.ContextWindowExceededError,
                litellm.exceptions.APIError,
                litellm.exceptions.AuthenticationError,
                KeyboardInterrupt,
            )
        ),
    )
    def _query(self, messages: list[dict[str, str]], **kwargs):
        try:
            return litellm.completion(
                model=self.config.model_name, messages=messages, **(self.config.model_kwargs | kwargs)
            )
        except litellm.exceptions.AuthenticationError as e:
            e.message += " You can permanently set your API key with `mini-extra config set KEY VALUE`."
            raise e

    def query(self, messages: list[dict[str, str]], **kwargs) -> dict:
        response = self._query(messages, **kwargs)
        # cost = litellm.cost_calculator.completion_cost(response)  # コスト計算を無効化
        self.n_calls += 1
        # self.cost += cost  # コスト追加を無効化
        # GLOBAL_MODEL_STATS.add(cost)  # グローバル統計への追加を無効化
        GLOBAL_MODEL_STATS.add(0)  # コスト0で追加（呼び出し回数のみカウント）
        return {
            "content": response.choices[0].message.content or "",  # type: ignore
        }
