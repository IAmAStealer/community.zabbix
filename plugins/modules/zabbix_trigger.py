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

    def get_triggers(self, trigger_name, host_name, template_name):
        host = host_name if host_name is not None else template_name
        try:
            return self._zapi.trigger.get({'filter': {'description': trigger_name, 'host': host}, "selectDependencies": "extend", "selectTags": "extend"})
        except Exception as e:
            self._module.fail_json(msg="Failed to get trigger: %s" % e)

    def build_api_payload(self, name, params, desc=None, dependencies=None):
        payload = params.copy()
        
        payload['description'] = name
        
        if desc is not None:
            payload['comments'] = desc

        if 'severity' in params or 'priority' in params:
            severity_str = params.get('severity', params.get('priority'))
            if severity_str in self.PRIORITY_TYPES:
                payload['priority'] = self.PRIORITY_TYPES[severity_str]
            payload.pop('severity', None)

        if 'enabled' in params:
            payload['status'] = 0 if params['enabled'] else 1
            payload.pop('enabled', None)
        elif 'status' in params:
            payload['status'] = 0 if params['status'] == 'enabled' else 1

        if 'generate_multiple_events' in params:
            payload['type'] = int(bool(params['generate_multiple_events']))
            payload.pop('generate_multiple_events', None)
            
        if 'manual_close' in params:
            payload['manual_close'] = int(bool(params['manual_close']))

        if 'recovery_mode' in params and params['recovery_mode'] in self.RECOVERY_MODES:
            payload['recovery_mode'] = self.RECOVERY_MODES[params['recovery_mode']]

        if 'correlation_mode' in params:
            payload['correlation_mode'] = 0 if params['correlation_mode'] == 'all' else 1

        if dependencies:
            payload['dependencies'] = []
            for dep in dependencies:
                triggers = self.get_triggers(dep['name'], dep.get('host_name'), dep.get('template_name'))
                payload['dependencies'].extend([{'triggerid': t['triggerid']} for t in triggers])

        return payload

    def add_trigger(self, api_payload):
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        try:
            return self._zapi.trigger.create(api_payload)
        except Exception as e:
            self._module.fail_json(msg="Failed to create trigger: %s" % e)

    def update_trigger(self, api_payload):
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        try:
            return self._zapi.trigger.update(api_payload)
        except Exception as e:
            self._module.fail_json(msg="Failed to update trigger: %s" % e)

    def check_trigger_changed(self, old_trigger):
        try:
            new_trigger = self._zapi.trigger.get({"triggerids": "%s" % old_trigger['triggerid'], "selectDependencies": "extend", "selectTags": "extend"})[0]
        except Exception as e:
            self._module.fail_json(msg="Failed to get trigger: %s" % e)
        return old_trigger != new_trigger

    def delete_trigger(self, trigger_id):
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        try:
            return self._zapi.trigger.delete(trigger_id)
        except Exception as e:
            self._module.fail_json(msg="Failed to delete trigger: %s" % e)


def main():
    argument_spec = zabbix_utils.zabbix_common_argument_spec()
    argument_spec.update(dict(
        name=dict(type='str', required=True),
        host_name=dict(type='str', required=False),
        template_name=dict(type='str', required=False),
        params=dict(type='dict', required=False, default={}),
        desc=dict(type='str', required=False, aliases=['description']),
        dependencies=dict(
            type='list', 
            elements='dict', 
            required=False,
            options=dict(
                name=dict(type='str', required=True),
                host_name=dict(type='str', required=False),
                template_name=dict(type='str', required=False)
            )
        ),
        state=dict(type='str', default="present", choices=['present', 'absent']),
    ))
    
    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[
            ['host_name', 'template_name']
        ],
        mutually_exclusive=[
            ['host_name', 'template_name']
        ],
        required_if=[
            ['state', 'present', ['params']]
        ],
        supports_check_mode=True
    )

    name = module.params['name']
    host_name = module.params.get('host_name')
    template_name = module.params.get('template_name')
    params = module.params.get('params', {})
    desc = module.params.get('desc')
    dependencies = module.params.get('dependencies')
    state = module.params['state']

    trigger = Trigger(module)

    if state == "absent":
        triggers = trigger.get_triggers(name, host_name, template_name)
        if not triggers:
            module.exit_json(changed=False, result="No trigger to delete.")
        else:
            delete_ids = [t['triggerid'] for t in triggers]
            results = trigger.delete_trigger(delete_ids)
            module.exit_json(changed=True, result=results)

    elif state == "present":
        api_payload = trigger.build_api_payload(name, params, desc, dependencies)
        triggers = trigger.get_triggers(name, host_name, template_name)
        
        if 'new_name' in api_payload:
            new_name_trigger = trigger.get_triggers(api_payload['new_name'], host_name, template_name)
            if new_name_trigger:
                module.exit_json(changed=False, result=[{'triggerids': [new_name_trigger[0]['triggerid']]}])
                
        if not triggers:
            if 'new_name' in api_payload:
                module.fail_json(msg='Cannot rename trigger: %s is not found' % name)
            results = trigger.add_trigger(api_payload)
            module.exit_json(changed=True, result=results)
        else:
            results = []
            changed = False
            for t in triggers:
                # Créer une copie pour chaque itération afin d'éviter la destruction des clés
                current_payload = api_payload.copy()
                current_payload['triggerid'] = t['triggerid']
                current_payload.pop('description', None)
                
                if 'new_name' in current_payload:
                    current_payload['description'] = current_payload.pop("new_name")
                    
                results.append(trigger.update_trigger(current_payload))
                if trigger.check_trigger_changed(t):
                    changed = True
                    
            module.exit_json(changed=changed, result=results)


if __name__ == '__main__':
    main()
