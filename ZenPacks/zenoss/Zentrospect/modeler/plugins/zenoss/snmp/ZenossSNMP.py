#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################

'''
Models systems, processes and their metrics from a server running Zenoss
and the zenoss-snmp-module extension to Net-SNMP.
'''

import logging
LOG = logging.getLogger('zen.Zentrospect')

import itertools
import re

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import RelationshipMap

from ZenPacks.zenoss.Zentrospect import MODULE_NAME


class ZenossSNMP(SnmpPlugin):
    deviceProperties = SnmpPlugin.deviceProperties + (
        'zZentrospectIgnoreSystems',
        'zZentrospectIgnoreProcesses',
        'zZentrospectIgnoreMetrics',
        )

    snmpGetTableMaps = (
        GetTableMap('zenProcessMetricTable', '1.3.6.1.4.1.14296.3.3.1', {
            '.1': 'zenProcessMetricName',
            }),
        )

    def process(self, device, results, log):
        log.info("processing %s for device %s", self.name(), device.id)

        ignore_systems = getattr(device, 'zZentrospectIgnoreSystems', None)
        ignore_processes = getattr(device, 'zZentrospectIgnoreProcesses', None)
        ignore_metrics = getattr(device, 'zZentrospectIgnoreMetrics', None)

        metric_table = results[1].get('zenProcessMetricTable', {})

        systems = {}

        for snmpindex, row in metric_table.items():
            decoded = snmpindex_tuples(snmpindex)
            system_name, system_snmpindex = decoded.next()
            process_name, process_snmpindex = decoded.next()
            metric_name, metric_snmpindex = decoded.next()

            system_id = self.prepId('-'.join([
                'z', system_name]))

            systems.setdefault(system_id, {
                'title': system_name,
                'name': system_name,
                'snmpindex': system_snmpindex,
                'processes': {},
                })

            process_id = self.prepId('-'.join([
                'z', system_name, process_name]))

            processes = systems[system_id]['processes']
            processes.setdefault(process_id, {
                'title': '-'.join([system_name, process_name]),
                'name': process_name,
                'snmpindex': process_snmpindex,
                'metrics': {},
                })

            metric_id = self.prepId('-'.join([
                'z', system_name, process_name, metric_name]))

            metrics = systems[system_id]['processes'][process_id]['metrics']
            metrics.setdefault(metric_id, {
                'title': '-'.join([system_name, process_name, metric_name]),
                'name': metric_name,
                'snmpindex': metric_snmpindex,
                })

        system_rm = RelationshipMap(
            relname='z_systems')

        maps = [system_rm]

        for system_id, system in systems.items():
            if ignore_systems and re.search(ignore_systems, system['title']):
                LOG.info("ignoring Zenoss system %s", system['title'])
                continue

            system_rm.append(ObjectMap(data={
                'modname': MODULE_NAME['System'],
                'id': system_id,
                'title': system['title'],
                'system_name': system['name'],
                'snmpindex': system['snmpindex'],
                }))

            process_rm = RelationshipMap(
                compname='z_systems/{0}'.format(system_id),
                relname='processes')

            maps.append(process_rm)

            for process_id, process in system['processes'].items():
                if ignore_processes and re.search(ignore_processes, process['title']):
                    LOG.info("ignoring Zenoss process %s", process['title'])
                    continue

                process_rm.append(ObjectMap(data={
                    'modname': MODULE_NAME['Process'],
                    'id': process_id,
                    'title': process['title'],
                    'process_name': process['name'],
                    'snmpindex': process['snmpindex'],
                    }))

                metric_rm = RelationshipMap(
                    compname='z_systems/{0}/processes/{1}'.format(system_id, process_id),
                    relname='metrics')

                maps.append(metric_rm)

                for metric_id, metric in process['metrics'].items():
                    if ignore_metrics and re.search(ignore_metrics, metric['title']):
                        LOG.info("ignoring Zenoss metric %s", metric['title'])
                        continue

                    metric_rm.append(ObjectMap(data={
                        'modname': MODULE_NAME['Metric'],
                        'id': metric_id,
                        'title': metric['title'],
                        'metric_name': metric['name'],
                        'snmpindex': metric['snmpindex'],
                        }))

        return maps


def snmpindex_tuples(snmpindex):
    full_parts = []

    parts_iter = itertools.imap(int, snmpindex.strip('.').split('.'))

    for part in parts_iter:
        section_parts = list(itertools.islice(parts_iter, part))
        full_parts.append(part)
        full_parts.extend(section_parts)

        yield (
            ''.join(map(chr, section_parts)),
            '.'.join(map(str, full_parts)),
            )
