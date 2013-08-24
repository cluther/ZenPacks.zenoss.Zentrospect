#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################

from Products.ZenRelations.ToManyRelationship import ToManyRelationshipBase
from Products.ZenRelations.ToOneRelationship import ToOneRelationship
from Products.ZenUtils.guid.interfaces import IGlobalIdentifier

from ZenPacks.zenoss.Impact.impactd.relations import ImpactEdge


RP = 'ZenPacks.zenoss.Zentrospect'
AVAILABILITY = 'AVAILABILITY'
PERCENT = 'policyPercentageTrigger'
THRESHOLD = 'policyThresholdTrigger'


def guid(obj):
    return IGlobalIdentifier(obj).getGUID()


def edge(source, target):
    return ImpactEdge(source, target, RP)


class BaseRelationsProvider(object):
    relationship_provider = RP

    impact_relationships = None
    impacted_by_relationships = None

    def __init__(self, adapted):
        self._object = adapted

    def belongsInImpactGraph(self):
        return True

    def guid(self):
        if not hasattr(self, '_guid'):
            self._guid = guid(self._object)

        return self._guid

    def impact(self, relname):
        relationship = getattr(self._object, relname, None)
        if relationship:
            if isinstance(relationship, ToOneRelationship):
                obj = relationship()
                if obj:
                    yield edge(self.guid(), guid(obj))

            elif isinstance(relationship, ToManyRelationshipBase):
                for obj in relationship():
                    yield edge(self.guid(), guid(obj))

    def impacted_by(self, relname):
        relationship = getattr(self._object, relname, None)
        if relationship:
            if isinstance(relationship, ToOneRelationship):
                obj = relationship()
                if obj:
                    yield edge(guid(obj), self.guid())

            elif isinstance(relationship, ToManyRelationshipBase):
                for obj in relationship():
                    yield edge(guid(obj), self.guid())

    def getEdges(self):
        if self.impact_relationships is not None:
            for impact_relationship in self.impact_relationships:
                for impact in self.impact(impact_relationship):
                    yield impact

        if self.impacted_by_relationships is not None:
            for impacted_by_relationship in self.impacted_by_relationships:
                for impacted_by in self.impacted_by(impacted_by_relationship):
                    yield impacted_by


class DeviceRelationsProvider(BaseRelationsProvider):
    impact_relationships = ['z_systems']


class SystemRelationsProvider(BaseRelationsProvider):
    impacted_by_relationships = ['z_device']
    impact_relationships = ['processes']


class ProcessRelationsProvider(BaseRelationsProvider):
    impacted_by_relationships = ['system']
    impact_relationships = ['metrics']


class MetricRelationsProvider(BaseRelationsProvider):
    impacted_by_relationships = ['process']
