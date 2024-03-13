# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from pytest_mock import MockerFixture

from superset.extensions.telemetry_handler import TelemetryHandler


def test_telemetry_handler(mocker: MockerFixture) -> None:
    """
    Test the telemetry handler.
    """
    time = mocker.patch("superset.extensions.telemetry_handler.time")
    time.time.side_effect = [1, 2, 3, 4]

    handler = TelemetryHandler()
    with handler.add("outter"):
        with handler.add("inner"):
            pass

    assert handler.events == [
        {
            "name": "outter",
            "start": 1,
            "children": [
                {
                    "name": "inner",
                    "start": 2,
                    "children": [],
                    "end": 3,
                },
            ],
            "end": 4,
        }
    ]
