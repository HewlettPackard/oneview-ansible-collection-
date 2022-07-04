#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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

from __future__ import (absolute_import, division, print_function)
import json

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''

---
module: login_session
short_description: Manages OneView login sessions
description:
    - Provides Session Id for login to the appliance.
version_added: "2.4.0"
requirements:
    - "python >= 3.4.2"
    - "hpeOneView >= 5.4.0"
author: "Alisha K (@alisha-k.kalladassery)"
options:
    name:
        description:
            - Indicates given name for the session.
        required: false
        type: str
extends_documentation_fragment:
- hpe.oneview.oneview
- hpe.oneview.oneview.validateetag
- hpe.oneview.oneview.params
'''

EXAMPLES = '''
- name: Fetch Session Id
  login_session:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1200
    name: "Test_Session"
  delegate_to: localhost
  register: session

- name: Fetch Session Id with config json
  login_session:
    config: "{{ config }}"
    name: "Test_Session"
  delegate_to: localhost
  register: session
'''

RETURN = '''
oneview_session:
    description: Has the facts about the oneview session created
    type: dict
'''

from ansible_collections.hpe.oneview.plugins.module_utils.oneview import OneViewModule
from hpeOneView.connection import connection

class LoginSessionModule(OneViewModule):
    MSG_CREATED = 'Session created successfully.'
    MSG_NOT_CREATED = 'Session creation failed.'

    def __init__(self):
        additional_arg_spec = dict(name=dict(required=False, type='str'))

        super().__init__(additional_arg_spec=additional_arg_spec,
                         validate_etag_support=True)

    def execute_module(self):

        oneview_config = self.get_config()
        if oneview_config:
            conn = connection(oneview_config.get('ip'), oneview_config.get('api_version'), oneview_config.get('ssl_certificate', False),
                                            oneview_config.get('timeout'))
            task, body = conn.post('/rest/login-sessions', oneview_config.get('credentials'))
            auth = body['sessionID']
            return dict(changed=True, msg=self.MSG_CREATED, ansible_facts={"session":auth})
        else:
            return dict(changed=False, msg=self.MSG_NOT_CREATED, ansible_facts=None)


    def get_config(self):
        if self.module.params.get('config'):
            with open(self.module.params['config']) as json_data:
                oneview_config = json.load(json_data)
        elif self.module.params.get('hostname'):
            oneview_config = dict(ip=self.module.params['hostname'],
                          credentials=dict(userName=self.module.params['username'], password=self.module.params['password'],
                                           authLoginDomain=self.module.params.get('auth_login_domain', '')),
                          api_version=self.module.params['api_version'],
                          image_streamer_ip=self.module.params['image_streamer_hostname'])
        return oneview_config


def main():
    LoginSessionModule().run()


if __name__ == '__main__':
    main()