import os
from pathlib import Path

import httpx
import pytest
from pytest_httpx import HTTPXMock, IteratorStream
from takeoff_client import TakeoffClient
from takeoff_client.exceptions import TakeoffException


def test_initialization_default():
    client = TakeoffClient()
    assert client.base_url == "http://localhost"
    assert client.port == 3000
    assert client.mgmt_port == 3001
    assert client.url == "http://localhost:3000"
    assert client.mgmt_url == "http://localhost:3001"


def test_initialization_custom():
    # test that mgmt_port is set to port + 1
    client = TakeoffClient("http://test", 9000)
    assert client.base_url == "http://test"
    assert client.port == 9000
    assert client.mgmt_port == 9001
    assert client.url == "http://test:9000"
    assert client.mgmt_url == "http://test:9001"


def test_initalization_custom_mgmt_port():
    client = TakeoffClient("http://test", 9000, 9005)
    assert client.base_url == "http://test"
    assert client.port == 9000
    assert client.mgmt_port == 9005
    assert client.url == "http://test:9000"
    assert client.mgmt_url == "http://test:9005"


def test_sync_request_errors(httpx_mock: HTTPXMock):
    client = TakeoffClient()
    # Test that an Exception is raised when the status code is not 200
    httpx_mock.add_response(status_code=400, text="Error message")
    with pytest.raises(TakeoffException) as e:
        client._sync_post("http://localhost:3000")
    assert str(e.value) == "Request failed\nStatus code: 400\nResponse: Error message"
    assert e.type == TakeoffException

    # Test that a request to a non-existent server raises an exception
    httpx_mock.add_exception(httpx.ReadTimeout("Connection error message"))
    with pytest.raises(TakeoffException) as e:
        client._sync_post("http://localhost:3000")
    assert str(e.value) == "Error issuing request\nError: Connection error message"
    assert e.type == TakeoffException


@pytest.mark.asyncio
async def test_async_request_errors(httpx_mock: HTTPXMock):
    client = TakeoffClient()
    # Test that an Exception is raised when the status code is not 200
    httpx_mock.add_response(status_code=400, text="Error message")
    with pytest.raises(TakeoffException) as e:
        await client._async_post("http://localhost:3000")

    assert str(e.value) == "Request failed\nStatus code: 400\nResponse: Error message"
    assert e.type == TakeoffException

    # Test that a request to a non-existent server raises an exception
    httpx_mock.add_exception(httpx.ReadTimeout("Connection error message"))
    with pytest.raises(TakeoffException) as e:
        await client._async_post("http://localhost:3000")
    assert str(e.value) == "Error issuing request\nError: Connection error message"
    assert e.type == TakeoffException


def test_generate(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"text": "generated text"},
    )
    httpx_mock.add_response(
        json={"text": "generated text"},
    )

    client = TakeoffClient()

    # Test default params
    response = client.generate("text to generate")
    assert response == {"text": "generated text"}

    # Test custom params
    response = client.generate(
        "text to generate",
        sampling_temperature=0.5,
        sampling_topp=0.5,
        sampling_topk=5,
        repetition_penalty=1.5,
        no_repeat_ngram_size=2,
        max_new_tokens=100,
        min_new_tokens=10,
        regex_string="test",
        json_schema={"test": "test"},
        prompt_max_tokens=50,
    )
    assert response == {"text": "generated text"}

    # Test invalid field
    with pytest.raises(TypeError):
        client.generate("text to generate", invalid_field="test")


@pytest.fixture
def create_image():
    with open("image.png", "w") as f:
        f.write("test")

    yield

    os.remove("image.png")


def test_generate_w_image(httpx_mock: HTTPXMock, create_image):
    httpx_mock.add_response(
        json={"text": "generated text"},
    )
    httpx_mock.add_response(
        json={"text": "generated text"},
    )

    client = TakeoffClient()

    # Test string image path
    response = client.generate("text to generate", image_path="image.png")
    assert response == {"text": "generated text"}

    # Test Path image path
    img_path = Path("image.png")
    response = client.generate("text to generate", image_path=img_path)
    assert response == {"text": "generated text"}


@pytest.mark.asyncio
async def test_generate_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"text": "generated text"},
    )
    httpx_mock.add_response(
        json={"text": "generated text"},
    )

    client = TakeoffClient()

    # Test default params
    response = await client.generate_async("text to generate")
    assert response == {"text": "generated text"}

    # Test custom params
    response = await client.generate_async(
        "text to generate",
        sampling_temperature=0.5,
        sampling_topp=0.5,
        sampling_topk=5,
        repetition_penalty=1.5,
        no_repeat_ngram_size=2,
        max_new_tokens=100,
        min_new_tokens=10,
        regex_string="test",
        json_schema={"test": "test"},
        prompt_max_tokens=50,
    )
    assert response == {"text": "generated text"}

    # Test invalid field
    with pytest.raises(TypeError):
        await client.generate_async("text to generate", invalid_field="test")


@pytest.mark.asyncio
async def test_generate_async_w_image(httpx_mock: HTTPXMock, create_image):
    httpx_mock.add_response(
        json={"text": "generated text"},
    )
    httpx_mock.add_response(
        json={"text": "generated text"},
    )

    client = TakeoffClient()

    response = await client.generate_async("text to generate", image_path="image.png")

    assert response == {"text": "generated text"}

    img_path = Path("image.png")
    response = await client.generate_async("text to generate", image_path=img_path)
    assert response == {"text": "generated text"}


def test_generate_stream(httpx_mock: HTTPXMock):
    httpx_mock.add_response(stream=IteratorStream([b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]))

    client = TakeoffClient()

    result_generator = client.generate_stream("text to generate")
    result = list(result_generator)
    print(result)

    assert len(result) == 2
    assert result[0].data == "Generated text 1"
    assert result[1].data == "Generated text 2"

    # Test that an Exception is raised when the status code is not 200
    httpx_mock.add_response(status_code=400, text="Error message")
    with pytest.raises(TakeoffException) as e:
        list(client.generate_stream("text to generate"))
    assert str(e.value) == "Generation failed\nStatus code: 400\nResponse: Error message"
    assert e.type == TakeoffException

    # Test that a request to a non-existent server raises an exception
    httpx_mock.add_exception(httpx.ReadTimeout("Connection error message"))
    with pytest.raises(TakeoffException) as e:
        list(client.generate_stream("text to generate"))
    assert str(e.value) == "Error issuing request\nError: Connection error message"
    assert e.type == TakeoffException


def test_generate_stream_w_image(httpx_mock: HTTPXMock, create_image):
    httpx_mock.add_response(stream=IteratorStream([b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]))
    httpx_mock.add_response(stream=IteratorStream([b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]))

    client = TakeoffClient()

    result_generator = client.generate_stream("text to generate", image_path="image.png")
    result = list(result_generator)

    assert len(result) == 2
    assert result[0].data == "Generated text 1"
    assert result[1].data == "Generated text 2"

    img_path = Path("image.png")
    result_generator = client.generate_stream("text to generate", image_path=img_path)
    result = list(result_generator)

    assert len(result) == 2
    assert result[0].data == "Generated text 1"
    assert result[1].data == "Generated text 2"


@pytest.mark.asyncio
async def test_generate_stream_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(stream=IteratorStream([b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]))

    client = TakeoffClient()

    result_generator = client.generate_stream_async("text to generate")
    result = [item async for item in result_generator]
    print(result)

    assert len(result) == 2
    assert result[0].data == "Generated text 1"
    assert result[1].data == "Generated text 2"

    # Test that an Exception is raised when the status code is not 200
    httpx_mock.add_response(status_code=400, text="Error message")
    with pytest.raises(TakeoffException) as e:
        [item async for item in client.generate_stream_async("text to generate")]
    assert str(e.value) == "Generation failed\nStatus code: 400\nResponse: Error message"
    assert e.type == TakeoffException

    # Test that a request to a non-existent server raises an exception
    httpx_mock.add_exception(httpx.ReadTimeout("Connection error message"))
    with pytest.raises(TakeoffException) as e:
        [item async for item in client.generate_stream_async("text to generate")]
    assert str(e.value) == "Error issuing request\nError: Connection error message"
    assert e.type == TakeoffException


@pytest.mark.asyncio
async def test_generate_stream_async_w_image(httpx_mock: HTTPXMock, create_image):
    httpx_mock.add_response(stream=IteratorStream([b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]))
    httpx_mock.add_response(stream=IteratorStream([b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]))

    client = TakeoffClient()

    result_generator = client.generate_stream_async("text to generate", image_path="image.png")
    result = [item async for item in result_generator]

    assert len(result) == 2
    assert result[0].data == "Generated text 1"
    assert result[1].data == "Generated text 2"

    img_path = Path("image.png")
    result_generator = client.generate_stream_async("text to generate", image_path=img_path)
    result = [item async for item in result_generator]

    assert len(result) == 2
    assert result[0].data == "Generated text 1"
    assert result[1].data == "Generated text 2"


@pytest.fixture
def create_document(tmp_path):
    path = tmp_path / "image.pdf"
    with open(path, "w") as f:
        f.write("test")

    yield path

    os.remove(path)


def test_partition_document(httpx_mock: HTTPXMock, create_document: str):
    httpx_mock.add_response(
        json={"text": "generated text"},
    )

    client = TakeoffClient()

    # Test default params
    response = client.partition_document(create_document)
    assert response == {"text": "generated text"}

    # Test invalid field
    with pytest.raises(TypeError):
        client.generate(create_document, invalid_field="test")


@pytest.mark.asyncio
async def test_partition_document_async(httpx_mock: HTTPXMock, create_document: str):
    httpx_mock.add_response(
        json={"text": "generated text"},
    )

    client = TakeoffClient()

    # Test default params
    response = await client.partition_document_async(create_document)
    assert response == {
        "text": "generated text"
    }  # Responses don't actually look like this, but we're testing the inputs not the outputs

    # Test invalid field
    with pytest.raises(TypeError):
        client.generate(create_document, invalid_field="test")


def test_partition_document_stream(httpx_mock: HTTPXMock, create_document: str):
    httpx_mock.add_response(stream=IteratorStream([b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]))
    # results don't actually look like this, but we're testing the inputs not the outputs

    client = TakeoffClient()

    result_generator = client.partition_document_stream(document_path=create_document)
    result = list(result_generator)

    assert len(result) == 2
    assert result[0].data == "Generated text 1"
    assert result[1].data == "Generated text 2"


@pytest.mark.asyncio
async def test_partition_document_async_stream(httpx_mock: HTTPXMock, create_document: str):
    httpx_mock.add_response(stream=IteratorStream([b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]))
    # Again, responses don't look like this, but we're testing the inputs not the outputs

    client = TakeoffClient()

    result_generator = client.partition_document_stream_async(document_path=create_document)
    result = [item async for item in result_generator]

    assert len(result) == 2
    assert result[0].data == "Generated text 1"
    assert result[1].data == "Generated text 2"


def test_embed(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"result": [0, 1, 2, 3]},
    )

    client = TakeoffClient()

    response = client.embed("text to embed")
    assert response == {"result": [0, 1, 2, 3]}


@pytest.mark.asyncio
async def test_embed_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"result": [0, 1, 2, 3]},
    )

    client = TakeoffClient()

    response = await client.embed_async("text to embed")
    assert response == {"result": [0, 1, 2, 3]}


def test_get_readers(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={
            "primary": [
                {
                    "reader_id": "test",
                    "device": "test",
                    "model_name": "test",
                    "model_type": "test",
                    "pids": [0],
                    "ready": True,
                }
            ]
        },
    )

    client = TakeoffClient()

    response = client.get_readers()
    assert response == {
        "primary": [
            {
                "reader_id": "test",
                "device": "test",
                "model_name": "test",
                "model_type": "test",
                "pids": [0],
                "ready": True,
            }
        ]
    }


@pytest.mark.asyncio
async def test_get_readers_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={
            "primary": [
                {
                    "reader_id": "test",
                    "device": "test",
                    "model_name": "test",
                    "model_type": "test",
                    "pids": [0],
                    "ready": True,
                }
            ]
        },
    )

    client = TakeoffClient()

    response = await client.get_readers_async()
    assert response == {
        "primary": [
            {
                "reader_id": "test",
                "device": "test",
                "model_name": "test",
                "model_type": "test",
                "pids": [0],
                "ready": True,
            }
        ]
    }


def test_tokenize(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"tokens": ["token1", "token2", "token3"], "tokens_count": 3},
    )
    httpx_mock.add_response(
        json={"tokens": ["token1", "token2", "token3"], "tokens_count": 3},
    )

    client = TakeoffClient()

    tokens = client.tokenize("reader_id", "text to tokenize")
    assert tokens == ["token1", "token2", "token3"]

    num_tokens = client.tokens_count("reader_id", "text to tokenize")
    assert num_tokens == 3


@pytest.mark.asyncio
async def test_tokenize_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"tokens": ["token1", "token2", "token3"], "tokens_count": 3},
    )
    httpx_mock.add_response(
        json={"tokens": ["token1", "token2", "token3"], "tokens_count": 3},
    )

    client = TakeoffClient()

    tokens = await client.tokenize_async("reader_id", "text to tokenize")
    assert tokens == ["token1", "token2", "token3"]

    num_tokens = await client.tokens_count_async("reader_id", "text to tokenize")
    assert num_tokens == 3


def test_chat_template(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"messages": ["<s>[INST] User Message [/INST]Assistant Message</s>[INST] User Response [/INST]"]},
    )

    client = TakeoffClient()

    input = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, how about you?"},
    ]

    chat_template = client.chat_template(input=input, reader_id="reader_id")
    assert chat_template == ["<s>[INST] User Message [/INST]Assistant Message</s>[INST] User Response [/INST]"]


@pytest.mark.asyncio
async def test_chat_template_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"messages": ["<s>[INST] User Message [/INST]Assistant Message</s>[INST] User Response [/INST]"]},
    )

    client = TakeoffClient()

    input = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, how about you?"},
    ]

    chat_template = await client.chat_template_async(input=input, reader_id="reader_id")
    assert chat_template == ["<s>[INST] User Message [/INST]Assistant Message</s>[INST] User Response [/INST]"]


def test_classify(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"result": [[1.1953125], [-10.1875], [-10.1875]]},
    )

    client = TakeoffClient()

    response = client.classify("text to classify")
    assert response == {"result": [[1.1953125], [-10.1875], [-10.1875]]}


@pytest.mark.asyncio
async def test_classify_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"result": [[1.1953125], [-10.1875], [-10.1875]]},
    )

    client = TakeoffClient()

    response = await client.classify_async("text to classify")
    assert response == {"result": [[1.1953125], [-10.1875], [-10.1875]]}


def test_create_reader(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"reader_id": "test"},
    )

    client = TakeoffClient()
    response = client.create_reader({"model_name": "test", "device": "cuda"})

    assert response == {"reader_id": "test"}


@pytest.mark.asyncio
async def test_create_reader_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"reader_id": "test"},
    )

    client = TakeoffClient()
    response = await client.create_reader_async({"model_name": "test", "device": "cuda"})

    assert response == {"reader_id": "test"}


def test_reader_create_failure_bad_device():
    client = TakeoffClient()
    # No device specified
    with pytest.raises(TakeoffException) as e:
        client.create_reader({"model_name": "test", "device": "mars"})
    assert "device" in str(e.value)
    # Wrong device
    with pytest.raises(TakeoffException) as e:
        client.create_reader({"model_name": "test"})
    assert "device" in str(e.value)


def test_reader_create_failure_bad_model_name():
    client = TakeoffClient()
    # No model specified
    with pytest.raises(TakeoffException) as e:
        client.create_reader({"device": "mars"})
    assert "model_name" in str(e.value)
    # Empty model string
    with pytest.raises(TakeoffException) as e:
        client.create_reader({"model_name": ""})
    assert "model_name" in str(e.value)


def test_reader_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=204,
    )

    client = TakeoffClient()
    response = client.delete_reader("test")

    assert response is None


@pytest.mark.asyncio
async def test_reader_delete_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=204,
    )

    client = TakeoffClient()
    response = await client.delete_reader_async("test")

    assert response is None


def test_list_reader_groups(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"primary": {"reader_id": "test"}},
    )

    client = TakeoffClient()
    response = client.list_all_readers()

    assert response == {"primary": {"reader_id": "test"}}


@pytest.mark.asyncio
async def test_list_reader_groups_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"primary": {"reader_id": "test"}},
    )

    client = TakeoffClient()
    response = await client.list_all_readers_async()

    assert response == {"primary": {"reader_id": "test"}}


def test_get_reader_config(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"reader_id": "test"},
    )

    client = TakeoffClient()
    response = client.get_reader_config("test")

    assert response == {"reader_id": "test"}


@pytest.mark.asyncio
async def test_get_reader_config_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={"reader_id": "test"},
    )

    client = TakeoffClient()
    response = await client.get_reader_config_async("test")

    assert response == {"reader_id": "test"}


@pytest.mark.asyncio
async def test_get_status_async(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://localhost:3001/status",
        method="GET",
        json={"status": {"live_readers": [], "dead_readers": []}, "config": {"reader_id": "test"}},
    )

    client = TakeoffClient()
    response = await client.get_status_async()

    assert response == {"status": {"live_readers": [], "dead_readers": []}, "config": {"reader_id": "test"}}


def test_get_status(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://localhost:3001/status",
        method="GET",
        json={"status": {"live_readers": [], "dead_readers": []}, "config": {"reader_id": "test"}},
    )

    client = TakeoffClient()
    response = client.get_status()

    assert response == {"status": {"live_readers": [], "dead_readers": []}, "config": {"reader_id": "test"}}
