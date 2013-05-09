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
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from ZenPacks.zenoss.Zentrospect import MODULE_NAME
from ZenPacks.zenoss.Zentrospect.Component import Component


class Metric(Component):
    '''
    Model class for Metric.
    '''

    meta_type = portal_type = 'ZentrospectMetric'

    metric_name = None

    _properties = Component._properties + (
        {'id': 'metric_name', 'type': 'string', 'mode': 'w'},
        )

    _relations = Component._relations + (
        ('process', ToOne(ToManyCont, MODULE_NAME['Process'], 'metrics')),
        )


class IMetricInfo(IComponentInfo):
    '''
    API Info interface for Metric.
    '''

    title = schema.TextLine(title=_t(u'Title'))
    metric_name = schema.TextLine(title=_t(u'Metric Name'))
    system = schema.Entity(title=_t(u'System'))
    process = schema.Entity(title=_t(u'Process'))
    value = schema.Float(title=_t(u'Value'))
    cycles_old = schema.Float(title=_t('Cycles Since Update'))


class MetricInfo(ComponentInfo):
    '''
    API Info adapter factory for Metric.
    '''

    implements(IMetricInfo)
    adapts(Metric)

    title = ProxyProperty('title')
    metric_name = ProxyProperty('metric_name')

    @property
    @info
    def system(self):
        return self._object.process().system()

    @property
    @info
    def process(self):
        return self._object.process()

    @property
    def value(self):
        return self._object.cacheRRDValue('zenProcessMetricValue', None)

    @property
    def cycles_old(self):
        return self._object.cacheRRDValue('zenProcessMetricCyclesSinceUpdate', None)
