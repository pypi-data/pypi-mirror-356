from __future__ import annotations

import os
import re
from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Literal, Optional

import pandas as pd
from typing_extensions import override

from dbnl.eval.llm import AzureOpenAILLMClient, LLMClient, OpenAILLMClient
from dbnl.tqdm import configure_tqdm

from .metric import Metric

DEFAULT_METRIC_VERSION = "v0"


class MetricValue:
    def __init__(self, scores: list[Any], justifications: list[Any]):
        self.scores = scores
        self.justifications = justifications


def _extract_score_and_justification(output: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Extracts the score and justification from the output string.
    """
    # Example output: "Score: 4.5\nJustification: This is a good response."
    if output is None:
        return None, None
    try:
        score_str, justification_str = output.split("\n")
        score = re.search(r"score:\s*([\d.]+)", score_str)
        justification = re.search(r"justification:\s*(.*)", justification_str)
        if score and justification:
            return score.group(1), justification.group(1)
    except Exception:
        pass
    return None, None


@contextmanager
def _set_env(**environ: str) -> Generator[None, None, None]:
    curr = os.environ.copy()
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(curr)


class GenAIMetric(Metric, ABC):
    def __init__(
        self,
        base_name: str,
        eval_llm_client: LLMClient,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        self._base_name = base_name
        self._eval_llm_client = eval_llm_client
        self._version = version

    def metric(self) -> str:
        return f"{self._base_name}_{self._version}"

    def description(self) -> str:
        return "See Distributional's metric augmentation documentation for more information."

    @override
    def greater_is_better(self) -> Optional[bool]:
        # NOTE: ignore for now
        gib = None
        return bool(gib) if gib is not None else None

    @property
    def version(self) -> Optional[str]:
        return self._version

    @override
    def evaluate(self, eval_df: pd.DataFrame) -> pd.Series[Any]:
        env_vars: dict[str, str] = {}
        # hack to use envvars from client
        # make sure this works with vanilla openAI client
        if isinstance(self._eval_llm_client, AzureOpenAILLMClient):
            env_vars = {
                "OPENAI_API_TYPE": "azure",
                "OPENAI_API_VERSION": self._eval_llm_client.client._api_version,
                "OPENAI_API_BASE": str(self._eval_llm_client.client.base_url).split("openai/")[0],
                "OPENAI_API_KEY": self._eval_llm_client.client.api_key,
                "OPENAI_DEPLOYMENT_NAME": self._eval_llm_client.llm_model,
            }
        elif isinstance(self._eval_llm_client, OpenAILLMClient):
            env_vars = {
                "OPENAI_API_KEY": self._eval_llm_client.client.api_key,
                "OPENAI_API_BASE": str(self._eval_llm_client.client.base_url).split("openai/")[0][:-1],
            }

        with _set_env(**env_vars), configure_tqdm():
            value = self.evaluate_with_client(eval_df)

        assert isinstance(value.scores, list)
        # ensure this is going to be an int
        if self.type() == "int":
            return pd.Series(data=value.scores, dtype="int32[pyarrow]")
        else:
            raise ValueError(f"Unsupported type for metric {self.metric()}: {self.type()}")

    @abstractmethod
    def evaluate_with_client(self, eval_df: pd.DataFrame) -> MetricValue: ...


class GenAIFromPromptEvaluationMetric(GenAIMetric):
    def __init__(
        self,
        name: str,
        judge_prompt: str,
        eval_llm_client: LLMClient,
        prediction: Optional[str] = None,
        input: Optional[str] = None,
        context: Optional[str] = None,
        target: Optional[str] = None,
        greater_is_better: Optional[bool] = None,
        version: Optional[str] = DEFAULT_METRIC_VERSION,
    ):
        super().__init__(name, eval_llm_client, version=version)
        self._judge_prompt = judge_prompt
        self._prediction = prediction
        self._context = context
        self._input = input
        self._target = target

    def name(self) -> str:
        metric = self.metric()
        args_candidates = [self._prediction, self._input, self._context, self._target]
        res = "__".join([metric] + [arg for arg in args_candidates if arg is not None])
        return res

    @override
    def inputs(self) -> list[str]:
        return [arg for arg in [self._prediction, self._input, self._context, self._target] if arg is not None]

    def expression(self) -> str:
        res = f"{self.metric()}("
        if self._prediction is not None:
            res += f"{self._prediction}"
        if self._input is not None:
            res += f", {self._input}"
        if self._target is not None:
            res += f", {self._target}"
        if self._context is not None:
            res += f", {self._context}"
        res += ")"
        return res

    def type(self) -> Literal["int"]:
        return "int"

    @override
    def component(self) -> Optional[str]:
        if self._prediction is not None:
            if self._input is not None:
                return f"{self._input}__{self._prediction}"
            return self._prediction
        return None

    @override
    def evaluate_with_client(
        self,
        eval_df: pd.DataFrame,
    ) -> MetricValue:
        col_names_to_use = [c for c in {self._prediction, self._input, self._target, self._context} if c is not None]
        subset_df = eval_df[col_names_to_use]

        FMT_NAMES = {
            self._prediction: "prediction",
            self._input: "input",
            self._target: "target",
            self._context: "context",
        }

        scores, justifications = [], []
        llm_client = self._eval_llm_client
        for idx, row in subset_df.iterrows():
            # prompt expectes "prediction", but df has self._prediction column name
            fmt_inputs = {FMT_NAMES[col]: row[col] for col in col_names_to_use}
            prompt = self._judge_prompt.format(**fmt_inputs)
            output = llm_client.call(prompt)
            score_str, justification = _extract_score_and_justification(output.content)
            if score_str is not None:
                try:
                    score = min(max(int(float(score_str)), 1), 5)
                except ValueError:
                    score = None
            else:
                score = None
            scores.append(score)
            justifications.append(justification)
        value = MetricValue(scores=scores, justifications=justifications)

        assert isinstance(value, MetricValue)
        return value
