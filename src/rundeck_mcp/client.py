"""Async HTTP client for the Rundeck API."""

from __future__ import annotations

from typing import Any

import httpx

from .config import RundeckConfig
from .exceptions import APIError, AuthenticationError, NotFoundError


class RundeckClient:
    """Thin async wrapper around httpx for the Rundeck REST API."""

    def __init__(self, config: RundeckConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient(
            base_url=config.api_base,
            headers={
                "X-Rundeck-Auth-Token": config.api_token,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=config.timeout,
            verify=config.verify_ssl,
        )

    @property
    def config(self) -> RundeckConfig:
        return self._config

    async def aclose(self) -> None:
        """Close the underlying httpx client."""
        await self._client.aclose()

    async def __aenter__(self) -> RundeckClient:
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> Any:
        """Perform an HTTP request and return parsed JSON (or empty dict)."""
        cleaned_params: dict[str, Any] | None = None
        if params is not None:
            cleaned_params = {k: v for k, v in params.items() if v is not None}

        try:
            response = await self._client.request(
                method, path, params=cleaned_params, json=json
            )
        except httpx.HTTPError as exc:
            raise APIError(f"HTTP error talking to Rundeck: {exc}") from exc

        if response.status_code in (401, 403):
            raise AuthenticationError(
                f"Rundeck rejected credentials (HTTP {response.status_code})."
            )
        if response.status_code == 404:
            raise NotFoundError(
                f"Rundeck resource not found: {method} {path}"
            )
        if response.status_code >= 400:
            raise APIError(
                f"Rundeck API error {response.status_code}: {response.text}",
                status_code=response.status_code,
            )

        if not response.content:
            return {}
        ctype = response.headers.get("content-type", "")
        if "application/json" in ctype:
            return response.json()
        return {"raw": response.text}

    # Projects -----------------------------------------------------------------
    async def list_projects(self) -> Any:
        return await self._request("GET", "/projects")

    # Jobs ---------------------------------------------------------------------
    async def list_jobs(self, project: str) -> Any:
        return await self._request("GET", f"/project/{project}/jobs")

    async def get_job(self, job_id: str) -> Any:
        return await self._request("GET", f"/job/{job_id}")

    async def run_job(
        self,
        job_id: str,
        options: dict[str, Any] | None = None,
        node_filter: str | None = None,
    ) -> Any:
        payload: dict[str, Any] = {}
        if options:
            payload["options"] = options
        if node_filter:
            payload["filter"] = node_filter
        return await self._request(
            "POST", f"/job/{job_id}/run", json=payload or None
        )

    async def enable_job_schedule(self, job_id: str) -> Any:
        return await self._request("POST", f"/job/{job_id}/schedule/enable")

    async def disable_job_schedule(self, job_id: str) -> Any:
        return await self._request("POST", f"/job/{job_id}/schedule/disable")

    async def enable_job_execution(self, job_id: str) -> Any:
        return await self._request("POST", f"/job/{job_id}/execution/enable")

    async def disable_job_execution(self, job_id: str) -> Any:
        return await self._request("POST", f"/job/{job_id}/execution/disable")

    # Executions ---------------------------------------------------------------
    async def get_execution(self, execution_id: str | int) -> Any:
        return await self._request("GET", f"/execution/{execution_id}")

    async def get_execution_output(self, execution_id: str | int) -> Any:
        return await self._request("GET", f"/execution/{execution_id}/output")

    async def abort_execution(self, execution_id: str | int) -> Any:
        # Rundeck spec: abort is GET, not POST/DELETE.
        return await self._request("GET", f"/execution/{execution_id}/abort")

    async def list_executions(
        self,
        project: str,
        status: str | None = None,
        max_results: int = 20,
    ) -> Any:
        params: dict[str, Any] = {"max": max_results}
        if status:
            params["statusFilter"] = status
        return await self._request(
            "GET", f"/project/{project}/executions", params=params
        )

    # Nodes --------------------------------------------------------------------
    async def list_nodes(self, project: str, filter: str | None = None) -> Any:
        params: dict[str, Any] = {}
        if filter:
            params["filter"] = filter
        return await self._request(
            "GET", f"/project/{project}/resources", params=params
        )
