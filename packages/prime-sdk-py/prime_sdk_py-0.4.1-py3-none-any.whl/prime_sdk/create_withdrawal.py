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
from prime_sdk.model import Blockchain


@dataclass
class PaymentMethod:
    payment_method_id: str


@dataclass
class BlockchainAddress:
    address: str
    account_identifier: Optional[str] = None
    allowed_status_codes: Optional[List[int]] = None


@dataclass
class CreateWithdrawalRequest:
    portfolio_id: str
    wallet_id: str
    amount: str
    destination_type: str
    idempotency_key: str
    currency_symbol: str
    payment_method: Optional[PaymentMethod] = None
    blockchain_address: Optional[BlockchainAddress] = None
    allowed_status_codes: Optional[List[int]] = None


@dataclass
class CreateWithdrawalResponse(BaseResponse):
    activity_id: str = None
    approval_url: str = None
    symbol: str = None
    amount: str = None
    fee: str = None
    destination_type: str = None
    source_type: str = None
    blockchain_destination: Blockchain = None
    blockchain_source: Blockchain = None
    transaction_id: str = None


class PrimeClient:
    def __init__(self, credentials: Credentials):
        self.client = Client(credentials)
        
    def create_withdrawal(self, request: CreateWithdrawalRequest) -> CreateWithdrawalResponse:
        path = f"/portfolios/{request.portfolio_id}/wallets/{request.wallet_id}/withdrawals"

        body = {k: v for k, v in asdict(request).items() if v is not None}

        if request.payment_method:
            body["payment_method"] = asdict(request.payment_method)

        if request.blockchain_address:
            body["blockchain_address"] = asdict(request.blockchain_address)

        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return CreateWithdrawalResponse(response.json())
