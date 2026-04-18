"""Tests for RundeckClient using pytest-httpx."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from rundeck_mcp.client import RundeckClient
from rundeck_mcp.exceptions import APIError, AuthenticationError, NotFoundError


async def test_auth_header_sent(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/projects",
        json=[{"name": "demo"}],
    )
    result = await client.list_projects()
    assert result == [{"name": "demo"}]

    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert requests[0].headers["X-Rundeck-Auth-Token"] == "test-token"
    assert requests[0].headers["Accept"] == "application/json"


async def test_list_jobs(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/project/demo/jobs",
        json=[{"id": "j1"}],
    )
    result = await client.list_jobs("demo")
    assert result == [{"id": "j1"}]


async def test_get_job(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/job/abc-123",
        json={"id": "abc-123", "name": "job"},
    )
    result = await client.get_job("abc-123")
    assert result["id"] == "abc-123"


async def test_run_job_with_options(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="POST",
        url=f"{api_base}/job/abc-123/run",
        json={"id": 99, "status": "running"},
    )
    result = await client.run_job(
        "abc-123",
        options={"env": "prod"},
        node_filter="tags: web",
    )
    assert result == {"id": 99, "status": "running"}

    req = httpx_mock.get_requests()[0]
    body = req.read().decode()
    assert "env" in body
    assert "prod" in body
    assert "tags: web" in body


async def test_run_job_no_options(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="POST",
        url=f"{api_base}/job/abc-123/run",
        json={"id": 100},
    )
    await client.run_job("abc-123")
    req = httpx_mock.get_requests()[0]
    assert req.read() in (b"", b"null")


async def test_get_execution(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/execution/42",
        json={"id": 42, "status": "succeeded"},
    )
    result = await client.get_execution(42)
    assert result["status"] == "succeeded"


async def test_get_execution_output(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/execution/42/output",
        json={"entries": [{"log": "hello"}]},
    )
    result = await client.get_execution_output(42)
    assert result["entries"][0]["log"] == "hello"


async def test_abort_execution_is_get(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/execution/42/abort",
        json={"abort": {"status": "pending"}},
    )
    result = await client.abort_execution(42)
    assert result["abort"]["status"] == "pending"


async def test_list_executions_params(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/project/demo/executions?max=5&statusFilter=succeeded",
        json={"executions": []},
    )
    result = await client.list_executions(
        "demo", status="succeeded", max_results=5
    )
    assert result == {"executions": []}


async def test_list_executions_default_max(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/project/demo/executions?max=20",
        json={"executions": []},
    )
    await client.list_executions("demo")


async def test_list_nodes(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/project/demo/resources?filter=tags%3A+web",
        json={"node1": {"name": "node1"}},
    )
    result = await client.list_nodes("demo", filter="tags: web")
    assert "node1" in result


async def test_list_nodes_no_filter(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{api_base}/project/demo/resources",
        json={},
    )
    await client.list_nodes("demo")


async def test_enable_disable_schedule_execution(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    for path in (
        "/job/j1/schedule/enable",
        "/job/j1/schedule/disable",
        "/job/j1/execution/enable",
        "/job/j1/execution/disable",
    ):
        httpx_mock.add_response(
            method="POST", url=f"{api_base}{path}", json={"success": True}
        )

    assert (await client.enable_job_schedule("j1"))["success"] is True
    assert (await client.disable_job_schedule("j1"))["success"] is True
    assert (await client.enable_job_execution("j1"))["success"] is True
    assert (await client.disable_job_execution("j1"))["success"] is True


async def test_401_raises_authentication_error(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET", url=f"{api_base}/projects", status_code=401, json={"error": "nope"}
    )
    with pytest.raises(AuthenticationError):
        await client.list_projects()


async def test_403_raises_authentication_error(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET", url=f"{api_base}/projects", status_code=403, json={}
    )
    with pytest.raises(AuthenticationError):
        await client.list_projects()


async def test_404_raises_not_found(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET", url=f"{api_base}/job/missing", status_code=404, json={}
    )
    with pytest.raises(NotFoundError):
        await client.get_job("missing")


async def test_500_raises_api_error(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="GET", url=f"{api_base}/projects", status_code=500, text="boom"
    )
    with pytest.raises(APIError) as excinfo:
        await client.list_projects()
    assert excinfo.value.status_code == 500


async def test_empty_response_body(
    client: RundeckClient, httpx_mock: HTTPXMock, api_base: str
) -> None:
    httpx_mock.add_response(
        method="POST",
        url=f"{api_base}/job/j1/schedule/enable",
        status_code=204,
    )
    result = await client.enable_job_schedule("j1")
    assert result == {}
