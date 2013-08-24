#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################


def add_contained(obj, relname, target):
    '''
    Add and return obj to containing relname on target.
    '''
    rel = getattr(obj, relname)
    rel._setObject(target.id, target)
    return rel._getOb(target.id)
