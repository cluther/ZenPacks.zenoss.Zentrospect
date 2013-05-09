##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from zope.component import adapts
from zope.interface import implements

from Products.ZenRelations.RelSchema import ToOne, ToManyCont
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from ZenPacks.zenoss.Zentrospect import MODULE_NAME
from ZenPacks.zenoss.Zentrospect.Component import Component


class System(Component):
    '''
    Model class for System.
    '''

    meta_type = portal_type = 'ZentrospectSystem'

    system_name = None

    _properties = Component._properties + (
        {'id': 'system_name', 'type': 'string', 'mode': 'w'},
        )

    _relations = Component._relations + (
        ('z_device', ToOne(ToManyCont, 'Products.ZenModel.Device', 'z_systems')),
        ('processes', ToManyCont(ToOne, MODULE_NAME['Process'], 'system')),
        )


class ISystemInfo(IComponentInfo):
    '''
    API Info interface for System.
    '''

    title = schema.TextLine(title=_t(u'Title'))
    system_name = schema.TextLine(title=_t(u'System Name'))
    process_count = schema.Int(title=_t(u'Number of Processes'))
    metric_count = schema.Int(title=_t(u'Number of Metrics'))


class SystemInfo(ComponentInfo):
    '''
    API Info adapter factory for System.
    '''

    implements(ISystemInfo)
    adapts(System)

    title = ProxyProperty('title')
    system_name = ProxyProperty('system_name')

    @property
    def process_count(self):
        return self._object.processes.countObjects()

    @property
    def metric_count(self):
        return sum(p.metrics.countObjects() for p in self._object.processes())
