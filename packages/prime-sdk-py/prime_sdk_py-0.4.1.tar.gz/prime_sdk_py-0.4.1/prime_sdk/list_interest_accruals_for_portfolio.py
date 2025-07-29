# Copyright 2025-present Coinbase Global, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import Optional, List
from prime_sdk.base_response import BaseResponse
from prime_sdk.client import Client
from prime_sdk.credentials import Credentials
from prime_sdk.model import Accrual
from prime_sdk.utils import append_query_param


@dataclass
class ListInterestAccrualsForPortfolioRequest:
    portfolio_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    allowed_status_codes: Optional[List[int]] = None


@dataclass
class ListInterestAccrualsForPortfolioResponse(BaseResponse):
    total_notional_accrual: str = None
    accruals: List[Accrual] = None


class PrimeClient:
    def __init__(self, credentials: Credentials):
        self.client = Client(credentials)

    def list_interest_accruals_for_portfolio(self, request: ListInterestAccrualsForPortfolioRequest) -> ListInterestAccrualsForPortfolioResponse:
        path = f"/portfolios/{request.portfolio_id}/accruals"
        query_params = append_query_param("", "portfolio_id", request.portfolio_id)
        query_params = append_query_param(query_params, "start_date", request.start_date)
        query_params = append_query_param(query_params, "end_date", request.end_date)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return ListInterestAccrualsForPortfolioResponse(response.json())
