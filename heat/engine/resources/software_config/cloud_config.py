#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from heat.common.template_format import yaml
from heat.common.template_format import yaml_dumper
from heat.engine import properties
from heat.engine.resources.software_config import software_config
from heat.engine import support


class CloudConfig(software_config.SoftwareConfig):
    '''
    A configuration resource for representing cloud-init cloud-config.

    This resource allows cloud-config YAML to be defined and stored by the
    config API. Any intrinsic functions called in the config will be resolved
    before storing the result.

    This resource will generally be referenced by OS::Nova::Server user_data,
    or OS::Heat::MultipartMime parts config. Since cloud-config is boot-only
    configuration, any changes to the definition will result in the
    replacement of all servers which reference it.
    '''

    support_status = support.SupportStatus(version='2014.1')

    PROPERTIES = (
        CLOUD_CONFIG
    ) = (
        'cloud_config'
    )

    properties_schema = {
        CLOUD_CONFIG: properties.Schema(
            properties.Schema.MAP,
            _('Map representing the cloud-config data structure which will '
              'be formatted as YAML.')
        )
    }

    def handle_create(self):
        props = {self.NAME: self.physical_resource_name()}
        cloud_config = yaml.dump(self.properties.get(
            self.CLOUD_CONFIG), Dumper=yaml_dumper)
        props[self.CONFIG] = '#cloud-config\n%s' % cloud_config
        sc = self.heat().software_configs.create(**props)
        self.resource_id_set(sc.id)


def resource_mapping():
    return {
        'OS::Heat::CloudConfig': CloudConfig,
    }
