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

from dataclasses import dataclass, asdict
from typing import Optional, List
from prime_sdk.base_response import BaseResponse
from prime_sdk.client import Client
from prime_sdk.credentials import Credentials


@dataclass
class CreateNewLocateRequest:
    portfolio_id: str
    symbol: str
    amount: str
    locate_date: str
    allowed_status_codes: Optional[List[int]] = None


@dataclass
class CreateNewLocateResponse(BaseResponse):
    locate_id: str = None


class PrimeClient:
    def __init__(self, credentials: Credentials):
        self.client = Client(credentials)

    def create_new_locate(self, request: CreateNewLocateRequest) -> CreateNewLocateResponse:
        path = f"/portfolios/{request.portfolio_id}/locates"
        body = {k: v for k, v in asdict(request).items() if v is not None}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return CreateNewLocateResponse(response.json())
