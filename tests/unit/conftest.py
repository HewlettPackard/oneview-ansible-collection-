###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

import pytest

from mock import Mock, patch, mock
# from hpeOneView.oneview_client import OneViewClient
from ansible_collections.hpe.oneview.tests.unit.utils.hpe_test_utils import OneViewClientTest
from ansible_collections.hpe.oneview.tests.unit.utils.oneview_module_loader import ONEVIEW_MODULE_UTILS_PATH


@mock.patch.object(OneViewClientTest, 'from_json_file')
@pytest.fixture
def mock_ov_client(mock_json_file):
    # patcher_json_file = patch.object(OneViewClientTest, 'from_json_file')
    client = mock_json_file.start()
    return client.return_value


@pytest.fixture
def mock_ansible_module():
    patcher_ansible = patch(ONEVIEW_MODULE_UTILS_PATH + '.AnsibleModule')
    patcher_ansible = patcher_ansible.start()
    ansible_module = Mock()
    patcher_ansible.return_value = ansible_module
    return ansible_module