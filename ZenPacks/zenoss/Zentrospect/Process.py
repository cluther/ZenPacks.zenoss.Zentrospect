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
from Products.Zuul.decorators import info
from Products.Zuul.form import schema
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from ZenPacks.zenoss.Zentrospect import MODULE_NAME
from ZenPacks.zenoss.Zentrospect.Component import Component


class Process(Component):
    '''
    Model class for Process.
    '''

    meta_type = portal_type = 'ZentrospectProcess'

    _relations = Component._relations + (
        ('system', ToOne(ToManyCont, MODULE_NAME['System'], 'processes')),
        ('metrics', ToManyCont(ToOne, MODULE_NAME['Metric'], 'process')),
        )


class IProcessInfo(IComponentInfo):
    '''
    API Info interface for Process.
    '''

    system = schema.Entity(title=_t(u'System'))
    metric_count = schema.Int(title=_t(u'Number of Metrics'))


class ProcessInfo(ComponentInfo):
    '''
    API Info adapter factory for Process.
    '''

    implements(IProcessInfo)
    adapts(Process)

    @property
    @info
    def system(self):
        return self._object.system()

    @property
    @info
    def metric_count(self):
        return self._object.metrics.countObjects()
