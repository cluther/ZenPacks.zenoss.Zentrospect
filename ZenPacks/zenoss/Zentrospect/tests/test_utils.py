#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################

'''
Tests for utilities.
'''

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ZenPacks.zenoss.Zentrospect.utils import sorted_powerset


class TestUtils(BaseTestCase):
    def test_sorted_powerset(self):
        input1 = ('localhost', 'zendisc', 'devices')
        output1 = sorted_powerset(input1)
        expected1 = (
            ('localhost', 'zendisc', 'devices'),
            ('zendisc', 'devices'),
            ('localhost', 'devices'),
            ('localhost', 'zendisc'),
            ('devices',),
            ('zendisc',),
            ('localhost',),
            (),
            )

        self.assertEquals(tuple(output1), expected1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUtils))
    return suite
