from __future__ import annotations

from typing import AsyncGenerator, Dict, Iterator, List, Any

from greennode.abstract import api_requestor
from greennode.greennode_response import GreenNodeResponse
from greennode.types import (
    CompletionChunk,
    CompletionRequest,
    CompletionResponse,
    GreenNodeClient,
    GreenNodeRequest,
)


class Completions:
    def __init__(self, client: GreenNodeClient) -> None:
        self._client = client

    def create(
        self,
        *,
        prompt: str,
        model: str,
        max_tokens: int | None = 512,
        stop: List[str] | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        repetition_penalty: float | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        min_p: float | None = None,
        logit_bias: Dict[str, float] | None = None,
        seed: int | None = None,
        stream: bool = False,
        logprobs: int | None = None,
        echo: bool | None = None,
        n: int | None = None,
        **kwargs: Any,
    ) -> CompletionResponse | Iterator[CompletionChunk]:
        """
        Method to generate completions based on a given prompt using a specified model.

        Args:
            prompt (str): A string providing context for the model to complete.
            model (str): The name of the model to query.
            max_tokens (int, optional): The maximum number of tokens to generate.
                Defaults to 512.
            stop (List[str], optional): List of strings at which to stop generation.
                Defaults to None.
            temperature (float, optional): A decimal number that determines the degree of randomness in the response.
                Defaults to None.
            top_p (float, optional): The top_p (nucleus) parameter is used to dynamically adjust the number
                    of choices for each predicted token based on the cumulative probabilities.
                Defaults to None.
            top_k (int, optional): The top_k parameter is used to limit the number of choices for the
                    next predicted word or token.
                Defaults to None.
            repetition_penalty (float, optional): A number that controls the diversity of generated text
                    by reducing the likelihood of repeated sequences. Higher values decrease repetition.
                Defaults to None.
            presence_penalty (float, optional): A number that controls the likelihood of tokens based on if they have
                    appeared in the text. Positive values decrease the likelihood of repeated tokens or phrases.
                    Must be in the range [-2, 2].
                Defaults to None.
            frequency_penalty (float, optional): A number that controls the likelihood of tokens based on the frequency
                    of their appearance in the text. Positive decrease the likelihood of repeated tokens or phrases.
                    Must be in the range [-2, 2].
                Defaults to None.
            min_p (float, optional): A number that controls the minimum percentage value that a token must reach to
                be considered during sampling.
                Must be in the range [0, 1].
                Defaults to None.
            logit_bias (Dict[str, float], optional): A dictionary of tokens and their bias values that modify the
                likelihood of specific tokens being sampled. Bias values must be in the range [-100, 100].
                Defaults to None.
            seed (int, optional): Seed value for reproducibility.
            stream (bool, optional): Flag indicating whether to stream the generated completions.
                Defaults to False.
            logprobs (int, optional): Number of top-k logprobs to return
                Defaults to None.
            echo (bool, optional): Echo prompt in output. Can be used with logprobs to return prompt logprobs.
                Defaults to None.
            n (int, optional): Number of completions to generate. Setting to None will return a single generation.
                Defaults to None.

        Returns:
            CompletionResponse | Iterator[CompletionChunk]: Object containing the completions
            or an iterator over completion chunks.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = CompletionRequest(
            model=model,
            prompt=prompt,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            repetition_penalty=repetition_penalty,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            seed=seed,
            min_p=min_p,
            logit_bias=logit_bias,
            stream=stream,
            logprobs=logprobs,
            echo=echo,
            n=n,
            **kwargs,
        ).model_dump(exclude_none=True)

        response, _, _ = requestor.request(
            options=GreenNodeRequest(
                method="POST",
                url="completions",
                params=parameter_payload,
            ),
            stream=stream,
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, GreenNodeResponse)
            return (CompletionChunk(**line.data) for line in response)
        assert isinstance(response, GreenNodeResponse)
        return CompletionResponse(**response.data)

