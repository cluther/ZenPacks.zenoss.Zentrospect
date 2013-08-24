#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################

from itertools import chain, combinations


def sorted_powerset(iterable):
    '''
    Return iterable of n-length combinations of iterable sorted in the
    right order of specificity.

    Input iterable example::

        ('localhost', 'zendisc', 'devices')

    Returned iterable::

        (
            ('localhost', 'zendisc', 'devices'),
            ('zendisc', 'devices'),
            ('localhost', 'devices'),
            ('localhost', 'zendisc'),
            ('devices',),
            ('zendisc',),
            ('localhost',),
            (),
        )
    '''
    return reversed(tuple(
        chain.from_iterable(
            combinations(iterable, r) for r in range(len(iterable)+1))))
