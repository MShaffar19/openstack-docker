# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2013 dotCloud, Inc.
# All Rights Reserved.
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

from nova import test
from nova.tests import utils
import nova.tests.virt.docker.mock_client
from nova.tests.virt import test_virt_drivers


class DockerDriverTestCase(test_virt_drivers._VirtDriverTestCase, test.TestCase):

    driver_module = 'nova.virt.docker.DockerDriver'
    driver_args = [nova.tests.virt.docker.mock_client.MockClient,]

    def setUp(self):
        super(DockerDriverTestCase, self).setUp()

        def fake_setup_network(self, instance, network_info):
            return

        self.stubs.Set(nova.virt.docker.driver.DockerDriver,
                       '_setup_network',
                       fake_setup_network)

    #NOTE(bcwaldon): This exists only because _get_running_instance on the
    # base class will not let us set a custom disk/container_format.
    def _get_running_instance(self):
        instance_ref = utils.get_test_instance()
        network_info = utils.get_test_network_info(legacy_model=False)
        network_info[0]['network']['subnets'][0]['meta']['dhcp_server'] = \
            '1.1.1.1'
        image_info = utils.get_test_image_info(None, instance_ref)
        image_info['disk_format'] = 'raw'
        image_info['container_format'] = 'docker'
        self.connection.spawn(self.ctxt, instance_ref, image_info,
                              [], 'herp', network_info=network_info)
        return instance_ref, network_info