# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from composio_client import Composio, AsyncComposio
from composio_client.types.v3.internal import (
    ActionExecutionSearchLogsResponse,
    ActionExecutionRetrieveLogResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestActionExecution:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve_log(self, client: Composio) -> None:
        action_execution = client.v3.internal.action_execution.retrieve_log(
            "id",
        )
        assert_matches_type(ActionExecutionRetrieveLogResponse, action_execution, path=["response"])

    @parametrize
    def test_raw_response_retrieve_log(self, client: Composio) -> None:
        response = client.v3.internal.action_execution.with_raw_response.retrieve_log(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action_execution = response.parse()
        assert_matches_type(ActionExecutionRetrieveLogResponse, action_execution, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_log(self, client: Composio) -> None:
        with client.v3.internal.action_execution.with_streaming_response.retrieve_log(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action_execution = response.parse()
            assert_matches_type(ActionExecutionRetrieveLogResponse, action_execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve_log(self, client: Composio) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.v3.internal.action_execution.with_raw_response.retrieve_log(
                "",
            )

    @parametrize
    def test_method_search_logs(self, client: Composio) -> None:
        action_execution = client.v3.internal.action_execution.search_logs(
            cursor=0,
        )
        assert_matches_type(ActionExecutionSearchLogsResponse, action_execution, path=["response"])

    @parametrize
    def test_method_search_logs_with_all_params(self, client: Composio) -> None:
        action_execution = client.v3.internal.action_execution.search_logs(
            cursor=0,
            case_sensitive=True,
            from_=0,
            limit=0,
            search_params=[
                {
                    "field": "field",
                    "operation": "operation",
                    "value": "value",
                }
            ],
            to=0,
        )
        assert_matches_type(ActionExecutionSearchLogsResponse, action_execution, path=["response"])

    @parametrize
    def test_raw_response_search_logs(self, client: Composio) -> None:
        response = client.v3.internal.action_execution.with_raw_response.search_logs(
            cursor=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action_execution = response.parse()
        assert_matches_type(ActionExecutionSearchLogsResponse, action_execution, path=["response"])

    @parametrize
    def test_streaming_response_search_logs(self, client: Composio) -> None:
        with client.v3.internal.action_execution.with_streaming_response.search_logs(
            cursor=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action_execution = response.parse()
            assert_matches_type(ActionExecutionSearchLogsResponse, action_execution, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncActionExecution:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve_log(self, async_client: AsyncComposio) -> None:
        action_execution = await async_client.v3.internal.action_execution.retrieve_log(
            "id",
        )
        assert_matches_type(ActionExecutionRetrieveLogResponse, action_execution, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_log(self, async_client: AsyncComposio) -> None:
        response = await async_client.v3.internal.action_execution.with_raw_response.retrieve_log(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action_execution = await response.parse()
        assert_matches_type(ActionExecutionRetrieveLogResponse, action_execution, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_log(self, async_client: AsyncComposio) -> None:
        async with async_client.v3.internal.action_execution.with_streaming_response.retrieve_log(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action_execution = await response.parse()
            assert_matches_type(ActionExecutionRetrieveLogResponse, action_execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve_log(self, async_client: AsyncComposio) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.v3.internal.action_execution.with_raw_response.retrieve_log(
                "",
            )

    @parametrize
    async def test_method_search_logs(self, async_client: AsyncComposio) -> None:
        action_execution = await async_client.v3.internal.action_execution.search_logs(
            cursor=0,
        )
        assert_matches_type(ActionExecutionSearchLogsResponse, action_execution, path=["response"])

    @parametrize
    async def test_method_search_logs_with_all_params(self, async_client: AsyncComposio) -> None:
        action_execution = await async_client.v3.internal.action_execution.search_logs(
            cursor=0,
            case_sensitive=True,
            from_=0,
            limit=0,
            search_params=[
                {
                    "field": "field",
                    "operation": "operation",
                    "value": "value",
                }
            ],
            to=0,
        )
        assert_matches_type(ActionExecutionSearchLogsResponse, action_execution, path=["response"])

    @parametrize
    async def test_raw_response_search_logs(self, async_client: AsyncComposio) -> None:
        response = await async_client.v3.internal.action_execution.with_raw_response.search_logs(
            cursor=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action_execution = await response.parse()
        assert_matches_type(ActionExecutionSearchLogsResponse, action_execution, path=["response"])

    @parametrize
    async def test_streaming_response_search_logs(self, async_client: AsyncComposio) -> None:
        async with async_client.v3.internal.action_execution.with_streaming_response.search_logs(
            cursor=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action_execution = await response.parse()
            assert_matches_type(ActionExecutionSearchLogsResponse, action_execution, path=["response"])

        assert cast(Any, response.is_closed) is True
