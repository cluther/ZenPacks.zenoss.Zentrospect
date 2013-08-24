#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################

from itertools import chain, combinations

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
from ZenPacks.zenoss.Zentrospect.utils import sorted_powerset


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

    def getRRDTemplates(self):
        '''
        Return the monitoring templates to use for this metric.

        Given the z-localhost-zendisc-devices metric this will attempt
        to return the following precedence-order. The first name for
        which a template exists will be used::

            ZentrospectMetric-localhost-zendisc-devices
            ZentrospectMetric-zendisc-devices
            ZentrospectMetric-localhost-devices
            ZentrospectMetric-localhost-zendisc
            ZentrospectMetric-devices
            ZentrospectMetric-zendisc
            ZentrospectMetric-localhost
        '''
        basename = self.getRRDTemplateName()
        process = self.process()
        powerset = sorted_powerset((
            process.system().system_name,
            process.process_name,
            self.metric_name))

        for parts in powerset:
            template = self.getRRDTemplateByName('-'.join((basename,) + parts))
            if template:
                return [template]

        return []


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
