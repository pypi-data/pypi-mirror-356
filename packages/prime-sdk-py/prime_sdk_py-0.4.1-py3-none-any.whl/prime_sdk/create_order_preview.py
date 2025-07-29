# Copyright 2024-present Coinbase Global, Inc.
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
from prime_sdk.base_response import BaseResponse
from prime_sdk.client import Client
from typing import Optional, List
from prime_sdk.credentials import Credentials
from prime_sdk.enums import OrderSide, OrderType, TimeInForce


@dataclass
class CreateOrderPreviewRequest:
    portfolio_id: str
    side: OrderSide
    product_id: str
    type: OrderType
    base_quantity: Optional[str] = None
    quote_value: Optional[str] = None
    limit_price: Optional[str] = None
    start_time: Optional[str] = None
    expiry_time: Optional[str] = None
    time_in_force: Optional[TimeInForce] = None
    stp_id: Optional[str] = None
    display_quote_size: Optional[str] = None
    display_base_size: Optional[str] = None
    is_raise_exact: Optional[str] = None
    historical_pov: Optional[str] = None
    allowed_status_codes: Optional[List[int]] = None


@dataclass
class CreateOrderPreviewResponse(BaseResponse):
    portfolio_id: str = None
    product_id: str = None
    side: str = None
    type: str = None
    base_quantity: str = None
    quote_value: str = None
    limit_price: str = None
    start_time: str = None
    expiry_time: str = None
    time_in_force: str = None
    commission: str = None
    slippage: str = None
    best_bid: str = None
    best_ask: str = None
    average_filled_price: str = None
    order_total: str = None
    historical_pov: str = None


class PrimeClient:
    def __init__(self, credentials: Credentials):
        self.client = Client(credentials)
        
    def create_order_preview(self, request: CreateOrderPreviewRequest) -> CreateOrderPreviewResponse:
        path = f"/portfolios/{request.portfolio_id}/order_preview"
        body = {k: v for k, v in asdict(request).items() if v is not None}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return CreateOrderPreviewResponse(response.json())
