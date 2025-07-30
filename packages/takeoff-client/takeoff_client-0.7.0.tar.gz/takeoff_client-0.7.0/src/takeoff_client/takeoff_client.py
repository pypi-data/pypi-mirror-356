"""This module contains the TakeoffClient class, which is used to interact with the Takeoff server."""

# ────────────────────────────────────────────────────── Import ────────────────────────────────────────────────────── #
import json
from pathlib import Path
from typing import Any, AsyncIterator, Dict, Iterator, List, Union, Optional

import httpx
from takeoff_config import ReaderConfig

from .exceptions import TakeoffException
from .sse import Event, SSEClient, SSEClientAsync

# 10 second timeout for connecting, writing, pooling. No limit for reading data
REQUEST_TIMEOUT = httpx.Timeout(10.0, read=None)

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                    Takeoff Client                                                    #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
ChatTemplateMessage = List[Dict[str, str]]


class TakeoffClient:
    def __init__(
        self,
        base_url: str = "http://localhost",
        port: int = 3000,
        mgmt_port: int | None = None,
        oai_port: int = 3003,
    ):
        """TakeoffClient is used to interact with the Takeoff server.

        Args:
            base_url (str, optional): base url that takeoff server runs on. Defaults to "http://localhost".
            port (int, optional): port that main server runs on. Defaults to 8000.
            mgmt_port (int, optional): port that management api runs on. Usually be `port + 1`. Defaults to None.
        """
        self.base_url = base_url
        self.port = port
        self.oai_port = oai_port

        if mgmt_port is None:
            self.mgmt_port = port + 1
        else:
            self.mgmt_port = mgmt_port

        self.url = f"{self.base_url}:{self.port}"  # "http://localhost:3000"
        self.oai_url = f"{self.base_url}:{self.oai_port}"  # "http://localhost:3000"
        self.mgmt_url = f"{self.base_url}:{self.mgmt_port}"  # "http://localhost:3001"

    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    #                                                    Utils                                                         #
    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    def _sync_request(self, network_func, endpoint, **kwargs):
        try:
            response = network_func(endpoint, timeout=REQUEST_TIMEOUT, **kwargs)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise TakeoffException(
                status_code=500,
                message=f"Error issuing request\nError: {str(e)}",
            ) from e
        except httpx.HTTPStatusError as e:
            raise TakeoffException(
                status_code=e.response.status_code,
                message=f"Request failed\nStatus code: {str(e.response.status_code)}\nResponse: {e.response.text}",
            ) from e

        return response

    def _sync_post(self, endpoint, **kwargs):
        response = self._sync_request(httpx.post, endpoint, **kwargs)
        return response.json()

    def _sync_get(self, endpoint, **kwargs):
        response = self._sync_request(httpx.get, endpoint, **kwargs)
        return response.json()

    def _sync_delete(self, endpoint, **kwargs):
        self._sync_request(httpx.delete, endpoint, **kwargs)

    async def _async_request(self, network_func, endpoint, **kwargs):
        try:
            response = await network_func(endpoint, timeout=REQUEST_TIMEOUT, **kwargs)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise TakeoffException(
                status_code=500,
                message=f"Error issuing request\nError: {str(e)}",
            ) from e
        except httpx.HTTPStatusError as e:
            raise TakeoffException(
                status_code=e.response.status_code,
                message=f"Request failed\nStatus code: {str(e.response.status_code)}\nResponse: {e.response.text}",
            ) from e

        return response

    async def _async_post(self, endpoint, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await self._async_request(client.post, endpoint, **kwargs)
            return response.json()

    async def _async_get(self, endpoint, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await self._async_request(client.get, endpoint, **kwargs)
            return response.json()

    async def _async_delete(self, endpoint, **kwargs):
        async with httpx.AsyncClient() as client:
            await self._async_request(client.delete, endpoint, **kwargs)

    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    #                                                    Generation                                                    #
    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    def _generate_preprocess(self, json_data, image_path, stream=False) -> dict:
        if image_path is not None:
            if isinstance(image_path, Path):
                image_path = str(image_path)

            files = {
                "image_data": (image_path, open(image_path, "rb"), "image/*"),
                "json_data": (None, json.dumps(json_data), "application/json"),
            }
            endpoint = self.url + "/image_generate"
            kwargs = {"files": files}
        else:
            endpoint = self.url + "/generate"
            kwargs = {"json": json_data}

        if stream:
            endpoint += "_stream"

        return endpoint, kwargs

    def generate(
        self,
        text: Union[str, List[str]],
        sampling_temperature: Optional[float] = None,
        sampling_topp: Optional[float] = None,
        sampling_topk: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        no_repeat_ngram_size: Optional[int] = None,
        max_new_tokens: Optional[int] = None,
        min_new_tokens: Optional[int] = None,
        regex_string: Optional[str] = None,
        json_schema: Optional[Any] = None,
        constrained_decoding_backend: Optional[str] = None,
        return_metadata: Optional[bool] = None,
        prompt_max_tokens: Optional[int] = None,
        consumer_group: str = "primary",
        image_path: Union[str, Path, None] = None,
        lora_id: Optional[str] = None,
        use_chat_template: Optional[bool] = None,
    ) -> dict:
        """Buffered generation of text, seeking a completion for the input prompt. Buffers output and returns at once.

        Args:
            use_chat_template: Whether to apply the chat template provided in the model config, if available.
            return_metadata: Whether to return the metadata of the generated text, including token count.
            text (str): Input prompt from which to generate
            sampling_topp (float, optional): Sample from set of tokens whose cumulative probability exceeds this value
            sampling_temperature (float, optional): Sample predictions from the top K most probable candidates
            sampling_topk (int, optional): Sample with randomness. Bigger temperatures are associated with more randomness.
            repetition_penalty (float, optional): Penalise the generation of tokens that have been generated before. Set to > 1 to penalize.
            no_repeat_ngram_size (int, optional): Prevent repetitions of ngrams of this size.
            max_new_tokens (int, optional): The maximum number of (new) tokens that the model will generate.
            min_new_tokens (int, optional): The minimum number of (new) tokens that the model will generate.
            regex_string (str, optional): The regex string which generations will adhere to as they decode.
            json_schema (dict, optional): The JSON Schema which generations will adhere to as they decode. Ignored if regex_str is set.
            constrained_decoding_backend (str, optional): Which of "lmfe" or "outlines" to use for json decoding. Uses server set default if not specified.
            prompt_max_tokens (int, optional): The maximum length (in tokens) for this prompt. Prompts longer than this value will be truncated.
            consumer_group (str, optional): The consumer group to which to send the request.
            image_path (Path, optional): Path to the image file to be used as input. Defaults to None.
                                         Note: This is only available if the running model supports image to text generation, for
                                         example with LlaVa models.
            lora_id (str, optional): The name of the lora module to use. Defaults to None.

        Returns:
            Output (dict): The response from Takeoff containing the generated text as a whole.

        """
        json_data = {
            "text": text,
            "sampling_temperature": sampling_temperature,
            "sampling_topp": sampling_topp,
            "sampling_topk": sampling_topk,
            "repetition_penalty": repetition_penalty,
            "no_repeat_ngram_size": no_repeat_ngram_size,
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": min_new_tokens,
            "regex_string": regex_string,
            "json_schema": json_schema,
            "constrained_decoding_backend": constrained_decoding_backend,
            "return_metadata": return_metadata,
            "prompt_max_tokens": prompt_max_tokens,
            "consumer_group": consumer_group,
        }
        if use_chat_template is not None:
            json_data["use_chat_template"] = use_chat_template
        if lora_id is not None:
            json_data["lora_id"] = lora_id

        endpoint, kwargs = self._generate_preprocess(json_data, image_path)
        return self._sync_post(endpoint, **kwargs)

    async def generate_async(
        self,
        text: Union[str, List[str]],
        sampling_temperature: Optional[float] = None,
        sampling_topp: Optional[float] = None,
        sampling_topk: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        no_repeat_ngram_size: Optional[int] = None,
        max_new_tokens: Optional[int] = None,
        min_new_tokens: Optional[int] = None,
        regex_string: Optional[str] = None,
        json_schema: Optional[Any] = None,
        constrained_decoding_backend: Optional[str] = None,
        return_metadata: Optional[bool] = None,
        prompt_max_tokens: Optional[int] = None,
        consumer_group: str = "primary",
        image_path: Union[str, Path, None] = None,
        use_chat_template: Optional[bool] = None,
        lora_id: Optional[str] = None,
    ) -> dict:
        """Asynchronous generation of text, seeking a completion for the input prompt. Buffers output and returns at once.

        Args:
            use_chat_template: Whether to apply the chat template provided in the model config, if available.
            return_metadata: Whether to return the metadata of the generated text, including token count.
            text (str): Input prompt from which to generate
            sampling_topp (float, optional): Sample from set of tokens whose cumulative probability exceeds this value
            sampling_temperature (float, optional): Sample predictions from the top K most probable candidates
            sampling_topk (int, optional): Sample with randomness. Bigger temperatures are associated with more randomness.
            repetition_penalty (float, optional): Penalise the generation of tokens that have been generated before. Set to > 1 to penalize.
            no_repeat_ngram_size (int, optional): Prevent repetitions of ngrams of this size.
            max_new_tokens (int, optional): The maximum number of (new) tokens that the model will generate.
            min_new_tokens (int, optional): The minimum number of (new) tokens that the model will generate.
            regex_string (str, optional): The regex string which generations will adhere to as they decode.
            json_schema (dict, optional): The JSON Schema which generations will adhere to as they decode. Ignored if regex_str is set.
            constrained_decoding_backend (str, optional): Which of "lmfe" or "outlines" to use for json decoding. Uses server set default if not specified.
            prompt_max_tokens (int, optional): The maximum length (in tokens) for this prompt. Prompts longer than this value will be truncated.
            consumer_group (str, optional): The consumer group to which to send the request.
            image_path (Path, optional): Path to the image file to be used as input. Defaults to None.
                                         Note: This is only available if the running model supports image to text generation, for
                                         example with LlaVa models.
            lora_id (str, optional): The name of the lora module to use. Defaults to None.

        Returns:
            Output (dict): The response from Takeoff containing the generated text as a whole.

        """
        json_data = {
            "text": text,
            "sampling_temperature": sampling_temperature,
            "sampling_topp": sampling_topp,
            "sampling_topk": sampling_topk,
            "repetition_penalty": repetition_penalty,
            "no_repeat_ngram_size": no_repeat_ngram_size,
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": min_new_tokens,
            "regex_string": regex_string,
            "json_schema": json_schema,
            "constrained_decoding_backend": constrained_decoding_backend,
            "return_metadata": return_metadata,
            "prompt_max_tokens": prompt_max_tokens,
            "consumer_group": consumer_group,
        }
        if use_chat_template is not None:
            json_data["use_chat_template"] = use_chat_template
        if lora_id is not None:
            json_data["lora_id"] = lora_id

        endpoint, kwargs = self._generate_preprocess(json_data, image_path)
        return await self._async_post(endpoint, **kwargs)

    def generate_stream(
        self,
        text: Union[str, List[str]],
        sampling_temperature: Optional[float] = None,
        sampling_topp: Optional[float] = None,
        sampling_topk: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        no_repeat_ngram_size: Optional[int] = None,
        max_new_tokens: Optional[int] = None,
        min_new_tokens: Optional[int] = None,
        regex_string: Optional[str] = None,
        json_schema: Optional[Any] = None,
        constrained_decoding_backend: Optional[str] = None,
        return_metadata: Optional[bool] = None,
        prompt_max_tokens: Optional[int] = None,
        consumer_group: str = "primary",
        image_path: Union[str, Path, None] = None,
        lora_id: Optional[str] = None,
        use_chat_template: Optional[bool] = None,
    ) -> Iterator[Event]:
        """Generates text, seeking a completion for the input prompt.

        Args:
            use_chat_template: Whether to apply the chat template provided in the model config, if available.
            return_metadata: Whether to return the metadata of the generated text, including token count, in the last SSE.
            text (Union[str, List[str]]): Input prompt from which to generate
            sampling_temperature (float, optional): Sample predictions from the top K most probable candidates
            sampling_topp (float, optional): Sample from set of tokens whose cumulative probability exceeds this value
            sampling_topk (int, optional): Sample with randomness. Bigger temperatures are associated with more randomness.
            repetition_penalty (float, optional): Penalise the generation of tokens that have been generated before. Set to > 1 to penalize.
            no_repeat_ngram_size (int, optional): Prevent repetitions of ngrams of this size.
            max_new_tokens (int, optional): The maximum number of (new) tokens that the model will generate.
            min_new_tokens (int, optional): The minimum number of (new) tokens that the model will generate.
            regex_string (str, optional): The regex string which generations will adhere to as they decode.
            json_schema (dict, optional): The JSON Schema which generations will adhere to as they decode. Ignored if regex_str is set.
            constrained_decoding_backend (str, optional): Which of "lmfe" or "outlines" to use for json decoding. Uses server set default if not specified.
            prompt_max_tokens (int, optional): The maximum length (in tokens) for this prompt. Prompts longer than this value will be truncated.
            consumer_group (str, optional): The consumer group to which to send the request.
            image_path (Path, optional): Path to the image file to be used as input. Defaults to None.
                                         Note: This is only available if the running model supports image to text generation, for
                                         example with LlaVa models.
            lora_id (str, optional): The name of the lora module to use. Defaults to None.

        Returns:
            Iterator[sseclient._.Event]: An iterat_or of server-sent events.

        """
        json_data = {
            "text": text,
            "sampling_temperature": sampling_temperature,
            "sampling_topp": sampling_topp,
            "sampling_topk": sampling_topk,
            "repetition_penalty": repetition_penalty,
            "no_repeat_ngram_size": no_repeat_ngram_size,
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": min_new_tokens,
            "regex_string": regex_string,
            "json_schema": json_schema,
            "constrained_decoding_backend": constrained_decoding_backend,
            "return_metadata": return_metadata,
            "prompt_max_tokens": prompt_max_tokens,
            "consumer_group": consumer_group,
        }
        if use_chat_template is not None:
            json_data["use_chat_template"] = use_chat_template
        if lora_id is not None:
            json_data["lora_id"] = lora_id

        endpoint, kwargs = self._generate_preprocess(json_data, image_path, stream=True)
        try:
            with httpx.stream("POST", endpoint, timeout=REQUEST_TIMEOUT, **kwargs) as response:
                try:
                    response.raise_for_status()

                    for event in SSEClient(response.iter_bytes()).events():
                        yield event

                except httpx.HTTPStatusError as e:
                    e.response.read()
                    raise TakeoffException(
                        status_code=response.status_code,
                        message=f"Generation failed\nStatus code: {str(e.response.status_code)}\nResponse: {e.response.text}",
                    ) from e

        except httpx.RequestError as e:
            raise TakeoffException(
                status_code=None,
                message=f"Error issuing request\nError: {str(e)}",
            ) from e

    async def generate_stream_async(
        self,
        text: Union[str, List[str]],
        sampling_temperature: Optional[float] = None,
        sampling_topp: Optional[float] = None,
        sampling_topk: Optional[int] = None,
        repetition_penalty: Optional[float] = None,
        no_repeat_ngram_size: Optional[int] = None,
        max_new_tokens: Optional[int] = None,
        min_new_tokens: Optional[int] = None,
        regex_string: Optional[str] = None,
        json_schema: Optional[Any] = None,
        constrained_decoding_backend: Optional[str] = None,
        return_metadata: Optional[bool] = None,
        prompt_max_tokens: Optional[int] = None,
        consumer_group: str = "primary",
        image_path: Union[str, Path, None] = None,
        lora_id: Optional[str] = None,
        use_chat_template: Optional[bool] = None,
    ) -> AsyncIterator[Event]:
        """Asynchronously Generates text, seeking a completion for the input prompt.

        Args:
            use_chat_template: Whether to apply the chat template provided in the model config, if available.
            return_metadata: Whether to return the metadata of the generated text, including token count, in the last SSE.
            text (Union[str, List[str]]): Input prompt from which to generate
            sampling_temperature (float, optional): Sample predictions from the top K most probable candidates
            sampling_topp (float, optional): Sample from set of tokens whose cumulative probability exceeds this value
            sampling_topk (int, optional): Sample with randomness. Bigger temperatures are associated with more randomness.
            repetition_penalty (float, optional): Penalise the generation of tokens that have been generated before. Set to > 1 to penalize.
            no_repeat_ngram_size (int, optional): Prevent repetitions of ngrams of this size.
            max_new_tokens (int, optional): The maximum number of (new) tokens that the model will generate.
            min_new_tokens (int, optional): The minimum number of (new) tokens that the model will generate.
            regex_string (str, optional): The regex string which generations will adhere to as they decode.
            json_schema (dict, optional): The JSON Schema which generations will adhere to as they decode. Ignored if regex_str is set.
            constrained_decoding_backend (str, optional): Which of "lmfe" or "outlines" to use for json decoding. Uses server set default if not specified.
            prompt_max_tokens (int, optional): The maximum length (in tokens) for this prompt. Prompts longer than this value will be truncated.
            consumer_group (str, optional): The consumer group to which to send the request.
            image_path (Path, optional): Path to the image file to be used as input. Defaults to None.
                                         Note: This is only available if the running model supports image to text generation, for
                                         example with LlaVa models.
            lora_id (str, optional): The name of the lora module to use. Defaults to None.

        Returns:
            AsyncIterator[sseclient.SSEClient.Event]: An asynchronous iterator of server-sent events.

        """
        json_data = {
            "text": text,
            "sampling_temperature": sampling_temperature,
            "sampling_topp": sampling_topp,
            "sampling_topk": sampling_topk,
            "repetition_penalty": repetition_penalty,
            "no_repeat_ngram_size": no_repeat_ngram_size,
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": min_new_tokens,
            "regex_string": regex_string,
            "json_schema": json_schema,
            "constrained_decoding_backend": constrained_decoding_backend,
            "return_metadata": return_metadata,
            "prompt_max_tokens": prompt_max_tokens,
            "consumer_group": consumer_group,
        }
        if use_chat_template is not None:
            json_data["use_chat_template"] = use_chat_template
        if lora_id is not None:
            json_data["lora_id"] = lora_id

        endpoint, kwargs = self._generate_preprocess(json_data, image_path, stream=True)

        client = httpx.AsyncClient()

        try:
            async with client.stream("POST", endpoint, timeout=REQUEST_TIMEOUT, **kwargs) as response:
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    await e.response.aread()
                    raise TakeoffException(
                        status_code=e.response.status_code,
                        message=f"Generation failed\nStatus code: {str(e.response.status_code)}\nResponse: {e.response.text}",
                    ) from e

                async for event in SSEClientAsync(response.aiter_bytes()).events():
                    yield event

        except httpx.RequestError as e:
            raise TakeoffException(
                status_code=500,
                message=f"Error issuing request\nError: {str(e)}",
            ) from e

    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    #                                          Document processing                                                     #
    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

    def partition_document(
        self,
        document_path: Union[str, Path],
        consumer_group: str = "primary",
    ) -> dict:
        """Buffered generation of text, seeking a completion for the input prompt. Buffers output and returns at once.

        Args:
            document_path (Path | str): Path to the pdf file to be used as input.
            consumer_group (str, optional): The consumer group to which to send the request.

        Returns:
            Output (dict): The response from Takeoff containing the generated text as a whole.

        """
        json_data = {
            "consumer_group": consumer_group,
        }

        if isinstance(document_path, Path):
            document_path = str(document_path)

        kwargs = {
            "files": {
                "image_data": (document_path, open(document_path, "rb"), "image/*"),
                "json_data": (None, json.dumps(json_data), "application/json"),
            }
        }
        endpoint = self.url + "/partition_document"

        return self._sync_post(endpoint, **kwargs)

    async def partition_document_async(
        self,
        document_path: Union[str, Path],
        consumer_group: str = "primary",
    ) -> dict:
        """Buffered generation of text, seeking a completion for the input prompt. Buffers output and returns at once.

        Args:
            document_path (Path | str): Path to the pdf file to be used as input.
            consumer_group (str, optional): The consumer group to which to send the request.

        Returns:
            Output (dict): The response from Takeoff containing the generated text as a whole.

        """
        json_data = {
            "consumer_group": consumer_group,
        }

        if isinstance(document_path, Path):
            document_path = str(document_path)

        kwargs = {
            "files": {
                "image_data": (document_path, open(document_path, "rb"), "image/*"),
                "json_data": (None, json.dumps(json_data), "application/json"),
            }
        }
        endpoint = self.url + "/partition_document"

        return await self._async_post(endpoint, **kwargs)

    def partition_document_stream(
        self,
        document_path: Union[str, Path],
        consumer_group: str = "primary",
    ) -> Iterator[Event]:
        """Generates text, seeking a completion for the input prompt.

        Args:
            document_path (Path | str): Path to the pdf file to be used as input.
            consumer_group (str, optional): The consumer group to which to send the request.

        Returns:
            Iterator[sseclient._.Event]: An iterat_or of server-sent events.

        """
        json_data = {
            "consumer_group": consumer_group,
        }

        if isinstance(document_path, Path):
            document_path = str(document_path)

        kwargs = {
            "files": {
                "image_data": (document_path, open(document_path, "rb"), "image/*"),
                "json_data": (None, json.dumps(json_data), "application/json"),
            }
        }
        endpoint = self.url + "/partition_document_stream"
        try:
            with httpx.stream("POST", endpoint, timeout=REQUEST_TIMEOUT, **kwargs) as response:
                try:
                    response.raise_for_status()

                    for event in SSEClient(response.iter_bytes()).events():
                        yield event

                except httpx.HTTPStatusError as e:
                    e.response.read()
                    raise TakeoffException(
                        status_code=response.status_code,
                        message=f"Generation failed\nStatus code: {str(e.response.status_code)}\nResponse: {e.response.text}",
                    ) from e

        except httpx.RequestError as e:
            raise TakeoffException(
                status_code=None,
                message=f"Error issuing request\nError: {str(e)}",
            ) from e

    async def partition_document_stream_async(
        self,
        document_path: Union[str, Path],
        consumer_group: str = "primary",
    ) -> AsyncIterator[Event]:
        """Generates text, seeking a completion for the input prompt.

        Args:
            document_path (Path | str): Path to the pdf file to be used as input.
            consumer_group (str, optional): The consumer group to which to send the request.

        Returns:
            Iterator[sseclient._.Event]: An iterat_or of server-sent events.

        """
        json_data = {
            "consumer_group": consumer_group,
        }

        if isinstance(document_path, Path):
            document_path = str(document_path)

        kwargs = {
            "files": {
                "image_data": (document_path, open(document_path, "rb"), "image/*"),
                "json_data": (None, json.dumps(json_data), "application/json"),
            }
        }
        endpoint = self.url + "/partition_document_stream"

        client = httpx.AsyncClient()

        try:
            async with client.stream("POST", endpoint, timeout=REQUEST_TIMEOUT, **kwargs) as response:
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    await e.response.aread()
                    raise TakeoffException(
                        status_code=e.response.status_code,
                        message=f"Generation failed\nStatus code: {str(e.response.status_code)}\nResponse: {e.response.text}",
                    ) from e

                async for event in SSEClientAsync(response.aiter_bytes()).events():
                    yield event

        except httpx.RequestError as e:
            raise TakeoffException(
                status_code=500,
                message=f"Error issuing request\nError: {str(e)}",
            ) from e

    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    #                                                    Embedding                                                     #
    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    def embed(self, text: Union[str, List[str]], consumer_group: str = "primary") -> dict:
        """Embed a batch of text.

        Args:
            text (Union[str, List[str]]): Text to embed.
            consumer_group (str, optional): consumer group to use. Defaults to "primary".

        Returns:
            dict: Embedding response.
        """
        return self._sync_post(self.oai_url + "/v1/embeddings", json={"input": text, "model": consumer_group})

    async def embed_async(self, text: Union[str, List[str]], consumer_group: str = "primary") -> dict:
        """Asynchronous embedding of text.

        Args:
            text (Union[str, List[str]]): Text to embed.
            consumer_group (str, optional): consumer group to use. Defaults to "primary".

        Returns:
            dict: Embedding response.
        """
        return await self._async_post(self.oai_url + "/v1/embeddings", json={"input": text, "model": consumer_group})

    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    #                                                 Classification                                                   #
    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    def classify(
        self,
        text: Union[str, List[str], List[List[str]]],
        consumer_group: str = "classify",
    ) -> dict:
        """Classify a batch of text.

        Text that is passed in as a list of list of strings will be concatenated on the
        innermost list, and the outermost list treated as a batch of concatenated strings.

        Concatenation happens server-side, as it needs information from the model tokenizer.

        Args:
            text (Union[str, List[str], List[List[str]]]): Text to classify.
            consumer_group (str, optional): consumer group to use. Defaults to "classify".

        Returns:
            dict: Classification response.
        """
        return self._sync_post(
            self.url + "/classify",
            json={"text": text, "consumer_group": consumer_group},
        )

    async def classify_async(
        self,
        text: Union[str, List[str], List[List[str]]],
        consumer_group: str = "classify",
    ) -> dict:
        """Asynchronous classification of text.

        Text that is passed in as a list of list of strings will be concatenated on the
        innermost list, and the outermost list treated as a batch of concatenated strings.

        Concatenation happens server-side, as it needs information from the model tokenizer.

        Args:
            text (Union[str, List[str]], List[List[str]]): Text to classify.
            consumer_group (str, optional): consumer group to use. Defaults to "classify".

        Returns:
            dict: Classification response.
        """
        return await self._async_post(
            self.url + "/classify",
            json={"text": text, "consumer_group": consumer_group},
        )

    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    #                                                    Tokenize                                                      #
    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    def tokens_count(self, text: str, reader_id: str) -> int:
        """Get the number of tokens in a single text item.

        Args:
            text (str): Text to tokenize.
            reader_id (str): The id of the reader to use.

        Returns:
            int: Number of tokens.
        """
        response = self._sync_post(self.url + f"/tokenize/{reader_id}", json={"text": text})

        if "tokens_count" not in response:
            raise TakeoffException("Tokenization failed\nResponse: " + response)
        else:
            return response["tokens_count"]

    async def tokens_count_async(self, text: str, reader_id: str) -> int:
        """Asynchronously get the number of tokens in a single text item.

        Args:
            text (str): Text to tokenize.
            reader_id (str): The id of the reader to use.

        Returns:
            int: Number of tokens.
        """
        response = await self._async_post(self.url + f"/tokenize/{reader_id}", json={"text": text})
        if "tokens_count" not in response:
            raise TakeoffException("Tokenization failed\nResponse: " + response)
        else:
            return response["tokens_count"]

    def tokenize(self, text: str, reader_id: str, use_chat_template: bool = True) -> List[str]:
        """Tokenize a single text item.

        The tokenize endpoint can be used to send a string to a models tokenizer for tokenization.
        The result is a list of tokens. For example, if "my_reader" is the id of a model that uses a Llama tokenizer,
        The following code will tokenize the string "hello, world" using the Llama tokenizer:

        >>> takeoff_client.tokenize(
        ...     "hello, world",
        ...     reader_id="my_reader",
        ... )
        ... [
        ...     "▁hello",
        ...     ",",
        ...     "▁world",
        ... ]

        NOTE: The `reader_id` parameter is not the same as the `consumer_group` parameter used in other endpoints.
        Because tokenization is specific to a specific loaded model, we need to specify a unique id that identifies
        a particular reader. To find this ID for the models currently loaded into your takeoff server, try the following

        >>> readers = takeoff_client.get_readers()
        >>> for reader_group in readers.values():
        >>>    for reader in reader_group:
        >>>       print(reader["reader_id"])

        Args:
            text (str): Text to tokenize.
            reader_id (str): The id of the reader to use.

        Returns:
            List[str]: Tokenized text.
        """
        response = self._sync_post(
            self.url + f"/tokenize/{reader_id}",
            json={"text": text, "use_chat_template": use_chat_template},
        )

        if "tokens" not in response:
            raise TakeoffException("Tokenization failed\nResponse: " + response)
        else:
            return response["tokens"]

    async def tokenize_async(self, text: str, reader_id: str, use_chat_template: bool = True) -> List[str]:
        """Asynchronous tokenization of text.

        The tokenize endpoint can be used to send a string to a models tokenizer for tokenization.
        The result is a list of tokens. For example, if "my_reader" is the id of a model that uses a Llama tokenizer,
        The following code will tokenize the string "hello, world" using the Llama tokenizer:

        >>> takeoff_client.tokenize(
        ...     "hello, world",
        ...     reader_id="my_reader",
        ... )
        ... [
        ...     "▁hello",
        ...     ",",
        ...     "▁world",
        ... ]

        NOTE: The `reader_id` parameter is not the same as the `consumer_group` parameter used in other endpoints.
        Because tokenization is specific to a specific loaded model, we need to specify a unique id that identifies
        a particular reader. To find this ID for the models currently loaded into your takeoff server, try the following

        >>> readers = takeoff_client.get_readers()
        >>> for reader_group in readers.values():
        >>>    for reader in reader_group:
        >>>       print(reader["reader_id"])

        Args:
            text (str): Text to tokenize.
            reader_id (str): The id of the reader to use.

        Returns:
            list[str]: Tokenized text.
        """
        response = await self._async_post(
            self.url + f"/tokenize/{reader_id}",
            json={"text": text, "use_chat_template": use_chat_template},
        )
        if "tokens" not in response:
            raise TakeoffException("Tokenization failed\nResponse: " + response, kwargs={})
        else:
            return response["tokens"]

    def detokenize(
        self,
        tokens: Union[list[str], list[int]],
        reader_id: str,
        skip_special_tokens: bool = True,
    ) -> str:
        """Detokenizes a list of tokens (as strings) or token ids.

        The detokenize endpoint can be used to send a list of tokens to a models tokenizer for detokenization/decoding.
        The result is an output string. For example, if "my_reader" is the id of a model that uses a Llama tokenizer,
        The following code will tokenize the string "hello, world" using the Llama tokenizer:

        >>> takeoff_client.detokenize(
        ...     ['▁Fish', '▁is', '▁very', '▁nut', 'rit', 'ious', '.']
        ...     reader_id="my_reader",
        ... )
        ... "Fish is very nutritious."

        >>> takeoff_client.detokenize(
        ...     [1, 12030, 338, 1407, 18254, 768, 2738, 29889]
        ...     reader_id="my_reader",
        ...     skip_special_tokens=False,
        ... )
        ... "<s> Fish is very nutritious."
        NOTE: The `reader_id` parameter is not the same as the `consumer_group` parameter used in other endpoints.
        Because (de)tokenization is specific to a specific loaded model, we need to specify a unique id that identifies
        a particular reader. To find this ID for the models currently loaded into your takeoff server, try the following

        >>> readers = takeoff_client.get_readers()
        >>> for reader_group in readers.values():
        >>>    for reader in reader_group:
        >>>       print(reader["reader_id"])

        Args:
            tokens (List[str] or List[int]): Tokens/token ids to detokenize/decode. If providing token ids, special tokens can optionally be included.
            reader_id (str): The id of the reader to use.
            skip_special_tokens (bool): Whether to include special tokens in the decoded output.

        Returns:
            List[str]: Tokenized text.
        """
        response = self._sync_post(
            self.url + f"/detokenize/{reader_id}",
            json={"tokens": tokens, "skip_special_tokens": skip_special_tokens},
        )

        if "text" not in response:
            raise TakeoffException("Detokenization failed\nResponse: " + str(response))
        else:
            return response["text"]

    async def detokenize_async(
        self,
        tokens: Union[list[str], list[int]],
        reader_id: str,
        skip_special_tokens: bool = True,
    ) -> str:
        """Asynchronously detokenizes a list of tokens (as strings) or token ids.

        The detokenize endpoint can be used to send a list of tokens to a models tokenizer for detokenization/decoding.
        The result is an output string. For example, if "my_reader" is the id of a model that uses a Llama tokenizer,
        The following code will tokenize the string "hello, world" using the Llama tokenizer:

        >>> takeoff_client.detokenize(
        ...     ['▁Fish', '▁is', '▁very', '▁nut', 'rit', 'ious', '.']
        ...     reader_id="my_reader",
        ... )
        ... "Fish is very nutritious."

        >>> takeoff_client.detokenize(
        ...     [1, 12030, 338, 1407, 18254, 768, 2738, 29889]
        ...     reader_id="my_reader",
        ...     skip_special_tokens=False,
        ... )
        ... "<s> Fish is very nutritious."
        NOTE: The `reader_id` parameter is not the same as the `consumer_group` parameter used in other endpoints.
        Because (de)tokenization is specific to a specific loaded model, we need to specify a unique id that identifies
        a particular reader. To find this ID for the models currently loaded into your takeoff server, try the following

        >>> readers = takeoff_client.get_readers()
        >>> for reader_group in readers.values():
        >>>    for reader in reader_group:
        >>>       print(reader["reader_id"])

        Args:
            tokens (List[str] or List[int]): Tokens/token ids to detokenize/decode. If providing token ids, special tokens can optionally be included.
            reader_id (str): The id of the reader to use.
            skip_special_tokens (bool): Whether to include special tokens in the decoded output.

        Returns:
            List[str]: Tokenized text.
        """
        response = await self._async_post(
            self.url + f"/detokenize/{reader_id}",
            json={"tokens": tokens, "skip_special_tokens": skip_special_tokens},
        )
        if "text" not in response:
            raise TakeoffException("Detokenization failed\nResponse: " + str(response), kwargs={})
        else:
            return response["text"]

    def chat_template(
        self,
        input: Union[List[ChatTemplateMessage], ChatTemplateMessage],
        reader_id: str,
        add_generation_prompt: bool = False,
    ) -> List[str]:
        """The chat template endpoint can be used to automatically find the chat template best for interacting with a model.
        The result is a list of strings which is a series of messages formatted in a chat template.

        A chat template message is a list of role->message pairs. For example, the following is a chat template message:
        [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, how about you?"}
        ]

        This might be returned to the user like this (the exact template is dependent on the model):

        "<s>[INST] Hello, how are you? [/INST]I'm doing well, how about you?</s>"

        You can pass in a message like that, or a batch of messages. The response will be a list of strings, each string
        representing a series of messages in the chat template.

        If you set add_generation_prompt to True, then the generated template will return with an empty last message,
        ready for the model to respond. This won't affect all model templates. If it doesn't then a warning will be
        returned in the takeoff logs, but the template will still be returned unaffected.

        Args:
            input (Union[List[ChatTemplateMessage], ChatTemplateMessage]): A list of messages to send to the model.
            add_generation_prompt (bool): Whether to add a generation prompt to the end of the chat template.
            reader_id (str): The id of the reader to use.

        Returns:
            List[str]: List of responses from the model in the chat template.
        """
        # raise an exception if the input is empty
        if not input:
            raise TakeoffException(status_code=400, message="Chat template failed\nError: Input is empty")

        if isinstance(input[0], dict):
            input = [input]

        response = self._sync_post(
            self.url + f"/chat_template/{reader_id}",
            json={"inputs": input, "add_generation_prompt": add_generation_prompt},
        )

        if "messages" not in response:
            raise TakeoffException(status_code=500, message="Chat template failed\nResponse: " + response)
        else:
            return response["messages"]

    async def chat_template_async(
        self,
        input: Union[List[ChatTemplateMessage], ChatTemplateMessage],
        reader_id: str,
        add_generation_prompt: bool = False,
    ) -> List[str]:
        """Asynchronous version of the chat_template function.

        The chat template endpoint can be used to automatically find the chat template best for interacting with a model.
        The result is a list of strings which is a series of messages formatted in a chat template.

        A chat template message is a list of role->message pairs. For example, the following is a chat template message:
        [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, how about you?"}
        ]

        This might be returned to the user like this (the exact template is dependent on the model):

        "<s>[INST] Hello, how are you? [/INST]I'm doing well, how about you?</s>"

        You can pass in a message like that, or a batch of messages. The response will be a list of strings, each string
        representing a series of messages in the chat template.

        If you set add_generation_prompt to True, then the generated template will return with an empty last message,
        ready for the model to respond. This won't affect all model templates. If it doesn't then a warning will be
        returned in the takeoff logs, but the template will still be returned unaffected.

        Args:
            input (Union[List[ChatTemplateMessage], ChatTemplateMessage]): A list of messages to send to the model.
            add_generation_prompt (bool): Whether to add a generation prompt to the end of the chat template.
            reader_id (str): The id of the reader to use.

        Returns:
            List[str]: List of responses from the model in the chat template.
        """
        if isinstance(input[0], dict):
            input = [input]

        response = await self._async_post(
            self.url + f"/chat_template/{reader_id}",
            json={"inputs": input, "add_generation_prompt": add_generation_prompt},
        )

        if "messages" not in response:
            raise TakeoffException("Chat template failed\nResponse: " + response)
        else:
            return response["messages"]

    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    #                                                    Management                                                    #
    # ──────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
    def get_readers(self) -> dict:
        """Get a list of information about all readers.

        Returns:
            dict: List of information about all readers.
        """
        return self._sync_get(self.mgmt_url + "/reader_groups")

    async def get_readers_async(self) -> dict:
        """Asynchronously get a list of information about all readers.

        Returns:
            dict: List of information about all readers.
        """
        return await self._async_get(self.mgmt_url + "/reader_groups")

    def create_reader(self, reader_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new reader.

        Args:
            reader_config (Dict[str, Any]): Dict containing all the reader configuration parameters.
        """
        try:
            reader = ReaderConfig(**reader_config)
        except Exception as e:
            raise TakeoffException(400, f"Reader creation failed\nError: {str(e)}") from e

        return self._sync_post(self.mgmt_url + "/reader", json=reader.dict_without_optionals())

    async def create_reader_async(self, reader_config: Dict[str, Any]) -> Dict[str, Any]:
        """Asynchronously create a new reader.

        Args:
            reader_config (Dict[str, Any]): Dict containing all the reader configuration parameters.
        """
        try:
            reader = ReaderConfig(**reader_config)
        except Exception as e:
            raise TakeoffException(400, f"Reader creation failed\nError: {str(e)}") from e

        return await self._async_post(self.mgmt_url + "/reader", json=reader.dict_without_optionals())

    def delete_reader(self, reader_id: str) -> None:
        """Delete a reader, using their reader_id.

        Args:
            reader_id (str): Reader id.
        """
        return self._sync_delete(self.mgmt_url + f"/reader/{reader_id}")

    async def delete_reader_async(self, reader_id: str) -> None:
        """Asynchronously delete a reader, using their reader_id.

        Args:
            reader_id (str): Reader id.
        """
        return await self._async_delete(self.mgmt_url + f"/reader/{reader_id}")

    def list_all_readers(self) -> Dict[str, Dict[str, Any]]:
        """List all readers, ordering by consumer group.

        Returns:
            Dict[str, Dict[str, Any]]: List of reader ids.
        """
        return self._sync_get(self.mgmt_url + "/reader_groups")

    async def list_all_readers_async(self) -> Dict[str, Dict[str, Any]]:
        """Asynchronously list all readers, ordering by consumer group.

        Returns:
            Dict[str, Dict[str, Any]]: List of reader ids.
        """
        return await self._async_get(self.mgmt_url + "/reader_groups")

    def get_reader_config(self, reader_id: str) -> Dict[str, Any]:
        """Get the config.json that a reader is running.

        Args:
            reader_id (str): Reader id.

        Returns:
            Dict[str, Any]: Reader configuration.
        """
        return self._sync_get(self.mgmt_url + f"/config/{reader_id}")

    async def get_reader_config_async(self, reader_id: str) -> Dict[str, Any]:
        """Asynchronously get the config.json that a reader is running.

        Args:
            reader_id (str): Reader id.

        Returns:
            Dict[str, Any]: Reader configuration.
        """
        return await self._async_get(self.mgmt_url + f"/config/{reader_id}")

    async def get_status_async(self) -> Dict[str, Any]:
        """Asynchronously get the status of Takeoff.

        Returns:
            Dict[str, Any]: takeoff server status.
        """
        return await self._async_get(self.mgmt_url + "/status")

    def get_status(self) -> Dict[str, Any]:
        """Get the status of a reader.

        Returns:
            Dict[str, Any]: takeoff server status.
        """
        return self._sync_get(self.mgmt_url + "/status")


if __name__ == "__main__":
    pass
