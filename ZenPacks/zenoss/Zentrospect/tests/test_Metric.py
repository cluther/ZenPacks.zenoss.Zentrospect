#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################

'''
Tests for model classes.
'''

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ZenPacks.zenoss.Zentrospect.tests.utils import add_contained


def create_device(dmd):
    '''
    Return a device with Zentrospect components suitable for testing.
    '''
    device = dmd.Devices.createInstance('test-device1')

    from ZenPacks.zenoss.Zentrospect.System import System
    system = add_contained(device, 'z_systems', System('z-localhost'))
    system.system_name = 'localhost'

    from ZenPacks.zenoss.Zentrospect.Process import Process
    process = add_contained(system, 'processes', Process('z-localhost-zendisc'))
    process.process_name = 'zendisc'

    from ZenPacks.zenoss.Zentrospect.Metric import Metric
    metric = add_contained(process, 'metrics', Metric('z-localhost-zendisc-devices'))
    metric.metric_name = 'devices'

    return device


class TestModel(BaseTestCase):
    def device(self):
        if not hasattr(self, '_device'):
            self._device = create_device(self.dmd)

        return self._device

    def test_Metric_getRRDTemplates(self):
        metric = self.device().getObjByPath(
            'z_systems/z-localhost/processes/z-localhost-zendisc/metrics/z-localhost-zendisc-devices')

        template_names = (
            'ZentrospectMetric-localhost-zendisc-devices',
            'ZentrospectMetric-zendisc-devices',
            'ZentrospectMetric-localhost-devices',
            'ZentrospectMetric-localhost-zendisc',
            'ZentrospectMetric-devices',
            'ZentrospectMetric-zendisc',
            'ZentrospectMetric-localhost',
            )

        for template_name in template_names:
            self.dmd.Devices.manage_addRRDTemplate(template_name)

        for i, template_name in enumerate(template_names):
            self.assertEquals(metric.getRRDTemplates()[0].id, template_names[i])
            self.dmd.Devices.manage_deleteRRDTemplates([template_name])
