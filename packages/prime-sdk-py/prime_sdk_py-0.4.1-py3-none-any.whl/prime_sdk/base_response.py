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

import json
import dataclasses
from dataclasses import dataclass, field
from typing import Any, Dict, get_origin, get_args, get_type_hints


@dataclass
class BaseResponse:
    response: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, response: Dict[str, Any] = None, **kwargs):
        object.__setattr__(self, "response", response or {})

        for field_name in self.__dataclass_fields__:
            if field_name == "response":
                continue
            if field_name in kwargs:
                object.__setattr__(self, field_name, kwargs[field_name])

    def __post_init__(self):
        child_cls = type(self)

        type_hints = get_type_hints(child_cls)

        for field_name, real_type in type_hints.items():
            if field_name == "response":
                continue

            current_val = getattr(self, field_name, None)
            if current_val is not None:
                continue

            raw_value = self.response.get(field_name)
            if raw_value is None:
                continue

            if dataclasses.is_dataclass(real_type) and isinstance(raw_value, dict):
                parsed_obj = real_type(**raw_value)
                object.__setattr__(self, field_name, parsed_obj)
                continue

            if get_origin(real_type) is list:
                (inner_type,) = get_args(real_type)
                if dataclasses.is_dataclass(inner_type) and isinstance(raw_value, list):
                    parsed_list = [inner_type(**item) for item in raw_value]
                    object.__setattr__(self, field_name, parsed_list)
                    continue

            object.__setattr__(self, field_name, raw_value)

    def __str__(self) -> str:
        return json.dumps(self.response)

    def __repr__(self) -> str:
        return self.__str__()
