# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""Tests for batches.get()."""

import pytest

from ... import types
from .. import pytest_helper


_BATCH_JOB_NAME = '5798522612028014592'
_BATCH_JOB_FULL_RESOURCE_NAME = (
    'projects/964831358985/locations/us-central1/'
    f'batchPredictionJobs/{_BATCH_JOB_NAME}'
)
_INVALID_BATCH_JOB_NAME = 'invalid_name'


# All tests will be run for both Vertex and MLDev.
test_table: list[pytest_helper.TestTableItem] = [
    pytest_helper.TestTableItem(
        name='test_get_batch_job',
        parameters=types._GetBatchJobParameters(
            name=_BATCH_JOB_NAME,
        ),
        exception_if_mldev='only supported in the Vertex AI client',
    ),
    pytest_helper.TestTableItem(
        name='test_get_batch_job_with_full_resource_name',
        parameters=types._GetBatchJobParameters(
            name=_BATCH_JOB_FULL_RESOURCE_NAME,
        ),
        exception_if_mldev='only supported in the Vertex AI client',
        override_replay_id='test_get_batch_job',
    ),
    pytest_helper.TestTableItem(
        name='test_get_batch_job_with_invalid_name',
        parameters=types._GetBatchJobParameters(
            name=_INVALID_BATCH_JOB_NAME,
        ),
        exception_if_mldev='only supported in the Vertex AI client',
        exception_if_vertex='Invalid batch job name',
    ),
]

pytestmark = pytest_helper.setup(
    file=__file__,
    globals_for_file=globals(),
    test_method='batches.get',
    test_table=test_table,
)


@pytest.mark.asyncio
async def test_async_get(client):
  with pytest_helper.exception_if_mldev(client, ValueError):
    batch_job = await client.aio.batches.get(name=_BATCH_JOB_NAME)

    assert batch_job