#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################

'''
Custom ZenPack initialization code. All code defined in this module will
be executed at startup time in all Zope clients.
'''

import logging
log = logging.getLogger('zen.Zentrospect')

import Globals

from Products.ZenModel.Device import Device
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenUtils.Utils import unused
from Products.Zuul.interfaces import ICatalogTool

unused(Globals)


ZP_NAME = 'ZenPacks.zenoss.Zentrospect'

# Modules containing model classes. Used by zenchkschema to validate
# bidirectional integrity of defined relationships.
productNames = (
    'System',
    'Process',
    'Metric',
    )

# Useful to avoid making literal string references to module and class names
# throughout the rest of the ZenPack.
MODULE_NAME = {}
CLASS_NAME = {}
for product_name in productNames:
    MODULE_NAME[product_name] = '.'.join([ZP_NAME, product_name])
    CLASS_NAME[product_name] = '.'.join([ZP_NAME, product_name, product_name])

# Define new device relations.
NEW_DEVICE_RELATIONS = [
    ('z_systems', MODULE_NAME['System']),
    ]

NEW_COMPONENT_TYPES = [
    CLASS_NAME['System'],
    ]

# Add new relationships to Device if they don't already exist.
for relname, modname in NEW_DEVICE_RELATIONS:
    if relname not in (x[0] for x in Device._relations):
        Device._relations += (
            (relname, ToManyCont(ToOne, modname, 'z_device')),
            )


class ZenPack(ZenPackBase):
    '''
    ZenPack loader that handles custom installation and removal tasks.
    '''

    def install(self, app):
        super(ZenPack, self).install(app)

        log.info('Adding Zentrospect relationships to existing devices')
        self._buildDeviceRelations()

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            log.info('Removing Zentrospect components')
            cat = ICatalogTool(app.zport.dmd)
            for brain in cat.search(types=NEW_COMPONENT_TYPES):
                component = brain.getObject()
                component.getPrimaryParent()._delObject(component.id)

            # Remove our Device relations additions.
            Device._relations = tuple(
                [x for x in Device._relations
                    if x[0] not in NEW_DEVICE_RELATIONS])

            log.info('Removing Zentrospect device relationships')
            self._buildDeviceRelations()

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

    def _buildDeviceRelations(self):
        for d in self.dmd.Devices.getSubDevicesGen():
            d.buildRelations()
