#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: zabbix_trigger
short_description: Create/delete Zabbix triggers
description:
   - Create triggers if they do not exist.
   - Delete existing triggers if they exist.
author:
    - "Andrew Lathrop (@aplathrop)"
requirements:
    - "python >= 2.6"

options:
    state:
        description:
            - Create or delete trigger.
        required: false
        type: str
        default: "present"
        choices: [ "present", "absent" ]
    name:
        description:
            - Name of trigger to create or delete.
            - Overrides "description" in API docs.
            - Cannot be changed. If a trigger's name needs to be changed, it needs to deleted and recreated
        required: true
        type: str
    host_name:
        description:
            - Name of host to add trigger to.
            - Required when I(template_name) is not used.
            - Mutually exclusive with I(template_name).
        required: false
        type: str
    template_name:
        description:
            - Name of template to add trigger to.
            - Required when I(host_name) is not used.
            - Mutually exclusive with I(host_name).
        required: false
        type: str
    desc:
        description:
            - Additional description of the trigger.
            - Overrides "comments" in API docs.
        required: false
        type: str
        aliases: [ "description" ]
    dependencies:
        description:
            - list of triggers that this trigger is dependent on
        required: false
        type: list
        elements: dict
        suboptions:
                name:
                    description:
                        - Name of dependent trigger.
                    required: true
                    type: str
                host_name:
                    description:
                        - Name of host containing dependent trigger.
                        - Required when I(template_name) is not used.
                        - Mutually exclusive with I(template_name).
                    required: false
                    type: str
                template_name:
                    description:
                        - Name of template containing dependent trigger.
                        - Required when I(host_name) is not used.
                        - Mutually exclusive with I(host_name).
                    required: false
                    type: str
    params:
        description:
            - Parameters to create/update trigger with.
            - Required if state is "present".
            - Parameters as defined at https://www.zabbix.com/documentation/current/en/manual/api/reference/trigger/object
            - Additionally supported parameters are below.
        required: false
        type: dict
        suboptions:
            severity:
                description:
                    - Severity of the trigger.
                    - Alias for "priority" in API docs.
                required: false
                type: str
                aliases: [ "priority" ]
                choices:
                    - not_classified
                    - information
                    - warning
                    - average
                    - high
                    - disaster
            status:
                description:
                    - Status of the trigger.
                required: false
                type: str
                choices: [ "enabled", "disabled" ]
            enabled:
                description:
                    - Status of the trigger.
                    - Overrides "status" in API docs.
                required: false
                type: bool
            new_name:
                description:
                    - New name for trigger
                required: false
                type: str
            generate_multiple_events:
                description:
                    - Whether the trigger can generate multiple problem events.
                    - Alias for "type" in API docs.
                required: false
                type: bool
            recovery_mode:
                description:
                    - OK event generation mode.
                    - Overrides "recovery_mode" in API docs.
                required: false
                type: str
                choices:
                    - expression
                    - recovery_expression
                    - none
            correlation_mode:
                description:
                    - OK event closes.
                    - Overrides "correlation_mode" in API docs.
                required: false
                type: str
                choices: [ "all", "tag" ]
            manual_close:
                description:
                    - Allow manual close.
                    - Overrides "manual_close" in API docs.
                required: false
                type: bool

extends_documentation_fragment:
- community.zabbix.zabbix
'''

EXAMPLES = r'''

# If you want to use Username and Password to be authenticated by Zabbix Server
- name: Set credentials to access Zabbix Server API
  ansible.builtin.set_fact:
    ansible_user: Admin
    ansible_httpapi_pass: zabbix

# If you want to use API token to be authenticated by Zabbix Server
# https://www.zabbix.com/documentation/current/en/manual/web_interface/frontend_sections/administration/general#api-tokens
- name: Set API token
  ansible.builtin.set_fact:
    ansible_zabbix_auth_key: 8ec0d52432c15c91fcafe9888500cf9a607f44091ab554dbee860f6b44fac895

# Create ping trigger on example_host
- name: create ping trigger
  # set task level variables as we change ansible_connection plugin here
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 443
    ansible_httpapi_use_ssl: true
    ansible_httpapi_validate_certs: false
    ansible_zabbix_url_path: 'zabbixeu'  # If Zabbix WebUI runs on non-default (zabbix) path ,e.g. http://<FQDN>/zabbixeu
    ansible_host: zabbix-example-fqdn.org
  community.zabbix.zabbix_trigger:
    name: agent_ping
    host_name: example_host
    params:
        severity: high
        expression: 'nodata(/example_host/agent.ping,1m)=1'
        manual_close: True
        enabled: True
    state: present

# Create ping trigger on example_template
- name: create ping trigger
  # set task level variables as we change ansible_connection plugin here
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 443
    ansible_httpapi_use_ssl: true
    ansible_httpapi_validate_certs: false
    ansible_zabbix_url_path: 'zabbixeu'  # If Zabbix WebUI runs on non-default (zabbix) path ,e.g. http://<FQDN>/zabbixeu
    ansible_host: zabbix-example-fqdn.org
  community.zabbix.zabbix_trigger:
    name: agent_ping
    host_name: example_template
    params:
        severity: high
        expression: 'nodata(/example_template/agent.ping,1m)=1'
        manual_close: True
        enabled: True
    state: present

# Add tags to the existing Zabbix trigger
- name: update ping trigger
  # set task level variables as we change ansible_connection plugin here
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 443
    ansible_httpapi_use_ssl: true
    ansible_httpapi_validate_certs: false
    ansible_zabbix_url_path: 'zabbixeu'  # If Zabbix WebUI runs on non-default (zabbix) path ,e.g. http://<FQDN>/zabbixeu
    ansible_host: zabbix-example-fqdn.org
  community.zabbix.zabbix_trigger:
    name: agent_ping
    host_name: example_template
    params:
        severity: high
        expression: 'nodata(/example_template/agent.ping,1m)=1'
        manual_close: True
        enabled: True
        tags:
          - tag: class
            value: application
    state: present

# delete Zabbix trigger
- name: delete ping trigger
  # set task level variables as we change ansible_connection plugin here
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 443
    ansible_httpapi_use_ssl: true
    ansible_httpapi_validate_certs: false
    ansible_zabbix_url_path: 'zabbixeu'  # If Zabbix WebUI runs on non-default (zabbix) path ,e.g. http://<FQDN>/zabbixeu
    ansible_host: zabbix-example-fqdn.org
  community.zabbix.zabbix_trigger:
    name: agent_ping
    host_name: example_template
    state: absent

- name: Rename Zabbix trigger
  # set task level variables as we change ansible_connection plugin here
  vars:
    ansible_network_os: community.zabbix.zabbix
    ansible_connection: httpapi
    ansible_httpapi_port: 443
    ansible_httpapi_use_ssl: true
    ansible_httpapi_validate_certs: false
    ansible_zabbix_url_path: "zabbixeu"  # If Zabbix WebUI runs on non-default (zabbix) path ,e.g. http://<FQDN>/zabbixeu
    ansible_host: zabbix-example-fqdn.org
  community.zabbix.zabbix_trigger:
    name: agent_ping
    template_name: example_template
    params:
      new_name: new_agent_ping
    state: present
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.zabbix.plugins.module_utils.base import ZabbixBase
import ansible_collections.community.zabbix.plugins.module_utils.helpers as zabbix_utils


class Trigger(ZabbixBase):

    PRIORITY_TYPES = {
        'not_classified': 0,
        'information': 1,
        'warning': 2,
        'average': 3,
        'high': 4,
        'disaster': 5
    }

    RECOVERY_MODES = {
        'expression': 0,
        'recovery_expression': 1,
        'none': 2
    }
